import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
import streamlit as st
from streamlit.components.v1 import html

warnings.filterwarnings("ignore")

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
    df = pd.read_excel("C:/Users/SPPL IT/Desktop/Study/Python/Competition/Battle Of Insights/Data/updated.xlsx")
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

# If the selected option is "Analysis", show the analysis visualizations
if sidebar_option == "Analysis":
    # 1. Average transaction amount by store type and season
    df_aggregated = df.groupby(["Store_Type", "Season"])["Amount($)"].mean().reset_index()

    fig = px.bar(
        df_aggregated,
        x='Store_Type',
        y='Amount($)',
        color='Season',
        title='Average Transaction Amount by Store Type and Season',
        labels={'Amount($)': 'Average Amount ($)', 'Store_Type': 'Store Type'},
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set3  # Professional color palette
    )

    # Add count labels on top of the bars
    fig.update_traces(text=df_aggregated["Amount($)"].round(2), textposition='outside', textfont_size=14, insidetextanchor="middle")

    # Customize layout
    fig.update_layout(
        title={
            'text': 'Average Transaction Amount by Store Type and Season',
            'x': 0.5,  # Center alignment
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'Arial', 'color': '#f5a623'}
        },
        xaxis={
            'title': {'text': 'Store Type', 'font': {'size': 16, 'color': '#f5a623'}},
            'tickangle': -30
        },
        yaxis={
            'title': {'text': 'Average Amount ($)', 'font': {'size': 16, 'color': '#f5a623'}}
        },
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        showlegend=True
    )

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)

    # Search icon button for interpretation
    search_button = st.button("🔍 Interpret Data")

    # Interpretation box
    if search_button:
        st.markdown(
            """
            <div style="background-color:#2C2C2C; padding:15px; border-radius:10px;">
                <h4 style="color: #f5a623; font-size: 18px; font-weight: bold;">Data Interpretation:</h4>
                <p style="color: #E0E0E0;">The chart illustrates the average transaction amount across different store types and seasons, showcasing how seasonality influences customer spending patterns. A comparison between Store Types (e.g., Online vs. Physical) can reveal which one performs better under different seasonal conditions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    # Question 2: Which payment method is most commonly used in high-value transactions, and how does it differ across cities?
    st.markdown("<h2 class='section-header'>Most Common Payment Method in High-Value Transactions by City</h2>", unsafe_allow_html=True)

    # Calculate the average transaction amount
    average_transaction_amount = df['Amount($)'].mean()

    # Filter for high-value transactions
    high_value_transactions = df[df['Amount($)'] > average_transaction_amount]

    # Count the payment methods used in high-value transactions across cities
    payment_method_counts = high_value_transactions.groupby(['City', 'Payment_Method']).size().reset_index(name='Count')

    # Identify the most commonly used payment method in each city
    most_common_payment_method = payment_method_counts.loc[payment_method_counts.groupby('City')['Count'].idxmax()]

    # Create the bar plot
    fig = px.bar(
        payment_method_counts,
        x='City',
        y='Count',
        color='Payment_Method',
        barmode='group',
        title='Most Common Payment Method in High-Value Transactions by City',
        labels={'Count': 'Number of Transactions', 'City': 'City'},
        color_discrete_sequence=px.colors.qualitative.Set3,
        text='Count'
    )

    # Update layout
    fig.update_layout(
        title={
            'text': 'Most Common Payment Method in High-Value Transactions by City',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'Arial', 'color': '#f5a623'}
        },
        font=dict(size=13, family='Arial'),
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        legend=dict(
            title='Payment Method',
            font=dict(size=13, family='Arial', color='#E0E0E0')
        ),
        xaxis=dict(
            title='City',
            tickangle=-45,
            title_font=dict(size=16, color='#f5a623'),
            tickfont=dict(size=12, family='Arial', color='#E0E0E0'),
            showgrid=True,
            gridcolor='#444444',
        ),
        yaxis=dict(
            title='Number of Transactions',
            title_font=dict(size=16, color='#f5a623'),
            tickfont=dict(size=12, family='Arial', color='#E0E0E0'),
            showgrid=True,
            gridcolor='#444444',
        )
    )

    # Update bar appearance
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        marker_line_width=1.5,
        textfont=dict(size=11, family='Arial', color='#E0E0E0', weight='bold')
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Add a state to track if the interpretation has been toggled
    if "interpret_payment_methods" not in st.session_state:
        st.session_state.interpret_payment_methods = False

    # Button for interpretation
    if st.button("🔍 Interpret Data for Payment Methods"):
        st.session_state.interpret_payment_methods = not st.session_state.interpret_payment_methods  # Toggle state

    # Show interpretation based on the state
    if st.session_state.interpret_payment_methods:
        st.markdown(
            """
            <div style="background-color:#2C2C2C; padding:15px; border-radius:10px;">
                <h4 style="color: #f5a623; font-size: 18px; font-weight: bold;">Data Interpretation:</h4>
                <p style="color: #E0E0E0;">The chart highlights the most commonly used payment methods for high-value transactions in each city. It offers a clear view of how customer payment preferences vary regionally for purchases exceeding the average transaction amount.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
# Question 3: How do the sales amounts in transactions with discounts compare to those without discounts, and what trends can be observed over the month?
st.markdown("<h2 class='section-header'>Sales Amounts: With vs Without Discounts Over the Month</h2>", unsafe_allow_html=True)

# Extract only the month name (e.g., 'January', 'February', etc.)
df['Month'] = df['Date'].dt.strftime('%B')

# Group by Month and Discount status, summing the sales amounts
sales_comparison = df.groupby(['Month', 'Discount_Applied'])['Amount($)'].sum().reset_index()

# Sort by month order (using a predefined month order list)
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
sales_comparison['Month'] = pd.Categorical(sales_comparison['Month'], categories=month_order, ordered=True)

# Sort the data by month for chronological order
sales_comparison = sales_comparison.sort_values(by='Month').reset_index(drop=True)

# Create the line plot
fig = px.line(
    sales_comparison,
    x='Month',
    y='Amount($)',
    color='Discount_Applied',
    title='Sales Amounts: With vs Without Discounts Over the Month',
    labels={'Amount($)': 'Total Sales Amount ($)', 'Month': 'Month'},
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Set3
)

# Update layout to match the desired theme
fig.update_layout(
    title={
        'text': 'Sales Amounts: With vs Without Discounts Over the Month',
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20, 'family': 'Arial', 'color': '#f5a623'}
    },
    font=dict(size=13, family='Arial'),
    height=600,
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    legend=dict(
        title='Discount Applied',
        font=dict(size=13, family='Arial', color='#E0E0E0')
    ),
    xaxis=dict(
        title='Month',
        tickangle=-45,
        title_font=dict(size=16, color='#f5a623'),
        tickfont=dict(size=12, family='Arial', color='#E0E0E0'),
        showgrid=True,
        gridcolor='#444444',
    ),
    yaxis=dict(
        title='Total Sales Amount ($)',
        title_font=dict(size=16, color='#f5a623'),
        tickfont=dict(size=12, family='Arial', color='#E0E0E0'),
        showgrid=True,
        gridcolor='#444444',
    )
)

