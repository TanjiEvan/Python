import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import pytz
import xlsxwriter
import logging
import os
import tempfile
import requests
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set current date and time dynamically to the current date and time in Asia/Dhaka timezone
bangladesh_tz = pytz.timezone('Asia/Dhaka')
current_datetime = datetime.now(bangladesh_tz)
current_date = current_datetime.date()

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .main, .stApp {
        background-color: #1f2937;
        color: #f9fafb;
    }
    h1 {
        color: #34d399;
        font-size: 2.5em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5em;
    }
    h2, h3, h4, h5, h6 {
        color: #34d399;
        font-weight: 600;
        margin-bottom: 0.75em;
    }
    .stMarkdown, .stDataFrame {
        color: #d1d5db;
    }
    .stDateInput, .stFileUploader, .stSelectbox, .stCheckbox, .stButton, .stMetric, .stExpander, .stPlotlyChart, .stRadio {
        margin-bottom: 2em !important;
        padding: 0.5em;
    }
    .stContainer {
        margin-bottom: 2em !important;
        padding: 1em;
    }
    .overview-card {
        background-color: #374151;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        text-align: center;
        color: #f9fafb;
        transition: transform 0.2s;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .overview-card:hover {
        transform: translateY(-5px);
    }
    .overview-card i {
        color: #34d399;
        font-size: 1.8em;
        margin-bottom: 10px;
    }
    .overview-card h3 {
        margin: 0;
        font-size: 1em;
        color: #34d399;
        font-weight: 400;
        white-space: normal;
        text-align: center;
        line-height: 1.2;
        max-width: 90%;
    }
    .overview-card p {
        margin: 10px 0 0;
        font-size: 1.8em;
        font-weight: 600;
        color: #f9fafb;
    }
    .dept-container {
        background-color: #374151;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    .employee-card {
        background-color: #4b5563;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
        display: flex;
        flex-direction: column;
    }
    .employee-card h4 {
        margin: 0 0 5px;
        color: #34d399;
        font-weight: 600;
    }
    .employee-card p {
        margin: 2px 0;
        color: #d1d5db;
    }
    .stSelectbox, .stDateInput, .stFileUploader, .stCheckbox, .stButton, .stRadio {
        background-color: #374151 !important;
        border-radius: 8px;
        color: #f9fafb !important;
    }
    .stSelectbox > div > div, .stDateInput > div > div, .stFileUploader > div > div, .stRadio > label {
        background-color: #374151 !important;
        color: #f9fafb !important;
    }
    .stButton > button {
        background-color: #34d399;
        color: #1f2937;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #6ee7b7;
    }
    .stDataFrame table {
        background-color: #374151;
        color: #f9fafb;
        border-radius: 8px;
    }
    .stDataFrame th {
        background-color: #4b5563 !important;
        color: #34d399 !important;
        font-weight: 600;
    }
    .stDataFrame td {
        color: #d1d5db !important;
    }
    .stMetric {
        background-color: #374151;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom: 1em;
    }
    .stMetric label {
        color: #34d399 !important;
        font-weight: 600 !important;
        white-space: normal;
        line-height: 1.2;
        font-size: 0.85em;
    }
    .stMetric div {
        color: #f9fafb !important;
        font-size: 1.3em !important;
    }
    .stTabs [role="tab"] {
        color: #34d399;
        font-weight: 600;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        color: #f9fafb;
        border-bottom: 2px solid #34d399;
    }
    .stExpander {
        background-color: #374151;
        border-radius: 8px;
        color: #f9fafb;
    }
    .stExpander summary {
        color: #34d399;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app title
st.title("Completion Report Dashboard")

# Sidebar for report type selection
st.sidebar.header("Report Type")
report_type = st.sidebar.radio("Select Report Type", ["Daily Report", "Monthly Report", "Hourly Employee Monitoring", "Status Report"], index=0)

# Sidebar for additional filters
st.sidebar.header("Filter Options")
st.sidebar.markdown("### Refine Your View")
show_table_overview = st.sidebar.checkbox("Show Table Overview", value=True)

# Employee → Department Mapping
employee_department_map = {
    "Md. Rezwanul Haque": "Network, IT & Internal Support",
    "Md. Shezan Mahmud": "Production & Media",
    "Md. Nazim Mahmud": "Production & Media",
    "Md. Jobayer Rahman": "Software Development",
    "Tanvir Islam": "Software Development",
    "Towfiqur Rahman": "Creative Marketing",
    "Md. Asif Saharwar": "Operations & Support",
    "Md. Ariful Islam (Rafi)": "Network, IT & Internal Support",
    "Md. Fahim Hasan Shah": "Network, IT & Internal Support",
    "Md. Sakib Shahriar": "Software Development",
    "Md. Arman Al Sharif": "Operations & Support",
    "Md. Muyed Moktadir Chowdhury": "Operations & Support",
    "Sohanur Rahman (Niloy)": "Production & Media",
    "Md. Shariar Hossen": "Creative Marketing",
    "Badhon Kumar Roy": "Software Development",
    "Md. Sohel Rana": "HR, Admin, Finance & Accounts",
    "Md. Rezaul Karim": "HR, Admin, Finance & Accounts",
    "Md Sajibur Rahman": "Operations & Support",
    "Md. Sadik": "Retail & Business",
    "Salma Nashin Esha": "Creative Marketing",
    "Sunnyat Ali": "Creative Marketing"
}

# Name mapping dictionary
name_mapping = {
    "Fahim Hasan Shah": "Md. Fahim Hasan Shah",
    "Niloy Ahmed": "Sohanur Rahman (Niloy)",
    "MD. Rezwanul Haque": "Md. Rezwanul Haque",
    "Sabbir": "Md. Shariar Hossen",
    "Sabbir Hossen": "Md. Shariar Hossen",
    "MD Arman Al Sharif": "Md. Arman Al Sharif",
    "Md. Sohel Rana": "Md. Sohel Rana",
    "Tanvir Islam": "Tanvir Islam",
    "Badhon Kumar Roy": "Badhon Kumar Roy",
    "Md. Muyed Moktadir": "Md. Muyed Moktadir Chowdhury",
    "Md. Ariful Islam": "Md. Ariful Islam (Rafi)",
    "Sakib Shahriar": "Md. Sakib Shahriar",
    "Md. Nazim Mahmud": "Najim Mahmud"
}

# Employee code mapping dictionary
employee_code_mapping = {
    "Tanvir Islam": 10003,
    "Md. Ariful Islam (Rafi)": 10005,
    "Md. Sakib Shahriar": 10013,
    "Md. Shariar Hossen": 10014,
    "Md. Sohel Rana": 10016,
    "Md Sajibur Rahman": 10018,
    "Salma Nashin Esha": 10017,
    "Md. Fahim Hasan Shah": 10019,
    "Md. Rezwanul Haque": 10020,
    "Md. Rezaul Karim": 10021,
    "Md. Jobayer Rahman": 10025,
    "Sohanur Rahman (Niloy)": 10026,
    "Md. Asif Saharwar": 10027,
    "Towfiqur Rahman": 10028,
    "Md. Arman Al Sharif": 10006,
    "Badhon Kumar Roy": 10011,
    "Md. Muyed Moktadir Chowdhury": 10004,
    "Md. Shezan Mahmud": 20001,
    "Md. Nazim Mahmud": 20002,
    "Md. Sadik": 30001,
}

# Space-to-Department Mapping
space_department_map = {
    "682eb692f3f2e6c5c6efba70": "Operations & Support",
    "682eb774f3f2e6c5c6efbb82": "Creative Marketing",
    "682eb843f3f2e6c5c6efbc91": "Retail & Business",
    "682eb2cdf3f2e6c5c6efa6ac": "Network, IT & Internal Support",
    "682eb6f4f3f2e6c5c6efbad9": "HR, Admin, Finance & Accounts",
    "682eb116f3f2e6c5c6efa21f": "Software Development",
    "682eb7f5f3f2e6c5c6efbc19": "Production & Media"
}

# Department heads mapping
department_heads_mapping = {
    "Network, IT & Internal Support": "Md. Fahim Hasan Shah",
    "Operations & Support": "Md. Arman Al Sharif",
    "HR, Admin, Finance & Accounts": "Md. Sohel Rana",
    "Software Development": "Tanvir Islam",
    "Production & Media": "Md. Shezan Mahmud",
    "Creative Marketing": "Sunnyat Ali",
    "Retail & Business": "Sunnyat Ali"
}

# Function to extract plain text from JSON comment
def extract_plain_text(comment_json):
    try:
        # If comment is a string, try to parse it as JSON
        if isinstance(comment_json, str):
            comment_data = json.loads(comment_json)
        else:
            comment_data = comment_json

        # Navigate through the nested structure to find the text
        if isinstance(comment_data, dict) and 'type' in comment_data and comment_data['type'] == 'doc':
            content = comment_data.get('content', [])
            for block in content:
                if block.get('type') == 'paragraph':
                    paragraph_content = block.get('content', [])
                    for item in paragraph_content:
                        if item.get('type') == 'text' and 'text' in item:
                            return item['text']
        return ""
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        logger.warning(f"Error parsing comment JSON: {str(e)}")
        return ""

# Function to process data for reports
def process_data(data, start_date, end_date):
    bangladesh_tz = pytz.timezone('Asia/Dhaka')
    start_of_period = datetime(start_date.year, start_date.month, start_date.day, tzinfo=bangladesh_tz)
    end_of_period = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59, 999999, tzinfo=bangladesh_tz)

    processed_data = []
    for item in data:
        try:
            modified_on_ts = item.get("modifiedOn")
            created_on_ts = item.get("createdOn")
            due_date_ts = item.get("dueDate")
            modified_on_dt = datetime.fromtimestamp(modified_on_ts / 1000, pytz.utc).astimezone(bangladesh_tz) if modified_on_ts else None
            created_on_dt = datetime.fromtimestamp(created_on_ts / 1000, pytz.utc).astimezone(bangladesh_tz) if created_on_ts else None
            due_date_dt = datetime.fromtimestamp(due_date_ts / 1000, pytz.utc).astimezone(bangladesh_tz) if due_date_ts else None

            is_relevant = False
            if (modified_on_dt and start_of_period <= modified_on_dt <= end_of_period) or (created_on_dt and start_of_period <= created_on_dt <= end_of_period):
                is_relevant = True
            elif due_date_dt and due_date_dt.date() <= end_date:
                is_relevant = True

            if not is_relevant:
                continue

            employee_raw = item.get("assignee", "Unassigned")
            employee_cleaned = employee_raw.strip(',').strip()
            if employee_cleaned != "Unassigned" and "," in employee_cleaned:
                last_name, first_name = employee_cleaned.split(",", 1)
                employee = f"{first_name.strip()} {last_name.strip()}"
            else:
                employee = employee_cleaned

            mapped_employee = name_mapping.get(employee, employee)

            space_id = item.get("space")
            department = space_department_map.get(space_id, "Unknown")
            department_head = department_heads_mapping.get(department, "N/A")
            raw_status = item.get("status", "Unknown")
            task_title = item.get("title", "No Title")
            task_identifier = item.get("identifier", "No ID")
            estimation = item.get("estimation", 0)
            reported_time = item.get("reportedTime", 0)
            comment = item.get("comment", "")

            # Extract the latest comment from the activity array
            activity = item.get("activity", [])
            latest_comment = ""
            latest_comment_time = None
            for act in activity:
                message = act.get("message", "")
                modified_on = item.get("modifiedOn")
                if message and modified_on:
                    mod_time = datetime.fromtimestamp(modified_on / 1000, pytz.utc).astimezone(bangladesh_tz)
                    plain_text = extract_plain_text(message)
                    if plain_text and (not latest_comment_time or mod_time > latest_comment_time):
                        latest_comment = plain_text
                        latest_comment_time = mod_time

            has_comment = "Yes" if (comment and comment.strip()) or latest_comment else "No"

            status = raw_status
            is_completed = raw_status == "DONE"

            task_url = f"https://huly.app/workbench/sohub/tracker/{task_identifier}"

            completed_tasks = task_title if is_completed else ""
            completed_task_urls = task_url if is_completed else ""
            incomplete_tasks = task_title if not is_completed else ""
            incomplete_task_urls = task_url if not is_completed else ""

            rules_violated = "No"
            rules_violated_urls = ""
            violation_types = []
            if not space_id or department == "Unknown":
                rules_violated = "Yes"
                rules_violated_urls = task_url
                violation_types.append("Missing Space")
            if due_date_dt is None:
                rules_violated = "Yes"
                rules_violated_urls = task_url
                violation_types.append("Missing Due Date")

            violation_type = ", ".join(violation_types) if violation_types else ""

            if rules_violated == "Yes":
                mapped_employee = f"{mapped_employee} [Rule Violator]"

            employee_code = employee_code_mapping.get(mapped_employee.split(" [Rule Violator]")[0], None)

            remarks = ""
            if is_completed:
                remarks = "Completed"
            elif due_date_dt:
                current_date_dt = current_date
                if due_date_dt.date() < current_date_dt:
                    remarks = "Overdue"
                elif due_date_dt.date() >= current_date_dt:
                    remarks = "In Progress"
            else:
                remarks = "Due date is missing"
            if violation_types:
                remarks += f" ({violation_type})"

            processed_data.append({
                "Employee Name": mapped_employee,
                "Employee Code": str(employee_code) if employee_code is not None else None,
                "Department Name": department,
                "Department Head": department_head,
                "Task Identifier": task_identifier,
                "Task Status": status,
                "Tasks Completed": completed_tasks,
                "Completed Task URLs": completed_task_urls,
                "Incomplete Tasks": incomplete_tasks,
                "Incomplete Task URLs": incomplete_task_urls,
                "Due Date": due_date_dt.strftime('%Y-%m-%d') if due_date_dt else "N/A",
                "Rules Violated": rules_violated,
                "Rules Violated URLs": rules_violated_urls,
                "Violation Type": violation_type,
                "Estimated Time": estimation,
                "Reported Time": reported_time,
                "Comments": has_comment,
                "Modified On": modified_on_dt,
                "Task Title": task_title,
                "Comment": latest_comment if latest_comment else comment,
                "Remarks": remarks
            })
        except Exception as e:
            logger.error(f"Error processing task: {item}. Error: {str(e)}")
            continue

    return processed_data

# Function to check for employees with no tasks in the morning report
def check_no_work_assigned(morning_data):
    all_employees = set(employee_code_mapping.keys())
    tasks_assigned = set()
    for item in morning_data:
        raw = item.get("assignee", "Unassigned").strip().strip(',')
        if raw != "Unassigned":
            if ',' in raw:
                ln, fn = raw.split(',', 1)
                emp = f"{fn.strip()} {ln.strip()}"
            else:
                emp = raw
            tasks_assigned.add(name_mapping.get(emp, emp))

    no_work_rows = []
    for emp in all_employees:
        mapped = name_mapping.get(emp, emp)
        if mapped not in tasks_assigned:
            dept = employee_department_map.get(mapped, "Unknown")
            head = department_heads_mapping.get(dept, "N/A")
            no_work_rows.append({
                "Department Name": dept,
                "Department Head": head,
                "Employee Name": mapped,
                "Employee Code": str(employee_code_mapping.get(mapped, "N/A")),
                "Status": "No work assigned/created yet",
                "Task Title": "N/A",
                "Task Identifier": "N/A",
                "Due Date": "N/A",
                "Remarks": "No tasks assigned or created"
            })

    return pd.DataFrame(no_work_rows)

# Function to process data for hourly monitoring
def process_hourly_data(data):
    bangladesh_tz = pytz.timezone('Asia/Dhaka')
    processed_data = []
    employee_tasks = {}

    for item in data:
        try:
            modified_on_ts = item.get("modifiedOn")
            modified_on_dt = datetime.fromtimestamp(modified_on_ts / 1000, pytz.utc).astimezone(bangladesh_tz) if modified_on_ts else None
            employee_raw = item.get("assignee", "Unassigned")
            employee_cleaned = employee_raw.strip(',').strip()
            employee = employee_cleaned.split(",", 1)[-1].strip() + " " + employee_cleaned.split(",", 1)[0].strip() if "," in employee_cleaned and employee_cleaned != "Unassigned" else employee_cleaned

            mapped_employee = name_mapping.get(employee, employee)

            space_id = item.get("space")
            department = space_department_map.get(space_id, "Unknown")
            task_title = item.get("title", "No Title")
            status = item.get("status", "Unknown")
            comment = item.get("comment", "")

            employee_code = employee_code_mapping.get(mapped_employee, None)

            if employee not in employee_tasks or modified_on_dt > employee_tasks[employee].get("last_updated", datetime.min):
                employee_tasks[employee] = {
                    "mapped_employee": mapped_employee,
                    "employee_code": employee_code,
                    "department": department,
                    "department_head": department_heads_mapping.get(department, "N/A"),
                    "current_work": task_title,
                    "last_status": status,
                    "last_updated": modified_on_dt,
                    "comment": comment
                }
        except Exception as e:
            logger.error(f"Error processing task: {item}. Error: {str(e)}")
            continue

    for employee, details in employee_tasks.items():
        processed_data.append({
            "Employee Name": details["mapped_employee"],
            "Employee Code": str(details["employee_code"]) if details["employee_code"] is not None else None,
            "Department Name": details["department"],
            "Department Head": details["department_head"],
            "Current Work": details["current_work"],
            "Last Status": details["last_status"],
            "Last Updated": details["last_updated"].strftime('%Y-%m-%d %H:%M') if details["last_updated"] else "",
            "Comment": details["comment"] or "No comment"
        })

    return processed_data

# Function to display analysis
def display_analysis(df, period_label, set1_colors):
    with st.container():
        st.header("Quick Overview")
        st.markdown(f"A snapshot of key task performance metrics for the {period_label}.", unsafe_allow_html=True)

        total_tasks = df.shape[0]
        done = df[df['Task Status'] == 'DONE'].shape[0]
        in_progress = df[df['Task Status'] == 'In Progress'].shape[0]
        rule_violations_count = df[df['Rules Violated'] == 'Yes'].shape[0]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="overview-card">
                    <i class="fas fa-tasks"></i>
                    <h3>Total Tasks</h3>
                    <p>{total_tasks}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="overview-card">
                    <i class="fas fa-check-circle"></i>
                    <h3>Done</h3>
                    <p>{done}</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="overview-card">
                    <i class="fas fa-spinner"></i>
                    <h3>In Progress</h3>
                    <p>{in_progress}</p>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="overview-card">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Rule Violations</h3>
                    <p>{rule_violations_count}</p>
                </div>
            """, unsafe_allow_html=True)

    with st.container():
        st.header("Analysis Dashboard")

        st.subheader(f"Q1: What is the overall completion rate of tasks in the {period_label}?")
        total_tasks = df.shape[0]
        completed_tasks = done
        incomplete_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        incomplete_rate = (incomplete_tasks / total_tasks * 100) if total_tasks > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", total_tasks)
        with col2:
            st.metric("Completed Tasks", f"{completed_tasks} ({completion_rate:.2f}%)")
        with col3:
            st.metric("Incomplete Tasks", f"{incomplete_tasks} ({incomplete_rate:.2f}%)")

        task_status_counts = df['Task Status'].value_counts().reset_index()
        task_status_counts.columns = ['Task Status', 'Count']
        with st.expander("View Task Status Breakdown"):
            st.write(task_status_counts)

        fig1 = go.Figure(data=[
            go.Pie(labels=['Completed', 'Incomplete'],
                   values=[completed_tasks, incomplete_tasks],
                   textinfo='label+percent',
                   marker=dict(colors=set1_colors[:2]))
        ])
        fig1.update_layout(title_text=f'Overall Task Completion Rate ({period_label})',
                           font=dict(color='#f9fafb'))
        st.plotly_chart(fig1, use_container_width=True)

        fig1b = px.bar(task_status_counts, x='Task Status', y='Count',
                       title=f'Task Status Distribution ({period_label})',
                       labels={'Count': 'Number of Tasks'},
                       color='Task Status',
                       color_discrete_sequence=set1_colors)
        fig1b.update_layout(xaxis_title='Task Status', yaxis_title='Number of Tasks', xaxis_tickangle=-45, showlegend=False,
                            font=dict(color='#f9fafb'))
        st.plotly_chart(fig1b, use_container_width=True)

        st.subheader(f"Q2: What is the task completion rate per employee in the {period_label}?")
        with st.container():
            q2_employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
            q2_selected_employee = st.selectbox("Filter by Employee (Q2)", q2_employees, key="q2_employee_filter")
            df_q2 = df.copy()
            if q2_selected_employee != "All":
                df_q2 = df_q2[df_q2['Employee Name'].str.contains(q2_selected_employee, na=False)]

        employee_stats = df_q2.groupby('Employee Name').agg({
            'Task Status': [
                lambda x: sum(x == 'DONE'),
                lambda x: sum(x != 'DONE')
            ],
            'Employee Code': 'first'
        }).reset_index()
        employee_stats.columns = ['Employee Name', 'Tasks Completed', 'Incomplete Tasks', 'Employee Code']
        employee_stats['Employee Name'] = employee_stats['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True)
        employee_stats = employee_stats.groupby('Employee Name').sum().reset_index()
        employee_stats['Total Tasks'] = employee_stats['Tasks Completed'] + employee_stats['Incomplete Tasks']
        employee_stats['Completion Rate (%)'] = (employee_stats['Tasks Completed'] / employee_stats['Total Tasks'] * 100).round(2)

        employee_task_status = df_q2.groupby(['Employee Name', 'Task Status']).size().unstack(fill_value=0).reset_index()
        employee_task_status['Employee Name'] = employee_task_status['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True)
        employee_task_status = employee_task_status.groupby('Employee Name').sum().reset_index()

        tab1, tab2 = st.tabs(["Completion Rate", "Task Status Breakdown"])
        with tab1:
            st.write("**Completion Rate per Employee:**")
            st.write(employee_stats[['Employee Name', 'Employee Code', 'Tasks Completed', 'Incomplete Tasks', 'Total Tasks', 'Completion Rate (%)']])
            fig2 = px.bar(employee_stats, x='Employee Name', y='Completion Rate (%)',
                          title=f'Task Completion Rate per Employee ({period_label})',
                          labels={'Completion Rate (%)': 'Completion Rate (%)'},
                          color='Employee Name',
                          color_discrete_sequence=set1_colors)
            fig2.update_layout(xaxis_title='Employee Name', yaxis_title='Completion Rate (%)', xaxis_tickangle=-45, showlegend=False,
                               font=dict(color='#f9fafb'))
            st.plotly_chart(fig2, use_container_width=True)
        with tab2:
            st.write("**Task Status Breakdown per Employee:**")
            st.write(employee_task_status)

        st.subheader(f"Q3: What is the task completion rate per department in the {period_label}?")
        department_stats = df.groupby('Department Name').agg({
            'Task Status': [
                lambda x: sum(x == 'DONE'),
                lambda x: sum(x != 'DONE')
            ]
        }).reset_index()
        department_stats.columns = ['Department Name', 'Tasks Completed', 'Incomplete Tasks']
        department_stats['Total Tasks'] = department_stats['Tasks Completed'] + department_stats['Incomplete Tasks']
        department_stats['Completion Rate (%)'] = (department_stats['Tasks Completed'] / department_stats['Total Tasks'] * 100).round(2)

        for _, row in department_stats.iterrows():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.metric("Department", row['Department Name'])
            with col2:
                st.metric("Tasks Completed", row['Tasks Completed'])
            with col3:
                st.metric("Incomplete Tasks", row['Incomplete Tasks'])
            with col4:
                st.metric("Completion Rate (%)", f"{row['Completion Rate (%)']}%")

        department_task_status = df.groupby(['Department Name', 'Task Status']).size().unstack(fill_value=0).reset_index()
        with st.expander("View Task Status Breakdown per Department"):
            st.write(department_task_status)

        fig3 = px.bar(department_stats, x='Department Name', y='Completion Rate (%)',
                      title=f'Task Completion Rate per Department ({period_label})',
                      labels={'Completion Rate (%)': 'Completion Rate (%)'},
                      color='Department Name',
                      color_discrete_sequence=set1_colors)
        fig3.update_layout(xaxis_title='Department Name', yaxis_title='Completion Rate (%)', xaxis_tickangle=-45, showlegend=False,
                           font=dict(color='#f9fafb'))
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader(f"Q4: Which incomplete tasks need attention, and what are their direct URLs for review in the {period_label}?")
        with st.container():
            q4_employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
            q4_selected_employee = st.selectbox("Filter by Employee (Q4)", q4_employees, key="q4_employee_filter")
            df_q4 = df.copy()
            if q4_selected_employee != "All":
                df_q4 = df_q4[df_q4['Employee Name'].str.contains(q4_selected_employee, na=False)]

            incomplete_tasks_df = df_q4[df_q4['Task Status'] != 'DONE'][['Employee Name', 'Employee Code', 'Department Name', 'Incomplete Tasks', 'Incomplete Task URLs', 'Due Date', 'Comments', 'Remarks']]
            if not incomplete_tasks_df.empty:
                st.write("**Incomplete Tasks:**")
                st.dataframe(incomplete_tasks_df)
            else:
                st.write("No incomplete tasks found for the selected period.")

        st.subheader(f"Q5: How many tasks violated rules, and who are the responsible employees in the {period_label}?")
        with st.container():
            q5_employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
            q5_selected_employee = st.selectbox("Filter by Employee (Q5)", q5_employees, key="q5_employee_filter")
            df_q5 = df.copy()
            if q5_selected_employee != "All":
                df_q5 = df_q5[df_q5['Employee Name'].str.contains(q5_selected_employee, na=False)]

            rule_violations_df = df_q5[df_q5['Rules Violated'] == 'Yes'][['Employee Name', 'Employee Code', 'Task Identifier', 'Rules Violated URLs', 'Violation Type', 'Remarks']]
            rule_violations_df['Employee Name'] = rule_violations_df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True)
            rule_violations_summary = rule_violations_df.groupby('Employee Name').size().reset_index(name='Rule Violations')

            if not rule_violations_df.empty:
                try:
                    api_url = "Startup_Employee_Monitoring_&_Task_Management/api.php"
                    payload = rule_violations_df.to_dict(orient='records')
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(api_url, json=payload, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        logger.info("Successfully sent rule violation data to API")
                        st.success("Rule violation data successfully sent to the portal!")
                    else:
                        logger.error(f"Failed to send data to API. Status code: {response.status_code}, Response: {response.text}")
                        st.error(f"Failed to send rule violation data to the portal. Status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error sending data to API: {str(e)}")
                    st.error(f"Error sending rule violation data to the portal: {str(e)}")

            if not rule_violations_df.empty:
                st.write("**Rule Violations Summary:**")
                st.write(rule_violations_summary)
                st.write("**Details of Rule Violations:**")
                st.dataframe(rule_violations_df)
                fig5 = px.bar(rule_violations_summary, x='Employee Name', y='Rule Violations',
                              title=f'Rule Violations per Employee ({period_label})',
                              labels={'Rule Violations': 'Number of Rule Violations'},
                              color='Employee Name',
                              color_discrete_sequence=set1_colors)
                fig5.update_layout(xaxis_title='Employee Name', yaxis_title='Number of Rule Violations', xaxis_tickangle=-45, showlegend=False,
                                   font=dict(color='#f9fafb'))
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.write("No rule violations found for the selected period.")

        st.subheader(f"Q6: Which tasks were completed, and what are their due dates, task identifiers, and URLs in the {period_label}?")
        with st.container():
            q6_employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
            q6_selected_employee = st.selectbox("Filter by Employee (Q6)", q6_employees, key="q6_employee_filter")
            df_q6 = df.copy()
            if q6_selected_employee != "All":
                df_q6 = df_q6[df_q6['Employee Name'].str.contains(q6_selected_employee, na=False)]

        completed_tasks_df = df_q6[df_q6['Tasks Completed'] != ''][['Employee Name', 'Employee Code', 'Department Name', 'Tasks Completed', 'Task Identifier', 'Due Date', 'Completed Task URLs', 'Comments', 'Remarks']]
        if not completed_tasks_df.empty:
            st.write("**Completed Tasks:**")
            st.dataframe(completed_tasks_df)
        else:
            st.write("No completed tasks found for the selected period.")

        st.subheader(f"Q7: How does the estimated time compare to the reported time per department in the {period_label}?")
        df['Estimated Time'] = pd.to_numeric(df['Estimated Time'], errors='coerce')
        df['Reported Time'] = pd.to_numeric(df['Reported Time'], errors='coerce')
        time_comparison = df.groupby('Department Name').agg({
            'Estimated Time': ['sum', 'mean'],
            'Reported Time': ['sum', 'mean']
        }).reset_index()
        time_comparison.columns = ['Department Name', 'Total Estimated Time', 'Avg Estimated Time', 'Total Reported Time', 'Avg Reported Time']
        time_comparison['Total Difference'] = time_comparison['Total Reported Time'] - time_comparison['Total Estimated Time']
        time_comparison['Avg Difference'] = time_comparison['Avg Reported Time'] - time_comparison['Avg Estimated Time']
        time_comparison = time_comparison.round(2)

        st.write("**Estimated vs Reported Time Summary:**")
        st.write(time_comparison)

        fig7 = go.Figure(data=[
            go.Bar(name='Total Estimated Time', x=time_comparison['Department Name'], y=time_comparison['Total Estimated Time'], marker_color=set1_colors[0]),
            go.Bar(name='Total Reported Time', x=time_comparison['Department Name'], y=time_comparison['Total Reported Time'], marker_color=set1_colors[1])
        ])
        fig7.update_layout(
            title=f'Total Estimated vs Reported Time per Department ({period_label})',
            xaxis_title='Department Name',
            yaxis_title='Time (hours)',
            xaxis_tickangle=-45,
            barmode='group',
            font=dict(color='#f9fafb')
        )
        st.plotly_chart(fig7, use_container_width=True)

# File uploader for reports except Status Report
if report_type in ["Daily Report", "Monthly Report", "Hourly Employee Monitoring"]:
    with st.container():
        uploaded_file = st.file_uploader("Upload the JSON File", type=["json"], key="single_upload")
    if uploaded_file is None:
        st.warning("Please upload a JSON file to proceed.")
        st.stop()
    try:
        data = json.load(uploaded_file)
        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of task objects")
    except Exception as e:
        logger.error(f"Error reading JSON file: {str(e)}")
        st.error(f"Failed to read the JSON file: {str(e)}")
        st.stop()

# Process reports based on report type
if report_type == "Daily Report":
    with st.container():
        selected_date = st.date_input("Select Report Date", value=current_date, min_value=date(2000, 1, 1), max_value=current_date)

    if selected_date > current_date:
        st.error(f"Invalid date selected. Please choose a date on or before {current_date}.")
        st.stop()

    bangladesh_tz = pytz.timezone('Asia/Dhaka')
    report_date = datetime(selected_date.year, selected_date.month, selected_date.day, tzinfo=bangladesh_tz)
    start_of_day = report_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = report_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    with st.container():
        st.markdown(f"### Daily Report for {report_date.strftime('%B %d, %Y')}", unsafe_allow_html=True)

    processed_data = process_data(data, selected_date, selected_date)
    if not processed_data:
        st.error(f"No relevant tasks found in the JSON file for {report_date.strftime('%B %d, %Y')}.")
        st.stop()

    df = pd.DataFrame(processed_data)

    column_order = [
        "Employee Name",
        "Employee Code",
        "Department Name",
        "Department Head",
        "Task Identifier",
        "Task Status",
        "Tasks Completed",
        "Completed Task URLs",
        "Incomplete Tasks",
        "Incomplete Task URLs",
        "Due Date",
        "Rules Violated",
        "Rules Violated URLs",
        "Violation Type",
        "Estimated Time",
        "Reported Time",
        "Comments",
        "Remarks"
    ]

    df = df[column_order]

    departments = ["All"] + sorted(list(space_department_map.values()))
    selected_department = st.sidebar.selectbox("Filter by Department", departments)
    if selected_department != "All":
        df = df[df['Department Name'] == selected_department]

    with st.container():
        employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
        selected_employee = st.selectbox("Filter by Employee (Global)", employees)
        if selected_employee != "All":
            df = df[df['Employee Name'].str.contains(selected_employee, na=False)]

    output_filename = os.path.join(tempfile.gettempdir(), f'daily_completion_report_{selected_date.strftime("%Y-%m-%d")}.xlsx')
    try:
        writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Report', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Report']
        for col_num, col_name in enumerate(column_order):
            max_length = max(df[col_name].astype(str).map(len).max(), len(col_name))
            worksheet.set_column(col_num, col_num, max_length + 2)

        writer.close()
        logger.info(f"Excel file saved as {output_filename}")
    except Exception as e:
        logger.error(f"Error saving Excel file: {str(e)}")
        st.error(f"Failed to save Excel file: {str(e)}")
        st.stop()

    with st.container():
        if show_table_overview:
            st.header("Overview of Converted Table (JSON to Excel)")
            st.write(f"Below is the table generated from the uploaded JSON file for {report_date.strftime('%B %d, %Y')}:")
            st.dataframe(df)

    with st.container():
        try:
            with open(output_filename, 'rb') as f:
                st.download_button(
                    label="Download Excel File",
                    data=f,
                    file_name=f'daily_completion_report_{selected_date.strftime("%Y-%m-%d")}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
        except Exception as e:
            logger.error(f"Error providing Excel file for download: {str(e)}")
            st.error(f"Failed to provide Excel file for download: {str(e)}")

    set1_colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF', '#999999']
    display_analysis(df, f"Daily Report ({report_date.strftime('%B %d, %Y')})", set1_colors)

    try:
        os.remove(output_filename)
        logger.info(f"Cleaned up temporary file: {output_filename}")
    except Exception as e:
        logger.warning(f"Could not delete temporary file {output_filename}: {str(e)}")

elif report_type == "Monthly Report":
    with st.container():
        default_start = current_date.replace(day=1)
        default_end = current_date
        date_range = st.date_input("Select Date Range for Monthly Report",
                                   value=(default_start, default_end),
                                   min_value=date(2000, 1, 1),
                                   max_value=current_date)

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.error("Please select a valid date range.")
        st.stop()

    if start_date > end_date:
        st.error("Start date must be before or equal to the end date.")
        st.stop()
    if start_date > current_date or end_date > current_date:
        st.error(f"Dates cannot be after {current_date}.")
        st.stop()

    with st.container():
        st.markdown(f"### Monthly Report from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}", unsafe_allow_html=True)

    processed_data = process_data(data, start_date, end_date)
    if not processed_data:
        st.error(f"No relevant tasks found for the period from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}.")
        st.stop()

    df = pd.DataFrame(processed_data)

    column_order = [
        "Employee Name",
        "Employee Code",
        "Department Name",
        "Department Head",
        "Task Identifier",
        "Task Status",
        "Tasks Completed",
        "Completed Task URLs",
        "Incomplete Tasks",
        "Incomplete Task URLs",
        "Due Date",
        "Rules Violated",
        "Rules Violated URLs",
        "Violation Type",
        "Estimated Time",
        "Reported Time",
        "Comments",
        "Remarks"
    ]

    df = df[column_order]

    departments = ["All"] + sorted(list(space_department_map.values()))
    selected_department = st.sidebar.selectbox("Filter by Department", departments)
    if selected_department != "All":
        df = df[df['Department Name'] == selected_department]

    with st.container():
        employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
        selected_employee = st.selectbox("Filter by Employee (Global)", employees)
        if selected_employee != "All":
            df = df[df['Employee Name'].str.contains(selected_employee, na=False)]

    output_filename = os.path.join(tempfile.gettempdir(), f'monthly_completion_report_{start_date.strftime("%Y-%m-%d")}_to_{end_date.strftime("%Y-%m-%d")}.xlsx')
    try:
        writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Report', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Report']
        for col_num, col_name in enumerate(column_order):
            max_length = max(df[col_name].astype(str).map(len).max(), len(col_name))
            worksheet.set_column(col_num, col_num, max_length + 2)

        writer.close()
        logger.info(f"Excel file saved as {output_filename}")
    except Exception as e:
        logger.error(f"Error saving Excel file: {str(e)}")
        st.error(f"Failed to save Excel file: {str(e)}")
        st.stop()

    with st.container():
        if show_table_overview:
            st.header("Overview of Converted Table (JSON to Excel)")
            st.write(f"Below is the table generated from the uploaded JSON file for the period from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}:")
            st.dataframe(df)

    with st.container():
        try:
            with open(output_filename, 'rb') as f:
                st.download_button(
                    label="Download Excel File",
                    data=f,
                    file_name=f'monthly_completion_report_{start_date.strftime("%Y-%m-%d")}_to_{end_date.strftime("%Y-%m-%d")}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
        except Exception as e:
            logger.error(f"Error providing Excel file for download: {str(e)}")
            st.error(f"Failed to provide Excel file for download: {str(e)}")

    set1_colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF', '#999999']
    display_analysis(df, f"Monthly Report ({start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')})", set1_colors)

    try:
        os.remove(output_filename)
        logger.info(f"Cleaned up temporary file: {output_filename}")
    except Exception as e:
        logger.warning(f"Could not delete temporary file {output_filename}: {str(e)}")

elif report_type == "Hourly Employee Monitoring":
    processed_data = process_hourly_data(data)
    if not processed_data:
        st.error("No relevant tasks found to process.")
        st.stop()

    df = pd.DataFrame(processed_data)

    current_hour = current_datetime.hour
    selected_hour = st.sidebar.selectbox("Select Hour (24h)", list(range(24)), index=current_hour)

    st.markdown(f"### Hourly Employee Monitoring for {selected_hour}:00", unsafe_allow_html=True)

    for department in sorted(list(space_department_map.values())):
        dept_df = df[df['Department Name'] == department]
        with st.container():
            st.markdown(f'<div class="dept-container"><h3>{department} (Head: {department_heads_mapping.get(department, "N/A")})</h3>', unsafe_allow_html=True)
            if not dept_df.empty:
                for index, row in dept_df.iterrows():
                    st.markdown(f'''
                        <div class="employee-card">
                            <h4>{row["Employee Name"]} (Code: {row["Employee Code"] if row["Employee Code"] is not None else "N/A"})</h4>
                            <p><strong>Department:</strong> {row["Department Name"]}</p>
                            <p><strong>Department Head:</strong> {row["Department Head"]}</p>
                            <p><strong>Current Work:</strong> {row["Current Work"]}</p>
                            <p><strong>Last Status:</strong> {row["Last Status"]}</p>
                            <p><strong>Last Updated:</strong> {row["Last Updated"]}</p>
                            <p><strong>Comment:</strong> {row["Comment"]}</p>
                        </div>
                    ''', unsafe_allow_html=True)
            else:
                st.write("No tasks found for this department.")
            st.markdown('</div>', unsafe_allow_html=True)

    output_filename = os.path.join(tempfile.gettempdir(), f'hourly_monitoring_report_{current_datetime.strftime("%Y-%m-%d_%H")}.xlsx')
    try:
        writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Hourly Monitoring', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Hourly Monitoring']
        for col_num, col_name in enumerate(df.columns):
            max_length = max(df[col_name].astype(str).map(len).max(), len(col_name))
            worksheet.set_column(col_num, col_num, max_length + 2)
        writer.close()
        logger.info(f"Excel file saved as {output_filename}")
    except Exception as e:
        logger.error(f"Error saving Excel file: {str(e)}")
        st.error(f"Failed to save Excel file: {str(e)}")
        st.stop()

    with st.container():
        try:
            with open(output_filename, 'rb') as f:
                st.download_button(
                    label="Download Excel File",
                    data=f,
                    file_name=f'hourly_monitoring_report_{current_datetime.strftime("%Y-%m-%d_%H")}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
        except Exception as e:
            logger.error(f"Error providing Excel file for download: {str(e)}")
            st.error(f"Failed to provide Excel file for download: {str(e)}")

    try:
        os.remove(output_filename)
        logger.info(f"Cleaned up temporary file: {output_filename}")
    except Exception as e:
        logger.warning(f"Could not delete temporary file {output_filename}: {str(e)}")

elif report_type == "Status Report":
    with st.container():
        st.subheader("Upload JSON Files")
        morning_file = st.file_uploader("Upload Morning JSON File (Required)", type=["json"], key="morning")
        evening_file = st.file_uploader("Upload Evening JSON File (Optional)", type=["json"], key="evening")

    if morning_file is None:
        st.warning("Please upload at least the morning JSON file to proceed.")
        st.stop()

    try:
        morning_data = json.load(morning_file)
        if not isinstance(morning_data, list):
            raise ValueError("Morning JSON file must contain a list of task objects")
        evening_data = None
        if evening_file:
            evening_data = json.load(evening_file)
            if not isinstance(evening_data, list):
                raise ValueError("Evening JSON file must contain a list of task objects")
    except Exception as e:
        logger.error(f"Error reading JSON file: {str(e)}")
        st.error(f"Failed to read the JSON file: {str(e)}")
        st.stop()

    with st.container():
        selected_date = st.date_input("Select Report Date", value=current_date, min_value=date(2000, 1, 1), max_value=current_date)

    if selected_date > current_date:
        st.error(f"Invalid date selected. Please choose a date on or before {current_date}.")
        st.stop()

    bangladesh_tz = pytz.timezone('Asia/Dhaka')
    report_date = datetime(selected_date.year, selected_date.month, selected_date.day, tzinfo=bangladesh_tz)
    start_of_day = report_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = report_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    with st.container():
        st.markdown(f"### Status Report for {report_date.strftime('%B %d, %Y')}", unsafe_allow_html=True)

    # Process morning and evening data
    morning_processed_data = process_data(morning_data, selected_date, selected_date)
    morning_df = pd.DataFrame(morning_processed_data) if morning_processed_data else pd.DataFrame()

    evening_processed_data = []
    if evening_data:
        evening_processed_data = process_data(evening_data, selected_date, selected_date)
    evening_df = pd.DataFrame(evening_processed_data) if evening_data else pd.DataFrame()

    # Check for employees with no tasks
    no_work_df = check_no_work_assigned(morning_data)

    # Create a DataFrame with all departments
    all_departments = pd.DataFrame({
        'Department': list(space_department_map.values()),
        'Department Head': [department_heads_mapping.get(dept, 'N/A') for dept in space_department_map.values()]
    })

    # Merge with morning_df to include departments with tasks
    if not morning_df.empty:
        morning_df['Due Date'] = pd.to_datetime(morning_df['Due Date'], errors='coerce').dt.date
        morning_df = morning_df[morning_df['Due Date'] <= current_date]
        morning_dept_counts = morning_df.groupby('Department Name').size().reset_index(name='Task Count')
        all_departments = all_departments.merge(morning_dept_counts, left_on='Department', right_on='Department Name', how='left')
    else:
        all_departments['Task Count'] = 0
        all_departments['Department Name'] = all_departments['Department']

    # Display employees with no tasks together in a single table
    if not no_work_df.empty:
        st.subheader("Employees with No Tasks Assigned/Created")
        st.dataframe(no_work_df)

    # Sidebar filters
    task_status_options = ["All"] + (sorted(morning_df['Task Status'].unique()) if not morning_df.empty else [])
    selected_status = st.selectbox("Filter by Task Status", task_status_options)
    departments = ["All"] + sorted(list(space_department_map.values()))
    selected_department = st.sidebar.selectbox("Filter by Department", departments)
    employees = ["All"] + (sorted(morning_df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique()) if not morning_df.empty else [])
    selected_employee = st.selectbox("Filter by Employee (Global)", employees)

    # Display morning report by department
    st.header("Morning Report")
    morning_df_filtered = morning_df.copy()
    if selected_status != "All":
        morning_df_filtered = morning_df_filtered[morning_df_filtered['Task Status'] == selected_status]
    if selected_department != "All":
        morning_df_filtered = morning_df_filtered[morning_df_filtered['Department Name'] == selected_department]
    if selected_employee != "All":
        morning_df_filtered = morning_df_filtered[morning_df_filtered['Employee Name'].str.contains(selected_employee, na=False)]

    for _, dept_row in all_departments.iterrows():
        dept = dept_row['Department']
        dept_head = dept_row['Department Head']
        task_count = dept_row['Task Count'] if pd.notnull(dept_row['Task Count']) else 0
        header_text = f"{dept} (Head: {dept_head})" if task_count > 0 else f"{dept} (Head: {dept_head}) (No work assigned/created yet)"
        
        with st.container():
            st.markdown(f'<div class="dept-container"><h3>{header_text}</h3>', unsafe_allow_html=True)
            dept_tasks = morning_df_filtered[morning_df_filtered['Department Name'] == dept][['Employee Name', 'Task Status', 'Task Title', 'Task Identifier', 'Due Date', 'Comment', 'Remarks']]
            if not dept_tasks.empty:
                st.dataframe(dept_tasks)
            else:
                st.write("No tasks found for this department.")
            st.markdown('</div>', unsafe_allow_html=True)

    # Display evening report by department if available
    if not evening_df.empty:
        st.subheader("Evening Report")
        evening_df['Due Date'] = pd.to_datetime(evening_df['Due Date'], errors='coerce').dt.date
        evening_df = evening_df[evening_df['Due Date'] <= current_date]
        evening_df_filtered = evening_df.copy()
        if selected_status != "All":
            evening_df_filtered = evening_df_filtered[evening_df_filtered['Task Status'] == selected_status]
        if selected_department != "All":
            evening_df_filtered = evening_df_filtered[evening_df_filtered['Department Name'] == selected_department]
        if selected_employee != "All":
            evening_df_filtered = evening_df_filtered[evening_df_filtered['Employee Name'].str.contains(selected_employee, na=False)]

        evening_dept_counts = evening_df_filtered.groupby('Department Name').size().reset_index(name='Task Count') if not evening_df_filtered.empty else pd.DataFrame()
        all_departments_evening = all_departments[['Department', 'Department Head']].merge(evening_dept_counts, left_on='Department', right_on='Department Name', how='left')
        all_departments_evening['Task Count'] = all_departments_evening['Task Count'].fillna(0)
        
        for _, dept_row in all_departments_evening.iterrows():
            dept = dept_row['Department']
            dept_head = dept_row['Department Head']
            task_count = dept_row['Task Count']
            header_text = f"{dept} (Head: {dept_head})" if task_count > 0 else f"{dept} (Head: {dept_head}) (No work assigned/created yet)"
            
            with st.container():
                st.markdown(f'<div class="dept-container"><h3>{header_text}</h3>', unsafe_allow_html=True)
                dept_tasks = evening_df_filtered[evening_df_filtered['Department Name'] == dept][['Employee Name', 'Task Status', 'Task Title', 'Task Identifier', 'Due Date', 'Comment', 'Remarks']]
                if not dept_tasks.empty:
                    st.dataframe(dept_tasks)
                else:
                    st.write("No tasks found for this department.")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No evening report uploaded.")

    # Process status update (morning only or morning vs evening)
    if evening_df.empty:
        required_columns = [
            "Department Name",
            "Department Head",
            "Employee Name",
            "Task Status",
            "Task Title",
            "Task Identifier",
            "Due Date",
            "Comment",
            "Remarks"
        ]

        if not morning_df.empty:
            missing_columns = [col for col in required_columns if col not in morning_df.columns]
            if missing_columns:
                st.error(f"Missing required columns in the morning DataFrame: {missing_columns}")
                st.stop()

            df_selected = morning_df[required_columns]
        else:
            df_selected = pd.DataFrame(columns=required_columns)

        grouped_df = df_selected.groupby('Department Name').apply(lambda x: x.assign(SL=range(1, len(x) + 1))).reset_index(drop=True)
        grouped_df = grouped_df.rename(columns={
            "Department Name": "Department",
            "Employee Name": "Assignee",
            "Task Status": "Status"
        })

        final_columns = [
            "SL",
            "Department",
            "Department Head",
            "Assignee",
            "Status",
            "Task Title",
            "Task Identifier",
            "Due Date",
            "Comment",
            "Remarks"
        ]

        grouped_df = grouped_df[final_columns]

        # Apply filters
        grouped_df_filtered = grouped_df.copy()
        if selected_status != "All":
            grouped_df_filtered = grouped_df_filtered[grouped_df_filtered['Status'] == selected_status]
        if selected_department != "All":
            grouped_df_filtered = grouped_df_filtered[grouped_df_filtered['Department'] == selected_department]
        if selected_employee != "All":
            grouped_df_filtered = grouped_df_filtered[grouped_df_filtered['Assignee'].str.contains(selected_employee, na=False)]

        with st.container():
            if show_table_overview:
                st.header("Morning Status Overview")
                st.write(f"Below is the table generated from the morning JSON file for {report_date.strftime('%B %d, %Y')}:")
                st.dataframe(grouped_df_filtered)

        output_filename = os.path.join(tempfile.gettempdir(), f'status_report_{selected_date.strftime("%Y-%m-%d")}.xlsx')
        try:
            writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
            grouped_df_filtered.to_excel(writer, sheet_name='Morning Report', index=False)

            if not no_work_df.empty:
                no_work_df.to_excel(writer, sheet_name='No Work Assigned', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Morning Report']
            for col_num, col_name in enumerate(final_columns):
                max_length = max(grouped_df_filtered[col_name].astype(str).map(len).max(), len(col_name))
                worksheet.set_column(col_num, col_num, max_length + 2)
            if not no_work_df.empty:
                worksheet_no_work = writer.sheets['No Work Assigned']
                for col_num, col_name in enumerate(no_work_df.columns):
                    max_length = max(no_work_df[col_name].astype(str).map(len).max(), len(col_name))
                    worksheet_no_work.set_column(col_num, col_num, max_length + 2)
            writer.close()
            logger.info(f"Excel file saved as {output_filename}")
        except Exception as e:
            logger.error(f"Error saving Excel file: {str(e)}")
            st.error(f"Failed to save Excel file: {str(e)}")
            st.stop()

        with st.container():
            try:
                with open(output_filename, 'rb') as f:
                    st.download_button(
                        label="Download Excel File",
                        data=f,
                        file_name=f'status_report_{selected_date.strftime("%Y-%m-%d")}.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
            except Exception as e:
                logger.error(f"Error providing Excel file for download: {str(e)}")
                st.error(f"Failed to provide Excel file for download: {str(e)}")

        try:
            os.remove(output_filename)
            logger.info(f"Cleaned up temporary file: {output_filename}")
        except Exception as e:
            logger.warning(f"Could not delete temporary file {output_filename}: {str(e)}")
    else:
        merged_df = pd.merge(
            morning_df[['Task Identifier', 'Employee Name', 'Task Status', 'Due Date', 'Task Title', 'Comment', 'Remarks']],
            evening_df[['Task Identifier', 'Task Status', 'Due Date', 'Task Title', 'Comment', 'Remarks']],
            on='Task Identifier',
            how='outer',
            suffixes=('_morning', '_evening')
        )

        merged_df['Employee Name'] = merged_df['Employee Name'].fillna(morning_df['Employee Name'])
        merged_df['Task Status_morning'] = merged_df['Task Status_morning'].fillna('Not Updated')
        merged_df['Task Status_evening'] = merged_df['Task Status_evening'].fillna('Not Updated')
        merged_df['Due Date_morning'] = pd.to_datetime(merged_df['Due Date_morning'], errors='coerce').dt.date
        merged_df['Due Date_evening'] = pd.to_datetime(merged_df['Due Date_evening'], errors='coerce').dt.date
        merged_df['Due Date'] = merged_df['Due Date_morning'].combine_first(merged_df['Due Date_evening'])
        merged_df['Task Title'] = merged_df['Task Title_morning'].combine_first(merged_df['Task Title_evening'])
        merged_df['Comment_morning'] = merged_df['Comment_morning'].fillna('No Comment')
        merged_df['Comment_evening'] = merged_df['Comment_evening'].fillna('No Comment')
        merged_df['Comment'] = merged_df['Comment_evening'].combine_first(merged_df['Comment_morning'])
        merged_df['Remarks'] = merged_df['Remarks_morning'].combine_first(merged_df['Remarks_evening'])

        required_columns = [
            "Employee Name",
            "Task Status_morning",
            "Task Status_evening",
            "Task Title",
            "Task Identifier",
            "Due Date",
            "Comment_morning",
            "Comment_evening",
            "Remarks"
        ]

        missing_columns = [col for col in required_columns if col not in merged_df.columns]
        if missing_columns:
            st.error(f"Missing required columns in the merged DataFrame: {missing_columns}")
            st.stop()

        merged_df = merged_df[required_columns]

        # Apply filters
        merged_df_filtered = merged_df.copy()
        if selected_status != "All":
            merged_df_filtered = merged_df_filtered[merged_df_filtered['Task Status_evening'] == selected_status]
        if selected_department != "All":
            merged_df_filtered = merged_df_filtered[merged_df_filtered['Employee Name'].map(lambda x: employee_department_map.get(x.split(' [Rule Violator]')[0], 'Unknown')) == selected_department]
        if selected_employee != "All":
            merged_df_filtered = merged_df_filtered[merged_df_filtered['Employee Name'].str.contains(selected_employee, na=False)]

        grouped_df = merged_df_filtered.groupby('Employee Name').apply(lambda x: x.assign(SL=range(1, len(x) + 1))).reset_index(drop=True)

        with st.container():
            if show_table_overview:
                st.header("Status Update Overview")
                st.write(f"Below is the status update comparison for {report_date.strftime('%B %d, %Y')}:")
                st.dataframe(grouped_df)

        output_filename = os.path.join(tempfile.gettempdir(), f'status_report_{selected_date.strftime("%Y-%m-%d")}.xlsx')
        try:
            writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
            grouped_df.to_excel(writer, sheet_name='Status Update', index=False)
            if not no_work_df.empty:
                no_work_df.to_excel(writer, sheet_name='No Work Assigned', index=False)
            workbook = writer.book
            worksheet1 = writer.sheets['Status Update']
            for col_num, col_name in enumerate(grouped_df.columns):
                max_length = max(grouped_df[col_name].astype(str).map(len).max(), len(col_name))
                worksheet1.set_column(col_num, col_num, max_length + 2)
            if not no_work_df.empty:
                worksheet3 = writer.sheets['No Work Assigned']
                for col_num, col_name in enumerate(no_work_df.columns):
                    max_length = max(no_work_df[col_name].astype(str).map(len).max(), len(col_name))
                    worksheet3.set_column(col_num, col_num, max_length + 2)
            writer.close()
            logger.info(f"Excel file saved as {output_filename}")
        except Exception as e:
            logger.error(f"Error saving Excel file: {str(e)}")
            st.error(f"Failed to save Excel file: {str(e)}")
            st.stop()

        with st.container():
            try:
                with open(output_filename, 'rb') as f:
                    st.download_button(
                        label="Download Excel File",
                        data=f,
                        file_name=f'status_report_{selected_date.strftime("%Y-%m-%d")}.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
            except Exception as e:
                logger.error(f"Error providing Excel file for download: {str(e)}")
                st.error(f"Failed to provide Excel file for download: {str(e)}")

        try:
            os.remove(output_filename)
            logger.info(f"Cleaned up temporary file: {output_filename}")
        except Exception as e:
            logger.warning(f"Could not delete temporary file {output_filename}: {str(e)}")