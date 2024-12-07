import pandas as pd
import streamlit as st

# Set page configuration for Streamlit app
st.set_page_config(page_title="Transaction Analysis Dashboard", layout="wide")

# Custom CSS for a dark theme with gradient title and professional card styles
custom_css = """
<style>
body {
    background-color: #181818;  /* Dark background */
    color: #E0E0E0;  /* Light text */
    font-family: 'Arial', sans-serif;
}

.dashboard-banner {
    background: linear-gradient(135deg, #1f2a36, #2C2C2C);  /* Gradient background */
    color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 30px;
}

.dashboard-banner h1 {
    font-size: 36px;
    margin: 0;
    font-weight: 700;
    color: #f5a623;  /* Light orange for emphasis */
}

.dashboard-banner p {
    font-size: 20px;
    margin: 5px 0 0 0;
}

.section-header {
    font-size: 24px;
    color: #f5a623;  /* Light orange for headers */
    margin-top: 20px;
    font-weight: 600;
}

.card {
    background: linear-gradient(135deg, #1f2a36, #2C2C2C);  /* Gradient background */
    color: #E0E0E0;  /* Light text color */
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
    margin: 15px;
    transition: transform 0.3s, box-shadow 0.3s;
    height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-width: 230px;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 8px 18px rgba(0, 0, 0, 0.4);
}

.card h3 {
    font-size: 22px;
    margin-bottom: 10px;
    font-weight: 500;
    color: #f5a623;  /* Light orange */
}

.card p {
    font-size: 30px;
    font-weight: 600;
    margin: 0;
    color: #f39c12;  /* Golden color for emphasis */
}

.card .bar-container {
    width: 100%;
    height: 8px;
    background: #444444;
    margin-top: 15px;
    border-radius: 5px;
    position: relative;
}

.card .bar-fill {
    height: 100%;
    border-radius: 5px;
    background: linear-gradient(90deg, #f5a623, #f39c12);  /* Bar theme color */
    position: absolute;
    top: 0;
    left: 0;
}

.card .bar-border {
    width: 100%;
    height: 100%;
    border-radius: 5px;
    border: 1px solid #333333;  /* Thin border on the right or left */
    position: absolute;
    top: 0;
    left: 0;
}

.table-container {
    overflow-x: auto;
    margin-top: 30px;
}

.table-container table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

.table-container th, .table-container td {
    text-align: left;
    padding: 12px;
    border: 1px solid #333333;  /* Darker borders */
}

.table-container th {
    background-color: #2e3b4e;
    color: #ffffff;
}

.table-container tr:nth-child(even) {
    background-color: #2C2C2C;  /* Dark rows */
}

.table-container tr:hover {
    background-color: #444444;  /* Lighter hover effect */
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Load the data with caching
@st.cache_data
def load_data():
    # Load your dataset from the specified path
    df = pd.read_excel("C:/Users/SPPL IT/Desktop/Study/Python/Competition/Battle Of Insights/Data/transactions.xlsx")
    df["Date"] = pd.to_datetime(df["Date"])  # Ensure 'Date' column is datetime
    df["Discount_Applied"].fillna(False, inplace=True)  # Ensure no missing values in 'Discount_Applied'
    return df

df = load_data()

# Sidebar with radio buttons for navigating between sections
sidebar_option = st.sidebar.radio("Select Section", ["Dataset Overview", "Analysis"])

# Dataset Overview Section
if sidebar_option == "Dataset Overview":
    # Dashboard Banner with Gradient
    st.markdown(
        """
        <div class="dashboard-banner">
            <h1>📊 E-commerce Customer Behavior Dashboard</h1>
            <p>Gain deep insights into customer behavior, purchasing patterns, and satisfaction metrics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Detailed Dataset Overview
    st.markdown("<h2 class='section-header'>Detailed Dataset Overview</h2>", unsafe_allow_html=True)
    st.dataframe(df)  # Display the full dataframe
    st.write("This dataset provides a comprehensive view of customer behavior metrics, including details on purchases, demographics, and return rates.")

    # Dataset Overview at a Glance
    st.markdown("<h2 class='section-header'>Dataset Overview at a Glance</h2>", unsafe_allow_html=True)

    # Key Metrics Display with Emojis
    total_transactions = df["Transaction_ID"].nunique()
    total_customers = df["Customer_Name"].nunique()
    avg_amount = df["Amount($)"].mean()
    total_discounted = df[df["Discount_Applied"] == True].shape[0]
    avg_items_per_transaction = df["Total_Items"].mean()

    # Create 3 columns for the top row and 2 columns for the bottom row
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>💳 Total Transactions</h3>
                <p>{}</p>
            </div>
            """.format(total_transactions),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>👥 Total Customers</h3>
                <p>{}</p>
            </div>
            """.format(total_customers),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <h3>💵 Avg. Purchase Amount</h3>
                <p>${:.2f}</p>
            </div>
            """.format(avg_amount),
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="card">
                <h3>🎉 Discounted Purchases</h3>
                <p>{}</p>
            </div>
            """.format(total_discounted),
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            """
            <div class="card">
                <h3>📦 Avg. Items per Transaction</h3>
                <p>{:.2f}</p>
            </div>
            """.format(avg_items_per_transaction),
            unsafe_allow_html=True,
        )

# Analysis Section
elif sidebar_option == "Analysis":
    # Here you can start adding the analysis part of the dashboard
    st.markdown("<h2 class='section-header'>Analysis Section</h2>", unsafe_allow_html=True)
    st.write("This section will be used for analysis questions and insights.")
