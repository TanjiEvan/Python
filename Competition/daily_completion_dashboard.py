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

# Set up logging to help debug issues
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Custom CSS for a dark ash/grey theme with vibrant fonts and improved container spacing
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
    /* Ensure proper spacing around all containers */
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
report_type = st.sidebar.radio("Select Report Type", ["Daily Report", "Monthly Report", "Hourly Employee Monitoring"], index=0)

# Sidebar for additional filters
st.sidebar.header("Filter Options")
st.sidebar.markdown("### Refine Your View")
show_table_overview = st.sidebar.checkbox("Show Table Overview", value=True)

# Current date for validation (May 18, 2025, 05:45 PM +06)
current_date = date(2025, 5, 18)

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
    "Sakib Shahriar": "Md. Sakib Shahriar"
}

# Employee code mapping dictionary (based on mapped names)
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
    "Md Redwanul Hasan": 10024,
    "Md. Asif Saharwar": 10027,
    "Towfiqur Rahman": 10028,
    "Md. Arman Al Sharif": 10006,
    "Badhon Kumar Roy": 10011,
    "Md. Muyed Moktadir Chowdhury": 10004,
    "Md. Shezan Mahmud": 20001,
    "Md. Nazim Mahmud": 20002,
    "Md. Sadik": 30001,
    "Md Ridwanul Islam": 30002
}

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
    "67bab404e8bc928dabdd5686": "Network, IT and Internal Support",
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
    "67baba25e8bc928dabddbe44": "Operations & Support",
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

# Department heads mapping (using mapped names)
department_heads_mapping = {
    "Network, IT and Internal Support": "Md. Fahim Hasan Shah",
    "Operations & Support": "Md. Arman Al Sharif",
    "HR, Admin, Finance & Accounts": "Md. Sohel Rana",
    "Software Development": "Tanvir Islam",
    "Production & Media": "Md. Shezan Mahmud, Md. Shariar Hossen",
    "Creative Marketing": "Sunnyat Ali",
    "Retail & Business": "Sunnyat Ali"
}

# File uploader for the JSON file
with st.container():
    uploaded_file = st.file_uploader("Upload the JSON File", type=["json"])