# Enhance markers and line visibility, and add black borders around markers
fig.update_traces(
    marker=dict(
        size=8,  # Adjust marker size for visibility
        line=dict(width=1.5, color='black')  # Thin black border around markers
    ),
    line=dict(width=2)  # Adjust line width for clarity
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Add a state to track if the interpretation has been toggled
if "interpret_sales_comparison" not in st.session_state:
    st.session_state.interpret_sales_comparison = False

# Button for interpretation
if st.button("🔍 Interpret Data for Sales Comparison"):
    st.session_state.interpret_sales_comparison = not st.session_state.interpret_sales_comparison  # Toggle state

# Show interpretation based on the state
if st.session_state.interpret_sales_comparison:
    st.markdown(
        """
        <div style="background-color:#2C2C2C; padding:15px; border-radius:10px;">
            <h4 style="color: #f5a623; font-size: 18px; font-weight: bold;">Data Interpretation:</h4>
            <p style="color: #E0E0E0;">This visualization compares the total sales amounts for transactions with and without discounts across different months. Observe how discounts influence sales trends over time and identify seasonal peaks for both categories.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Question 4: Top three cities with the highest average number of items per transaction and their seasonal sales amounts
st.markdown("<h2 class='section-header'>Average Items per Transaction & Sales by Season</h2>", unsafe_allow_html=True)

# Step 1: Calculate average number of items per city
avg_items_per_city = df.groupby("City")["Total_Items"].mean().reset_index().sort_values(by="Total_Items", ascending=False)

# Step 2: Get the top three cities with the highest average number of items
top_cities = avg_items_per_city.nlargest(3, 'Total_Items')

# Step 3: Filter the original dataframe for these top cities
filtered_df = df[df['City'].isin(top_cities['City'])]

# Step 4: Group by City and Season to sum the sales amounts
sales_by_season = filtered_df.groupby(['City', 'Season'])['Amount($)'].sum().reset_index()

# Step 5: Prepare visualizations using Plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

# Define a color palette using Set3 for both plots
color_palette = px.colors.qualitative.Set3

# Create subplot with 2 rows
fig_combined = make_subplots(
    rows=2, cols=1,
    shared_xaxes=False,
    row_heights=[0.5, 0.5],
    subplot_titles=(
        "<b>Average Number of Items per City</b>",
        "<b>Sales Amounts Across Seasons for Top Cities by Average Items per Transaction</b>"
    ),
    vertical_spacing=0.2
)

# First Chart: Average Number of Items per City (sorted)
avg_items_per_city_sorted = avg_items_per_city.sort_values(by='Total_Items', ascending=True)
fig_combined.add_trace(
    go.Bar(
        x=avg_items_per_city_sorted['Total_Items'],
        y=avg_items_per_city_sorted['City'],
        text=avg_items_per_city_sorted['Total_Items'].round(2),
        orientation='h',
        marker_color=color_palette[:len(avg_items_per_city_sorted)],  # Unique color for each city
        texttemplate='%{text}',
        textposition='inside',
        hoverinfo='x+y',
        showlegend=False
    ),
    row=1, col=1
)

# Second Chart: Sales by Season for Top Cities
for i, season in enumerate(sales_by_season['Season'].unique()):
    season_data = sales_by_season[sales_by_season['Season'] == season]
    fig_combined.add_trace(
        go.Bar(
            x=season_data['City'],
            y=season_data['Amount($)'],
            text=season_data['Amount($)'].apply(lambda x: f'${x/1000:.1f}k'),
            texttemplate='%{text}',
            textposition='outside',
            name=season,  # Season as legend entry
            marker_color=color_palette[i % len(color_palette)]  # Rotate colors
        ),
        row=2, col=1
    )

# Step 6: Update layout and styles
fig_combined.update_layout(
    height=1000,
    width=1100,
    title_text="<b>Top Cities: Average Items & Seasonal Sales Analysis</b>",
    title_font=dict(size=22, family='Arial', color='#f5a623'),  # Updated title color
    font=dict(size=13, family='Arial'),
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    legend=dict(
        title='Season',
        orientation='v',
        font=dict(size=12, family='Arial')
    ),
    barmode='group'  # Grouped bars for seasonal sales
)

# Update axes with new color and better readability
fig_combined.update_xaxes(
    title_text="Average Number of Items",
    row=1, col=1,
    showgrid=True,
    gridcolor='lightgray',
    title_font=dict(size=14, color='#f5a623')  # Updated x-axis title color
)
fig_combined.update_yaxes(
    title_text="City",
    row=1, col=1,
    showgrid=True,
    gridcolor='lightgray',
    title_font=dict(size=14, color='#f5a623')  # Updated y-axis title color
)
fig_combined.update_xaxes(
    title_text="Sales Amount ($)",
    row=2, col=1,
    showgrid=True,
    gridcolor='lightgray',
    title_font=dict(size=14, color='#f5a623')  # Updated x-axis title color
)
fig_combined.update_yaxes(
    title_text="City",
    row=2, col=1,
    showgrid=True,
    gridcolor='lightgray',
    title_font=dict(size=14, color='#f5a623')  # Updated y-axis title color
)

# Step 7: Display the combined plot in Streamlit
st.plotly_chart(fig_combined, use_container_width=True)

# Interpretation Button
if "interpret_top_cities" not in st.session_state:
    st.session_state.interpret_top_cities = False

if st.button("🔍 Interpret Data for Top Cities"):
    st.session_state.interpret_top_cities = not st.session_state.interpret_top_cities

# Show interpretation if toggled
if st.session_state.interpret_top_cities:
    st.markdown(
        """
        <div style="background-color:#2C2C2C; padding:15px; border-radius:10px;">
            <h4 style="color: #f5a623; font-size: 18px; font-weight: bold;">Data Insights:</h4>
            <p style="color: #E0E0E0;">The analysis highlights the top three cities with the highest average number of items per transaction. Seasonal sales trends reveal how each city's revenue varies throughout the year, offering insights into seasonal demand patterns and inventory optimization opportunities.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
 # Question 5: Effectiveness of Promotions and Best Performers per Season
st.markdown("<h2 class='section-header'>Promotion Effectiveness by Season</h2>", unsafe_allow_html=True)

# Step 1: Group data by Promotion and Season, summing the transaction amounts
promotion_performance = df.groupby(['Promotion', 'Season'])['Amount($)'].sum().reset_index()

# Step 2: Identify the best-performing promotion for each season
best_promotions = promotion_performance.loc[promotion_performance.groupby('Season')['Amount($)'].idxmax()]

# Step 3: Create a grouped bar chart for promotions' performance
import plotly.express as px

# Define color palette
color_palette = px.colors.qualitative.Set3

# Create bar chart
fig = px.bar(
    promotion_performance,
    x='Season',
    y='Amount($)',
    color='Promotion',
    title="<b>Effectiveness of Promotions in Driving Transaction Amounts by Season</b>",
    labels={'Amount($)': 'Total Transaction Amount ($)', 'Season': 'Season'},
    barmode='group',
    color_discrete_sequence=px.colors.qualitative.Set3 
)

# Customizing layout and aesthetics
fig.update_layout(
    height=500,
    width=1100,
    title_font=dict(size=20, family='Arial', color='#f5a623'),  # Title color as per theme
    font=dict(size=13, family='Arial'),
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background,
    margin=dict(t=60, b=50, l=50, r=50),  # Adjusted margins for better spacing
    legend=dict(
        title='Promotion Type',
        font=dict(size=12),
        orientation='v',  # Vertical orientation for the legend
        yanchor='top',
        y=1,
        xanchor='left',
        x=1.05  # Position the legend on the right
    )
)

# Add custom bold text on top of the bars with "K" formatting
fig.update_traces(
    text=promotion_performance['Amount($)'].apply(lambda x: f'{x / 1000:.1f}K'),  # Convert to K format
    textposition='outside',  # Position the text on top of bars
    textfont=dict(size=11, family='Arial', color='black', weight='bold')  # Bold text
)

# Enhancing axes and gridlines
fig.update_xaxes(
    title_text="Season",
    showgrid=True,
    gridcolor='lightgray',
    title_font=dict(size=14, color='#f5a623')  # Updated x-axis title color
)
fig.update_yaxes(
    title_text="Total Transaction Amount ($)",
    showgrid=True,
    gridcolor='lightgray',
    title_font=dict(size=14, color='#f5a623')  # Updated y-axis title color
)

# Step 4: Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Interpretation Button
if "interpret_promotions" not in st.session_state:
    st.session_state.interpret_promotions = False

if st.button("🔍 Interpret Promotion Effectiveness"):
    st.session_state.interpret_promotions = not st.session_state.interpret_promotions

# Show interpretation if toggled
if st.session_state.interpret_promotions:
    st.markdown(
        f"""
        <div style="background-color:#2C2C2C; padding:15px; border-radius:10px;">
            <h4 style="color: #f5a623; font-size: 18px; font-weight: bold;">Data Insights:</h4>
            <p style="color: #E0E0E0;">
                The analysis reveals the following:
                <ul>
                    <li><strong>Top Promotion Types:</strong> The best-performing promotions in each season are:
                        <ul>
                            {"".join(f"<li>{row['Season']}: {row['Promotion']} (${row['Amount($)']:,.2f})</li>" for _, row in best_promotions.iterrows())}
                        </ul>
                    </li>
                    <li>Promotion effectiveness varies significantly across seasons, suggesting opportunities for optimizing campaigns based on seasonal demand patterns.</li>
                </ul>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )



    