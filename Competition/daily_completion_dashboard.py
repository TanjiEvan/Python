import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import pytz
import xlsxwriter
import logging
import os
import tempfile

# Set up logging to help debug issues
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Custom CSS for a professional look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }
    .main {
        background-color: #1e1e2f;
        color: #ffffff;
    }
    .stApp {
        background-color: #1e1e2f;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    .stMarkdown, .stDataFrame {
        color: #d1d1d1;
    }
    .overview-card {
        background-color: #2a2a3d;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        text-align: center;
        color: #ffffff;
    }
    .overview-card h3 {
        margin: 0;
        font-size: 1.2em;
        color: #a3bffa;
    }
    .overview-card p {
        margin: 10px 0 0;
        font-size: 1.5em;
        font-weight: bold;
    }
    .stSelectbox, .stDateInput, .stFileUploader, .stCheckbox, .stButton {
        background-color: #2a2a3d !important;
        border-radius: 5px;
        color: #ffffff !important;
    }
    .stSelectbox > div > div, .stDateInput > div > div, .stFileUploader > div > div {
        background-color: #2a2a3d !important;
        color: #ffffff !important;
    }
    .stButton > button {
        background-color: #6366f1;
        color: #ffffff;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #818cf8;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app title
st.title("Daily Completion Report Dashboard")

# Sidebar for additional filters
st.sidebar.header("Filter Options")
show_table_overview = st.sidebar.checkbox("Show Table Overview", value=True)

# Current date for validation (April 30, 2025)
current_date = date(2025, 4, 30)

# Date picker for selecting the report date
selected_date = st.date_input("Select Report Date", value=current_date, min_value=date(2000, 1, 1), max_value=current_date)

# Validate the selected date
if selected_date > current_date:
    st.error(f"Invalid date selected. Please choose a date on or before {current_date}.")
    st.stop()

# Format the selected date for the report
bangladesh_tz = pytz.timezone('Asia/Dhaka')
report_date = datetime(selected_date.year, selected_date.month, selected_date.day, tzinfo=bangladesh_tz)
start_of_day = report_date.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_day = report_date.replace(hour=23, minute=59, second=59, microsecond=999999)

# Update the title with the selected date
st.markdown(f"### Report for {report_date.strftime('%B %d, %Y')}")

# File uploader for the JSON file
uploaded_file = st.file_uploader("Upload the JSON File", type=["json"])

if uploaded_file is not None:
    try:
        # Read the JSON file
        logger.info("Reading the uploaded JSON file")
        data = json.load(uploaded_file)

        # Component-to-Department Mapping
        component_department_map = {
            "67baee6d35e2055277c6f7aa": "Creative Marketing",
            "67bab60de8bc928dabdd8397": "Creative Marketing",
            "67bab5bde8bc928dabdd776b": "Creative Marketing",
            "67bab7f9e8bc928dabdda4c7": "Creative Marketing",
            "67baba7ae8bc928dabddc3f5": "Creative Marketing",
            "67bab546e8bc928dabdd6b57": "Creative Marketing",
            "67baba0be8bc928dabddb8a8": "Creative Marketing",
            "67bab775e8bc928dabdd9a30": "Creative Marketing",
            "67bc22dfea1f4ffdf6dfe6d5": "Creative Marketing",
            "67bab3f6e8bc928dabdd5466": "Creative Marketing",
            "67bab2dde8bc928dabdd48ba": "Creative Marketing",
            "67baba81e8bc928dabddc55a": "HR, Admin, Finance & Accounts",
            "67baee7535e2055277c6f8e7": "HR, Admin, Finance & Accounts",
            "67baba0fe8bc928dabddba15": "HR, Admin, Finance & Accounts",
            "67bab305e8bc928dabdd4a43": "HR, Admin, Finance & Accounts",
            "67bc22edea1f4ffdf6dfe81c": "HR, Admin, Finance & Accounts",
            "67bab77ce8bc928dabdd9b95": "HR, Admin, Finance & Accounts",
            "67bab550e8bc928dabdd6cbc": "HR, Admin, Finance & Accounts",
            "67bab7fce8bc928dabdda634": "HR, Admin, Finance & Accounts",
            "67bab5c1e8bc928dabdd78d0": "HR, Admin, Finance & Accounts",
            "67bab613e8bc928dabdd83a0": "HR, Admin, Finance & Accounts",
            "67bab3fbe8bc928dabdd55cb": "HR, Admin, Finance & Accounts",
            "67baee7d35e2055277c6fa1c": "Network, IT and Internal Support",
            "67bab559e8bc928dabdd6e21": "Network, IT and Internal Support",
            "67bab619e8bc928dabdd85b9": "Network, IT and Internal Support",
            "67baba89e8bc928dabddc6bf": "Network, IT and Internal Support",
            "67bc22f9ea1f4ffdf6dfe965": "Network, IT and Internal Support",
            "67bab5c8e8bc928dabdd7a35": "Network, IT and Internal Support",
            "67bab809e8bc928dabdda799": "Network, IT and Internal Support",
            "67bab786e8bc928dabdd9cfa": "Network, IT and Internal Support",
            "67bab30fe8bc928dabdd4ba8": "Network, IT and Internal Support",
            "67b9af251a20cc50f3b630cb": "Network, IT and Internal Support",
            "67baba17e8bc928dabddbb7a": "Network, IT and Internal Support",
            "67bab78ce8bc928dabdd9db5": "Operations & Support",
            "67bab81ce8bc928dabdda8fe": "Operations & Support",
            "67bab410e8bc928dabdd57eb": "Operations & Support",
            "67bc2312ea1f4ffdf6dfeac2": "Operations & Support",
            "67bab562e8bc928dabdd6f86": "Operations & Support",
            "67baee8635e2055277c6fb51": "Operations & Support",
            "67bab5cfe8bc928dabdd7b9a": "Operations & Support",
            "67baba90e8bc928dabddc824": "Operations & Support",
            "67bab31ae8bc928dabdd4d0d": "Operations & Support",
            "67bab620e8bc928dabdd871e": "Operations & Support",
            "67baba25e8bc928dabddbcdf": "Operations & Support",
            "67baee9135e2055277c6fc86": "Production & Media",
            "67bab56de8bc928dabdd70eb": "Production & Media",
            "67bab41be8bc928dabdd5950": "Production & Media",
            "67bab626e8bc928dabdd8883": "Production & Media",
            "67bab823e8bc928dabddaa63": "Production & Media",
            "67babaa2e8bc928dabddc98e": "Production & Media",
            "67bab326e8bc928dabdd4e72": "Production & Media",
            "67bab793e8bc928dabdd9f1a": "Production & Media",
            "67baba2ee8bc928dabddbe44": "Production & Media",
            "67bc231aea1f4ffdf6dfec23": "Production & Media",
            "67bc2326ea1f4ffdf6dfece8": "Retail & Business",
            "67bab57be8bc928dabdd7250": "Retail & Business",
            "67bab799e8bc928dabdda07f": "Retail & Business",
            "67bab5dbe8bc928dabdd7e64": "Retail & Business",
            "67baba48e8bc928dabddbfa9": "Retail & Business",
            "67bab335e8bc928dabdd4fd7": "Retail & Business",
            "67babaace8bc928dabddcaf3": "Retail & Business",
            "67baeeba35e2055277c6fdbb": "Retail & Business",
            "67bab42ce8bc928dabdd5ab5": "Retail & Business",
            "67bab87ae8bc928dabddabc8": "Retail & Business",
            "67bab62de8bc928dabdd89e8": "Retail & Business",
            "67baba51e8bc928dabddc10e": "Software Development",
            "67bab7a1e8bc928dabdda1e4": "Software Development",
            "67baeec235e2055277c6fef0": "Software Development",
            "67bab375e8bc928dabdd513c": "Software Development",
            "67babab4e8bc928dabddcc58": "Software Development",
            "67bab5e1e8bc928dabdd7fc9": "Software Development",
            "67bab581e8bc928dabdd73b5": "Software Development",
            "67bc2335ea1f4ffdf6dfee5b": "Software Development",
            "67bab882e8bc928dabddad2d": "Software Development",
            "67bab648e8bc928dabdd8b4d": "Software Development",
            "67bab44be8bc928dabdd5c1a": "Software Development"
        }

        # Department heads mapping
        department_heads_mapping = {
            "Network, IT and Internal Support": "Fahim Hasan Shah",
            "Operations & Support": "Md. Arman Al Sharif",
            "HR, Admin, Finance & Accounts": "Md. Sohel Rana",
            "Software Development": "Tanvir Islam",
            "Production & Media": "Md. Shezan Mahmud Tomal, Shariar Hossen",
            "Creative Marketing": "Sunnyat Ali",
            "Retail & Business": "Sunnyat Ali"
        }

        # Process tasks for the selected date
        processed_data = []
        for item in data:
            try:
                # Get timestamps and convert to Bangladesh time
                modified_on_ts = item.get("modifiedOn")
                created_on_ts = item.get("createdOn")
                due_date_ts = item.get("dueDate")
                modified_on_dt = datetime.fromtimestamp(modified_on_ts / 1000, pytz.utc).astimezone(bangladesh_tz) if modified_on_ts else None
                created_on_dt = datetime.fromtimestamp(created_on_ts / 1000, pytz.utc).astimezone(bangladesh_tz) if created_on_ts else None
                due_date_dt = datetime.fromtimestamp(due_date_ts / 1000, pytz.utc).astimezone(bangladesh_tz) if due_date_ts else None

                # Filter tasks relevant to the selected date
                is_relevant = False
                if (modified_on_dt and start_of_day <= modified_on_dt <= end_of_day) or (created_on_dt and start_of_day <= created_on_dt <= end_of_day):
                    is_relevant = True
                elif due_date_dt and due_date_dt <= end_of_day and item.get("status") != "DONE":
                    is_relevant = True

                if not is_relevant:
                    continue

                # Get basic task info
                employee_raw = item.get("assignee", "Unassigned")
                if employee_raw != "Unassigned" and "," in employee_raw:
                    last_name, first_name = employee_raw.split(",", 1)
                    employee = f"{first_name.strip()} {last_name.strip()}"
                else:
                    employee = employee_raw

                component_id = item.get("component")
                department = component_department_map.get(component_id, "Unknown")
                department_head = department_heads_mapping.get(department, "N/A")
                raw_status = item.get("status", "Unknown")
                task_title = item.get("title", "No Title")
                task_identifier = item.get("identifier", "No ID")

                # Use the raw status directly
                status = raw_status
                is_completed = raw_status == "DONE"
                is_incomplete = due_date_dt and due_date_dt <= end_of_day and not is_completed
                is_not_due_yet = due_date_dt and due_date_dt > end_of_day and not is_completed

                # Adjust status based on due date
                if is_completed:
                    if due_date_dt:
                        modified_on_date = modified_on_dt.date() if modified_on_dt else None
                        due_date_date = due_date_dt.date() if due_date_dt else None
                        if modified_on_date <= due_date_date:
                            status = "DONE(On Time)"
                        else:
                            status = "DONE(Late)"
                    else:
                        status = "DONE(No Due Date)"
                elif is_incomplete:
                    status = "Incomplete"
                elif is_not_due_yet:
                    status = "In Progress(not due yet)"
                elif not due_date_dt:
                    status = f"{status}(No Due Date)"

                # Construct URL for tasks
                task_url = f"https://huly.app/workbench/sohub/tracker/{task_identifier}"

                # Determine completed and incomplete tasks
                completed_tasks = task_title if is_completed else ""
                completed_task_urls = task_url if is_completed else ""
                incomplete_tasks = task_title if is_incomplete else ""
                incomplete_task_urls = task_url if is_incomplete else ""

                # Check for rules violation and determine violation type
                rules_violated = "No"
                rules_violated_urls = ""
                violation_type = ""
                if not component_id or department == "Unknown":
                    rules_violated = "Yes"
                    rules_violated_urls = task_url
                    violation_type = "Missing Component"
                elif due_date_dt is None:
                    rules_violated = "Yes"
                    rules_violated_urls = task_url
                    violation_type = "Missing Due Date"

                # Append "[Rule Violator]" to employee name if rules are violated
                if rules_violated == "Yes":
                    employee = f"{employee} [Rule Violator]"

                # Add to processed data
                processed_data.append({
                    "Employee Name": employee,
                    "Department Name": department,
                    "Department Head": department_head,
                    "Task Identifier": task_identifier,
                    "Task Status": status,
                    "Tasks Completed": completed_tasks,
                    "Completed Task URLs": completed_task_urls,
                    "Incomplete Tasks": incomplete_tasks,
                    "Incomplete Task URLs": incomplete_task_urls,
                    "Due Date": due_date_dt.strftime('%Y-%m-%d') if due_date_dt else "",
                    "Rules Violated": rules_violated,
                    "Rules Violated URLs": rules_violated_urls,
                    "Violation Type": violation_type
                })
            except Exception as e:
                logger.error(f"Error processing task: {item}. Error: {str(e)}")
                continue

        if not processed_data:
            st.error(f"No relevant tasks found in the JSON file for {report_date.strftime('%B %d, %Y')}.")
            st.stop()

        # Create DataFrame
        df = pd.DataFrame(processed_data)

        # Define column order
        column_order = [
            "Employee Name",
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
            "Violation Type"
        ]

        # Reorder DataFrame
        df = df[column_order]

        # Apply filters
        # Department filter in sidebar
        departments = ["All"] + sorted(df['Department Name'].unique())
        selected_department = st.sidebar.selectbox("Filter by Department", departments)
        if selected_department != "All":
            df = df[df['Department Name'] == selected_department]

        # Employee filter as a dropdown
        employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
        selected_employee = st.selectbox("Filter by Employee", employees)
        if selected_employee != "All":
            df = df[df['Employee Name'].str.contains(selected_employee, na=False)]

        # Quick Overview Dashboard
        st.header("Quick Overview")
        st.markdown("Get a quick snapshot of task performance metrics for the selected date.")

        # Calculate metrics
        total_tasks = df.shape[0]
        completed_tasks = df[df['Task Status'].str.startswith('DONE')].shape[0]
        incomplete_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        rule_violations_count = df[df['Rules Violated'] == 'Yes'].shape[0]

        # Display metrics in a card layout
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"""
                <div class="overview-card">
                    <h3>📋 Total Tasks</h3>
                    <p>{total_tasks}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="overview-card">
                    <h3>✅ Completed Tasks</h3>
                    <p>{completed_tasks}</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="overview-card">
                    <h3>⏳ Incomplete Tasks</h3>
                    <p>{incomplete_tasks}</p>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="overview-card">
                    <h3>📊 Completion Rate</h3>
                    <p>{completion_rate:.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
                <div class="overview-card">
                    <h3>⚠️ Rule Violations</h3>
                    <p>{rule_violations_count}</p>
                </div>
            """, unsafe_allow_html=True)

        # Export to Excel (use temporary directory)
        output_filename = os.path.join(tempfile.gettempdir(), f'daily_completion_report_{selected_date.strftime("%Y-%m-%d")}.xlsx')
        try:
            writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Report', index=False)

            # Adjust column widths for better readability
            workbook = writer.book
            worksheet = writer.sheets['Report']
            for col_num, col_name in enumerate(column_order):
                max_length = max(df[col_name].astype(str).map(len).max(), len(col_name))
                worksheet.set_column(col_num, col_num, max_length + 2)

            # Save the Excel file
            writer.close()
            logger.info(f"Excel file saved as {output_filename}")
        except Exception as e:
            logger.error(f"Error saving Excel file: {str(e)}")
            st.error(f"Failed to save Excel file: {str(e)}")
            st.stop()

        # Display the converted table overview if toggled on
        if show_table_overview:
            st.header("Overview of Converted Table (JSON to Excel)")
            st.write(f"Below is the table generated from the uploaded JSON file for {report_date.strftime('%B %d, %Y')}:")
            st.dataframe(df)

        # Provide download link for the Excel file
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

        # --- Analysis Section ---
        st.header("Analysis Dashboard")

        # --- Question 1: Overall Completion Rate with Task Status Breakdown ---
        st.subheader(f"Q1: What is the overall completion rate of tasks on {report_date.strftime('%B %d, %Y')}?")
        total_tasks = df.shape[0]
        completed_tasks = df[df['Task Status'].str.startswith('DONE')].shape[0]
        incomplete_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        incomplete_rate = (incomplete_tasks / total_tasks * 100) if total_tasks > 0 else 0

        st.write(f"Total Tasks: {total_tasks}")
        st.write(f"Completed Tasks: {completed_tasks} ({completion_rate:.2f}%)")
        st.write(f"Incomplete Tasks: {incomplete_tasks} ({incomplete_rate:.2f}%)")

        # Task Status breakdown
        task_status_counts = df['Task Status'].value_counts().reset_index()
        task_status_counts.columns = ['Task Status', 'Count']
        st.write("**Task Status Breakdown:**")
        st.write(task_status_counts)

        # Define Set1 color palette
        set1_colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF', '#999999']

        # Visualize: Pie chart for overall completion
        fig1 = go.Figure(data=[
            go.Pie(labels=['Completed', 'Incomplete'],
                   values=[completed_tasks, incomplete_tasks],
                   textinfo='label+percent',
                   marker=dict(colors=set1_colors[:2]))
        ])
        fig1.update_layout(title_text=f'Overall Task Completion Rate ({report_date.strftime("%B %d, %Y")})',
                           paper_bgcolor='#2a2a3d', plot_bgcolor='#2a2a3d', font=dict(color='#ffffff'))
        st.plotly_chart(fig1, use_container_width=True)

        # Visualize: Bar chart for task status breakdown
        fig1b = px.bar(task_status_counts, x='Task Status', y='Count',
                       title=f'Task Status Distribution ({report_date.strftime("%B %d, %Y")})',
                       labels={'Count': 'Number of Tasks'},
                       color='Task Status',
                       color_discrete_sequence=set1_colors)
        fig1b.update_layout(xaxis_title='Task Status', yaxis_title='Number of Tasks', xaxis_tickangle=-45, showlegend=False,
                            paper_bgcolor='#2a2a3d', plot_bgcolor='#2a2a3d', font=dict(color='#ffffff'))
        st.plotly_chart(fig1b, use_container_width=True)

        # --- Question 2: Task Completion Rate per Employee with Task Status Breakdown ---
        st.subheader(f"Q2: What is the task completion rate per employee on {report_date.strftime('%B %d, %Y')}?")
        employee_stats = df.groupby('Employee Name').agg({
            'Task Status': [
                lambda x: sum(x.str.startswith('DONE')),
                lambda x: sum(~x.str.startswith('DONE'))
            ]
        }).reset_index()
        employee_stats.columns = ['Employee Name', 'Tasks Completed', 'Incomplete Tasks']
        employee_stats['Employee Name'] = employee_stats['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True)
        employee_stats = employee_stats.groupby('Employee Name').sum().reset_index()
        employee_stats['Total Tasks'] = employee_stats['Tasks Completed'] + employee_stats['Incomplete Tasks']
        employee_stats['Completion Rate (%)'] = (employee_stats['Tasks Completed'] / employee_stats['Total Tasks'] * 100).round(2)

        # Task Status breakdown per employee
        employee_task_status = df.groupby(['Employee Name', 'Task Status']).size().unstack(fill_value=0).reset_index()
        employee_task_status['Employee Name'] = employee_task_status['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True)
        employee_task_status = employee_task_status.groupby('Employee Name').sum().reset_index()

        st.write("**Completion Rate per Employee:**")
        st.write(employee_stats[['Employee Name', 'Tasks Completed', 'Incomplete Tasks', 'Total Tasks', 'Completion Rate (%)']])
        st.write("**Task Status Breakdown per Employee:**")
        st.write(employee_task_status)

        # Visualize: Bar chart for completion rate per employee
        fig2 = px.bar(employee_stats, x='Employee Name', y='Completion Rate (%)',
                      title=f'Task Completion Rate per Employee ({report_date.strftime("%B %d, %Y")})',
                      labels={'Completion Rate (%)': 'Completion Rate (%)'},
                      color='Employee Name',
                      color_discrete_sequence=set1_colors)
        fig2.update_layout(xaxis_title='Employee Name', yaxis_title='Completion Rate (%)', xaxis_tickangle=-45, showlegend=False,
                           paper_bgcolor='#2a2a3d', plot_bgcolor='#2a2a3d', font=dict(color='#ffffff'))
        st.plotly_chart(fig2, use_container_width=True)

        # --- Question 3: Task Completion Rate per Department ---
        st.subheader(f"Q3: What is the task completion rate per department on {report_date.strftime('%B %d, %Y')}?")
        department_stats = df.groupby('Department Name').agg({
            'Task Status': [
                lambda x: sum(x.str.startswith('DONE')),
                lambda x: sum(~x.str.startswith('DONE'))
            ]
        }).reset_index()
        department_stats.columns = ['Department Name', 'Tasks Completed', 'Incomplete Tasks']
        department_stats['Total Tasks'] = department_stats['Tasks Completed'] + department_stats['Incomplete Tasks']
        department_stats['Completion Rate (%)'] = (department_stats['Tasks Completed'] / department_stats['Total Tasks'] * 100).round(2)

        st.write(department_stats[['Department Name', 'Tasks Completed', 'Incomplete Tasks', 'Total Tasks', 'Completion Rate (%)']])

        # Visualize: Bar chart
        fig3 = px.bar(department_stats, x='Department Name', y='Completion Rate (%)',
                      title=f'Task Completion Rate per Department ({report_date.strftime("%B %d, %Y")})',
                      labels={'Completion Rate (%)': 'Completion Rate (%)'},
                      color='Department Name',
                      color_discrete_sequence=set1_colors)
        fig3.update_layout(xaxis_title='Department Name', yaxis_title='Completion Rate (%)', xaxis_tickangle=-45, showlegend=False,
                           paper_bgcolor='#2a2a3d', plot_bgcolor='#2a2a3d', font=dict(color='#ffffff'))
        st.plotly_chart(fig3, use_container_width=True)

        # --- Question 4: Incomplete Tasks with Due Date ---
        st.subheader(f"Q4: Which incomplete tasks need attention, and what are their direct URLs for review on {report_date.strftime('%B %d, %Y')}?")
        incomplete_tasks_df = df[df['Incomplete Tasks'] != ''][['Employee Name', 'Department Name', 'Incomplete Tasks', 'Incomplete Task URLs', 'Due Date']]
        st.write(incomplete_tasks_df)

        # --- Question 5: Rule Violations per Employee with Task Identifier, URL, and Violation Type ---
        st.subheader(f"Q5: How many tasks violated rules, and who are the responsible employees on {report_date.strftime('%B %d, %Y')}?")
        rule_violations_df = df[df['Rules Violated'] == 'Yes'][['Employee Name', 'Task Identifier', 'Rules Violated URLs', 'Violation Type']]
        rule_violations_summary = rule_violations_df.groupby('Employee Name').size().reset_index(name='Rule Violations')

        if not rule_violations_df.empty:
            st.write("**Rule Violations Summary:**")
            st.write(rule_violations_summary)
            st.write("**Details of Rule Violations:**")
            st.write(rule_violations_df)
            # Visualize: Bar chart
            fig4 = px.bar(rule_violations_summary, x='Employee Name', y='Rule Violations',
                          title=f'Rule Violations per Employee ({report_date.strftime("%B %d, %Y")})',
                          labels={'Rule Violations': 'Number of Rule Violations'},
                          color='Employee Name',
                          color_discrete_sequence=set1_colors)
            fig4.update_layout(xaxis_title='Employee Name', yaxis_title='Number of Rule Violations', xaxis_tickangle=-45, showlegend=False,
                               paper_bgcolor='#2a2a3d', plot_bgcolor='#2a2a3d', font=dict(color='#ffffff'))
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.write("No rule violations found.")

        # --- Question 6: Completed Tasks with Due Date, Task Identifier, and URL ---
        st.subheader(f"Q6: Which tasks were completed, and what are their due dates, task identifiers, and URLs on {report_date.strftime('%B %d, %Y')}?")
        completed_tasks_df = df[df['Tasks Completed'] != ''][['Employee Name', 'Department Name', 'Tasks Completed', 'Task Identifier', 'Due Date', 'Completed Task URLs']]
        st.write(completed_tasks_df)

        # Clean up the temporary Excel file
        try:
            os.remove(output_filename)
            logger.info(f"Cleaned up temporary file: {output_filename}")
        except Exception as e:
            logger.warning(f"Could not delete temporary file {output_filename}: {str(e)}")

    except Exception as e:
        logger.error(f"Error processing JSON file: {str(e)}")
        st.error(f"Failed to process the JSON file: {str(e)}")