if uploaded_file is not None:
    try:
        # Read the JSON file
        logger.info("Reading the uploaded JSON file")
        data = json.load(uploaded_file)

        # Function to process data for reports
        def process_data(data, start_date, end_date):
            bangladesh_tz = pytz.timezone('Asia/Dhaka')
            start_of_period = datetime(start_date.year, start_date.month, start_date.day, tzinfo=bangladesh_tz)
            end_of_period = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59, 999999, tzinfo=bangladesh_tz)

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

                    # Filter tasks relevant to the selected period
                    is_relevant = False
                    if (modified_on_dt and start_of_period <= modified_on_dt <= end_of_period) or (created_on_dt and start_of_period <= created_on_dt <= end_of_period):
                        is_relevant = True
                    elif due_date_dt and due_date_dt <= end_of_period and item.get("status") != "DONE":
                        is_relevant = True

                    if not is_relevant:
                        continue

                    # Get basic task info
                    employee_raw = item.get("assignee", "Unassigned")
                    # Clean up the name by removing leading/trailing commas and spaces
                    employee_cleaned = employee_raw.strip(',').strip()
                    if employee_cleaned != "Unassigned" and "," in employee_cleaned:
                        last_name, first_name = employee_cleaned.split(",", 1)
                        employee = f"{first_name.strip()} {last_name.strip()}"
                    else:
                        employee = employee_cleaned

                    # Apply name mapping
                    mapped_employee = name_mapping.get(employee, employee)

                    component_id = item.get("component")
                    department = component_department_map.get(component_id, "Unknown")
                    department_head = department_heads_mapping.get(department, "N/A")
                    raw_status = item.get("status", "Unknown")
                    task_title = item.get("title", "No Title")
                    task_identifier = item.get("identifier", "No ID")
                    estimation = item.get("estimation", 0)
                    reported_time = item.get("reportedTime", 0)
                    comment = item.get("comment", "")

                    # Determine if comment exists
                    has_comment = "Yes" if comment and comment.strip() else "No"

                    # Use the raw status directly
                    status = raw_status
                    is_completed = raw_status == "DONE"
                    is_incomplete = due_date_dt and due_date_dt <= end_of_period and not is_completed
                    is_not_due_yet = due_date_dt and due_date_dt > end_of_period and not is_completed

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

                    # Check for rules violation and determine violation types
                    rules_violated = "No"
                    rules_violated_urls = ""
                    violation_types = []
                    # Rule 1: Missing Component
                    if not component_id or department == "Unknown":
                        rules_violated = "Yes"
                        rules_violated_urls = task_url
                        violation_types.append("Missing Component")
                    # Rule 2: Missing Due Date
                    if due_date_dt is None:
                        rules_violated = "Yes"
                        rules_violated_urls = task_url
                        violation_types.append("Missing Due Date")
                    # Rule 3: Missing Comment after Status Update
                    if not comment or not comment.strip():
                        rules_violated = "Yes"
                        rules_violated_urls = task_url
                        violation_types.append("Missing Comment")

                    # Join violation types if there are multiple
                    violation_type = ", ".join(violation_types) if violation_types else ""

                    # Append "[Rule Violator]" to employee name if rules are violated
                    if rules_violated == "Yes":
                        mapped_employee = f"{mapped_employee} [Rule Violator]"

                    # Assign employee code based on mapped name (before adding [Rule Violator])
                    employee_code = employee_code_mapping.get(mapped_employee.split(" [Rule Violator]")[0], None)

                    # Add to processed data
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
                        "Due Date": due_date_dt.strftime('%Y-%m-%d') if due_date_dt else "",
                        "Rules Violated": rules_violated,
                        "Rules Violated URLs": rules_violated_urls,
                        "Violation Type": violation_type,
                        "Estimated Time": estimation,
                        "Reported Time": reported_time,
                        "Comments": has_comment,
                        "Modified On": modified_on_dt,
                        "Task Title": task_title,
                        "Comment": comment
                    })
                except Exception as e:
                    logger.error(f"Error processing task: {item}. Error: {str(e)}")
                    continue

            return processed_data

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
                    # Clean up the name by removing leading/trailing commas and spaces
                    employee_cleaned = employee_raw.strip(',').strip()
                    employee = employee_cleaned.split(",", 1)[-1].strip() + " " + employee_cleaned.split(",", 1)[0].strip() if "," in employee_cleaned and employee_cleaned != "Unassigned" else employee_cleaned

                    # Apply name mapping
                    mapped_employee = name_mapping.get(employee, employee)

                    component_id = item.get("component")
                    department = component_department_map.get(component_id, "Unknown")
                    task_title = item.get("title", "No Title")
                    status = item.get("status", "Unknown")
                    comment = item.get("comment", "")

                    # Assign employee code based on mapped name
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

        # Function to display analysis (shared between daily and monthly reports)
        def display_analysis(df, period_label, set1_colors):
            # Quick Overview Dashboard
            with st.container():
                st.header("Quick Overview")
                st.markdown(f"A snapshot of key task performance metrics for the {period_label}.", unsafe_allow_html=True)

                # Calculate metrics for all task statuses
                total_tasks = df.shape[0]
                done_on_time = df[df['Task Status'] == 'DONE(On Time)'].shape[0]
                done_late = df[df['Task Status'] == 'DONE(Late)'].shape[0]
                done_no_due_date = df[df['Task Status'] == 'DONE(No Due Date)'].shape[0]
                incomplete = df[df['Task Status'] == 'Incomplete'].shape[0]
                in_progress_not_due = df[df['Task Status'] == 'In Progress(not due yet)'].shape[0]
                in_progress_no_due = df[df['Task Status'] == 'In Progress(No Due Date)'].shape[0]
                rule_violations_count = df[df['Rules Violated'] == 'Yes'].shape[0]

                # Display metrics in a card layout
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
                            <h3>Done (On Time)</h3>
                            <p>{done_on_time}</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                        <div class="overview-card">
                            <i class="fas fa-clock"></i>
                            <h3>Done (Late)</h3>
                            <p>{done_late}</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col4:
                    st.markdown(f"""
                        <div class="overview-card">
                            <i class="fas fa-calendar-check"></i>
                            <h3>Done (No Due Date)</h3>
                            <p>{done_no_due_date}</p>
                        </div>
                    """, unsafe_allow_html=True)

                col5, col6, col7, col8 = st.columns(4)
                with col5:
                    st.markdown(f"""
                        <div class="overview-card">
                            <i class="fas fa-hourglass-half"></i>
                            <h3>Incomplete</h3>
                            <p>{incomplete}</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col6:
                    st.markdown(f"""
                        <div class="overview-card">
                            <i class="fas fa-spinner"></i>
                            <h3>In Progress (Not Due)</h3>
                            <p>{in_progress_not_due}</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col7:
                    st.markdown(f"""
                        <div class="overview-card">
                            <i class="fas fa-calendar-times"></i>
                            <h3>In Progress (No Due)</h3>
                            <p>{in_progress_no_due}</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col8:
                    st.markdown(f"""
                        <div class="overview-card">
                            <i class="fas fa-exclamation-triangle"></i>
                            <h3>Rule Violations</h3>
                            <p>{rule_violations_count}</p>
                        </div>
                    """, unsafe_allow_html=True)

            # Analysis Section
            with st.container():
                st.header("Analysis Dashboard")

                # Question 1: Overall Completion Rate with Task Status Breakdown
                st.subheader(f"Q1: What is the overall completion rate of tasks in the {period_label}?")
                total_tasks = df.shape[0]
                completed_tasks = (done_on_time + done_late + done_no_due_date)
                incomplete_tasks = total_tasks - completed_tasks
                completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                incomplete_rate = (incomplete_tasks / total_tasks * 100) if total_tasks > 0 else 0

                # Display metrics using st.metric
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Tasks", total_tasks)
                with col2:
                    st.metric("Completed Tasks", f"{completed_tasks} ({completion_rate:.2f}%)")
                with col3:
                    st.metric("Incomplete Tasks", f"{incomplete_tasks} ({incomplete_rate:.2f}%)")

                # Task Status breakdown with expander
                task_status_counts = df['Task Status'].value_counts().reset_index()
                task_status_counts.columns = ['Task Status', 'Count']
                with st.expander("View Task Status Breakdown"):
                    st.write(task_status_counts)

                # Visualize: Pie chart for overall completion
                fig1 = go.Figure(data=[
                    go.Pie(labels=['Completed', 'Incomplete'],
                           values=[completed_tasks, incomplete_tasks],
                           textinfo='label+percent',
                           marker=dict(colors=set1_colors[:2]))
                ])
                fig1.update_layout(title_text=f'Overall Task Completion Rate ({period_label})',
                                   font=dict(color='#f9fafb'))
                st.plotly_chart(fig1, use_container_width=True)

                # Visualize: Bar chart for task status breakdown
                fig1b = px.bar(task_status_counts, x='Task Status', y='Count',
                               title=f'Task Status Distribution ({period_label})',
                               labels={'Count': 'Number of Tasks'},
                               color='Task Status',
                               color_discrete_sequence=set1_colors)
                fig1b.update_layout(xaxis_title='Task Status', yaxis_title='Number of Tasks', xaxis_tickangle=-45, showlegend=False,
                                    font=dict(color='#f9fafb'))
                st.plotly_chart(fig1b, use_container_width=True)

                # Question 2: Task Completion Rate per Employee with Task Status Breakdown
                st.subheader(f"Q2: What is the task completion rate per employee in the {period_label}?")
                with st.container():
                    q2_employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
                    q2_selected_employee = st.selectbox("Filter by Employee (Q2)", q2_employees, key="q2_employee_filter")
                    df_q2 = df.copy()
                    if q2_selected_employee != "All":
                        df_q2 = df_q2[df_q2['Employee Name'].str.contains(q2_selected_employee, na=False)]

                employee_stats = df_q2.groupby('Employee Name').agg({
                    'Task Status': [
                        lambda x: sum(x.str.startswith('DONE')),
                        lambda x: sum(~x.str.startswith('DONE'))
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

                # Question 3: Task Completion Rate per Department
                st.subheader(f"Q3: What is the task completion rate per department in the {period_label}?")
                department_stats = df.groupby('Department Name').agg({
                    'Task Status': [
                        lambda x: sum(x.str.startswith('DONE')),
                        lambda x: sum(~x.str.startswith('DONE'))
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

                # Question 4: Incomplete Tasks with Due Date
                st.subheader(f"Q4: Which incomplete tasks need attention, and what are their direct URLs for review in the {period_label}?")
                with st.container():
                    q4_employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
                    q4_selected_employee = st.selectbox("Filter by Employee (Q4)", q4_employees, key="q4_employee_filter")
                    df_q4 = df.copy()
                    if q4_selected_employee != "All":
                        df_q4 = df_q4[df_q4['Employee Name'].str.contains(q4_selected_employee, na=False)]

                    # Ensure incomplete tasks are filtered correctly
                    incomplete_tasks_df = df_q4[df_q4['Task Status'] == 'Incomplete'][['Employee Name', 'Employee Code', 'Department Name', 'Incomplete Tasks', 'Incomplete Task URLs', 'Due Date', 'Comments']]
                    if not incomplete_tasks_df.empty:
                        st.write("**Incomplete Tasks:**")
                        st.dataframe(incomplete_tasks_df)
                    else:
                        st.write("No incomplete tasks found for the selected period.")

                            # Question 5: Rule Violations per Employee with Task Identifier, URL, and Violation Type
            st.subheader(f"Q5: How many tasks violated rules, and who are the responsible employees in the {period_label}?")
            with st.container():
                q5_employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
                q5_selected_employee = st.selectbox("Filter by Employee (Q5)", q5_employees, key="q5_employee_filter")
                df_q5 = df.copy()
                if q5_selected_employee != "All":
                    df_q5 = df_q5[df_q5['Employee Name'].str.contains(q5_selected_employee, na=False)]

                rule_violations_df = df_q5[df_q5['Rules Violated'] == 'Yes'][['Employee Name', 'Employee Code', 'Task Identifier', 'Rules Violated URLs', 'Violation Type']]
                rule_violations_df['Employee Name'] = rule_violations_df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True)
                rule_violations_summary = rule_violations_df.groupby('Employee Name').size().reset_index(name='Rule Violations')

                # API integration to send rule violation data with user feedback
                if not rule_violations_df.empty:
                    try:
                        api_url = "http://103.51.129.55/api.php"
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
                    st.write(rule_violations_df)
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

                # Question 6: Completed Tasks with Due Date, Task Identifier, and URL
                st.subheader(f"Q6: Which tasks were completed, and what are their due dates, task identifiers, and URLs in the {period_label}?")
                with st.container():
                    q6_employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
                    q6_selected_employee = st.selectbox("Filter by Employee (Q6)", q6_employees, key="q6_employee_filter")
                    df_q6 = df.copy()
                    if q6_selected_employee != "All":
                        df_q6 = df_q6[df_q6['Employee Name'].str.contains(q6_selected_employee, na=False)]

                completed_tasks_df = df_q6[df_q6['Tasks Completed'] != ''][['Employee Name', 'Employee Code', 'Department Name', 'Tasks Completed', 'Task Identifier', 'Due Date', 'Completed Task URLs', 'Comments']]
                if not completed_tasks_df.empty:
                    st.write("**Completed Tasks:**")
                    st.dataframe(completed_tasks_df)
                else:
                    st.write("No completed tasks found for the selected period.")

                # Question 7: Comparison of Estimated vs Reported Time per Department
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

                # Visualize: Bar chart for total estimated vs reported time
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

        if report_type == "Daily Report":
            # Date picker for selecting the report date
            with st.container():
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
            with st.container():
                st.markdown(f"### Daily Report for {report_date.strftime('%B %d, %Y')}", unsafe_allow_html=True)

            # Process data for the daily report
            processed_data = process_data(data, selected_date, selected_date)
            if not processed_data:
                st.error(f"No relevant tasks found in the JSON file for {report_date.strftime('%B %d, %Y')}.")
                st.stop()

            # Create DataFrame
            df = pd.DataFrame(processed_data)

            # Define column order
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
                "Comments"
            ]

            # Reorder DataFrame
            df = df[column_order]

            # Apply filters
            departments = ["All"] + sorted(df['Department Name'].unique())
            selected_department = st.sidebar.selectbox("Filter by Department", departments)
            if selected_department != "All":
                df = df[df['Department Name'] == selected_department]

            with st.container():
                employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
                selected_employee = st.selectbox("Filter by Employee (Global)", employees)
                if selected_employee != "All":
                    df = df[df['Employee Name'].str.contains(selected_employee, na=False)]

            # Export to Excel
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

            # Display the converted table overview if toggled on
            with st.container():
                if show_table_overview:
                    st.header("Overview of Converted Table (JSON to Excel)")
                    st.write(f"Below is the table generated from the uploaded JSON file for {report_date.strftime('%B %d, %Y')}:")
                    st.dataframe(df)

            # Provide download link for the Excel file
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

            # Display analysis
            set1_colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF', '#999999']
            display_analysis(df, f"Daily Report ({report_date.strftime('%B %d, %Y')})", set1_colors)

            # Clean up the temporary Excel file
            try:
                os.remove(output_filename)
                logger.info(f"Cleaned up temporary file: {output_filename}")
            except Exception as e:
                logger.warning(f"Could not delete temporary file {output_filename}: {str(e)}")

        elif report_type == "Monthly Report":
            # Date range picker for selecting the report period
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

            # Validate the date range
            if start_date > end_date:
                st.error("Start date must be before or equal to the end date.")
                st.stop()
            if start_date > current_date or end_date > current_date:
                st.error(f"Dates cannot be after {current_date}.")
                st.stop()

            # Update the title with the selected date range
            with st.container():
                st.markdown(f"### Monthly Report from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}", unsafe_allow_html=True)

            # Process data for the monthly report
            processed_data = process_data(data, start_date, end_date)
            if not processed_data:
                st.error(f"No relevant tasks found in the JSON file for the period from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}.")
                st.stop()

            # Create DataFrame
            df = pd.DataFrame(processed_data)

            # Define column order
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
                "Comments"
            ]

            # Reorder DataFrame
            df = df[column_order]

            # Apply filters
            departments = ["All"] + sorted(df['Department Name'].unique())
            selected_department = st.sidebar.selectbox("Filter by Department", departments)
            if selected_department != "All":
                df = df[df['Department Name'] == selected_department]

            with st.container():
                employees = ["All"] + sorted(df['Employee Name'].str.replace(' \[Rule Violator\]', '', regex=True).unique())
                selected_employee = st.selectbox("Filter by Employee (Global)", employees)
                if selected_employee != "All":
                    df = df[df['Employee Name'].str.contains(selected_employee, na=False)]

            # Export to Excel
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

            # Display the converted table overview if toggled on
            with st.container():
                if show_table_overview:
                    st.header("Overview of Converted Table (JSON to Excel)")
                    st.write(f"Below is the table generated from the uploaded JSON file for the period from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}:")
                    st.dataframe(df)

            # Provide download link for the Excel file
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

            # Display analysis
            set1_colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF', '#999999']
            display_analysis(df, f"Monthly Report ({start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')})", set1_colors)

            # Clean up the temporary Excel file
            try:
                os.remove(output_filename)
                logger.info(f"Cleaned up temporary file: {output_filename}")
            except Exception as e:
                logger.warning(f"Could not delete temporary file {output_filename}: {str(e)}")

        elif report_type == "Hourly Employee Monitoring":
            # Process data for hourly monitoring
            processed_data = process_hourly_data(data)
            if not processed_data:
                st.error("No relevant tasks found to process.")
                st.stop()

            # Create DataFrame
            df = pd.DataFrame(processed_data)

            # Select hour for monitoring
            current_hour = datetime.now(pytz.timezone('Asia/Dhaka')).hour
            selected_hour = st.sidebar.selectbox("Select Hour (24h)", list(range(24)), index=current_hour)

            st.markdown(f"### Hourly Employee Monitoring for {selected_hour}:00", unsafe_allow_html=True)

            # Group data by department and display employees
            for department in df['Department Name'].unique():
                dept_df = df[df['Department Name'] == department]
                with st.container():
                    st.markdown(f'<div class="dept-container"><h3>{department} (Head: {dept_df["Department Head"].iloc[0]})</h3>', unsafe_allow_html=True)
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
                    st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        logger.error(f"Error processing JSON file: {str(e)}")
        st.error(f"Failed to process the JSON file: {str(e)}")