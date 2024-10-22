import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Custom CSS for better metric visualization 
st.markdown(
    """
    <style>
    body {
        background-color: #2C3E50; /* Dark background color */
    }
    .metric-container {
        background-color: #34495E; /* Dark blue card for dark mode */
        color: white; /* White text for contrast */
        border-left: 5px solid #1ABC9C;
        padding: 15px; /* Increased padding for better spacing */
        border-radius: 10px;
        margin-bottom: 20px; /* Increased margin for spacing between metrics */
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5); /* Darker shadow */
        text-align: center; /* Center text in metrics */
        min-width: 200px; /* Minimum width for better uniformity */
    }
    .metric-header {
        font-size: 24px; /* Slightly larger header */
        text-align: center;
        color: #E74C3C; /* Red header for emphasis */
        margin: 20px 0; /* Margins for spacing */
    }
    .metric-container p {
        font-size: 18px; /* Increased font size for better visibility */
        margin: 0;
    }
    .metric-container h2 {
        font-size: 24px; /* Larger size for the main metric */
        margin: 5px 0; /* Reduced margin for closer display */
    }
    .icon {
        font-size: 28px; /* Increased icon size for better visibility */
        margin-right: 8px;
        color: #1ABC9C; /* Lighter green for better visibility */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Home Page Title and Description
st.markdown("<h1 style='text-align: center; color: #1ABC9C;'>E-commerce Customer Behavior Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #E74C3C;'>Gain deep insights into customer behavior, purchasing patterns, and satisfaction metrics.</h4>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('Competition/ecommerce_customer_behavior_dataset.csv')

df = load_data()


# Navigation Section
st.sidebar.title("Insights Navigation")
insight_level = st.sidebar.radio("Choose Insight Level", ["Basic Insights", "Intermediate Insights", "Critical Thinking Insights", "Own Findings"])

# Showing dataset overview only when 'Basic Insights' is selected
if insight_level == "Basic Insights":
    if 'first_time' not in st.session_state:
        st.session_state.first_time = True

    if st.session_state.first_time:
        st.header("Detailed Dataset Overview")
        st.dataframe(df)
        st.write("This dataset provides a comprehensive view of customer behavior metrics, including details on purchases, demographics, and return rates.")
        st.session_state.first_time = False

   
    st.markdown("---")  # Horizontal line separator

    # Adding Dataset Overview at a Glance Section
    st.markdown("<h2 class='metric-header'>Dataset Overview at a Glance</h2>", unsafe_allow_html=True)

    # Organizing the layout with compact columns
    with st.container():
        total_customers = df['Customer ID'].nunique()
        total_purchases = df['Number of Items Purchased'].sum()
        avg_order_value = df['Purchase Amount ($)'].mean()
        total_revenue = df['Purchase Amount ($)'].sum()
        avg_review_score = df['Review Score (1-5)'].mean()

      
        col1, col2, col3 = st.columns(3)  # Three equal columns for main metrics
        with col1:
            st.markdown("<div class='metric-container'><span class='icon'>👥</span><p>Total Customers</p><h2>{}</h2></div>".format(total_customers), unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='metric-container'><span class='icon'>🛒</span><p>Total Purchases</p><h2>{}</h2></div>".format(total_purchases), unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='metric-container'><span class='icon'>💵</span><p>Avg. Order Value</p><h2>${:.2f}</h2></div>".format(avg_order_value), unsafe_allow_html=True)

        col4, col5 = st.columns(2)  # Two columns for the remaining metrics
        with col4:
            st.markdown("<div class='metric-container'><span class='icon'>💰</span><p>Total Revenue</p><h2>${:.2f}</h2></div>".format(total_revenue), unsafe_allow_html=True)
        with col5:
            st.markdown("<div class='metric-container'><span class='icon'>⭐</span><p>Avg. Review Score</p><h2>{:.2f}/5</h2></div>".format(avg_review_score), unsafe_allow_html=True)

    st.write("Explore key customer metrics such as total customers, total purchases, and revenue to gain a quick understanding of the dataset.")



# Streamlit separator before Question 1
st.markdown("---")  # Separator

# Basic Insights - Q1
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Exploring Age Distribution: Mean, Median, and Mode</h2>", unsafe_allow_html=True)

    if 'Age' in df.columns:
        # Calculate statistics for the entire dataset
        age_mean = df['Age'].mean()
        age_median = df['Age'].median()
        age_mode = df['Age'].mode()[0]

        # Add a slider to filter age range
        age_range = st.slider("Select Age Range", 
                              int(df['Age'].min()), 
                              int(df['Age'].max()), 
                              (int(df['Age'].min()), int(df['Age'].max())))

        # Filter DataFrame based on selected age range
        filtered_df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

        # Calculate statistics for the filtered data
        filtered_age_mean = filtered_df['Age'].mean()
        filtered_age_median = filtered_df['Age'].median()
        filtered_age_mode = filtered_df['Age'].mode()[0] if not filtered_df['Age'].mode().empty else None

        # Creating a single figure
        fig = go.Figure()

        # Adding histogram for filtered data
        fig.add_trace(go.Histogram(x=filtered_df['Age'], name="Age Distribution", opacity=0.7))

        # Adding vertical lines for mean, median, and mode (filtered data)
        fig.add_vline(x=filtered_age_mean, line_dash="dash", line_color="red")
        fig.add_vline(x=filtered_age_median, line_dash="dash", line_color="green")
        if filtered_age_mode is not None:
            fig.add_vline(x=filtered_age_mode, line_dash="dash", line_color="blue")

        # Adding annotations for filtered data
        fig.add_annotation(
            x=filtered_age_mean, y=filtered_df['Age'].value_counts().max() * 0.9,
            text=f"Mean: {filtered_age_mean:.2f}",
            arrowhead=2,
            bgcolor="red",
            font=dict(color="white"),
            bordercolor="red",
            borderwidth=2,
            borderpad=2,
            arrowcolor="red",
            ax=-80, ay=-20  
        )

        fig.add_annotation(
            x=filtered_age_median, y=filtered_df['Age'].value_counts().max() * 0.9,
            text=f"Median: {filtered_age_median:.2f}",
            arrowhead=2,
            bgcolor="green",
            font=dict(color="white"),
            bordercolor="green",
            borderwidth=2,
            borderpad=2,
            arrowcolor="green",
            ax=60, ay=-20  
        )

        if filtered_age_mode is not None:
            fig.add_annotation(
                x=filtered_age_mode, y=filtered_df['Age'].value_counts().max() * 0.9,
                text=f"Mode: {filtered_age_mode}",
                arrowhead=2,
                bgcolor="blue",
                font=dict(color="white"),
                bordercolor="blue",
                borderwidth=2,
                borderpad=2,
                arrowcolor="blue",
                ax=-55, ay=25
            )

        # Update layout
        fig.update_layout(
            title_text="Age Distribution with Mean, Median, and Mode",
            xaxis_title_text="Age",
            yaxis_title_text="Count",
            bargap=0.2,
            showlegend=False
        )

        # Show the plot
        st.plotly_chart(fig)
    else:
        st.error("The dataset does not contain an 'Age' column.")

    # Streamlit separator
    st.markdown("---")  # Separator

## Question 2
# Custom CSS for better metric visualization
st.markdown(
    """
    <style>
    .dashboard-title {
        font-size: 24px;
        color: #1ABC9C; /* Bright color for the title */
        text-align: center;
        margin: 20px 0;
    }
    .metric-header {
        font-size: 20px;
        color: #E74C3C; /* Emphasize headers with a bright color */
        text-align: center;
        margin: 10px 0;
    }
    .metric-container {
        background-color: #34495E; /* Dark blue card for dark mode */
        color: white; /* White text for contrast */
        border-left: 5px solid #1ABC9C;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5); /* Shadow for depth */
    }
    </style>
    """,
    unsafe_allow_html=True
)

## BASIC QUE: 2
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Key Metrics for Purchase Amount</h2>", unsafe_allow_html=True)
    
    # Calculate variance and standard deviation
    variance = df['Purchase Amount ($)'].var()
    standard_deviation = df['Purchase Amount ($)'].std()
    mean_purchase_amount = df['Purchase Amount ($)'].mean()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-container'><p><strong>Variance of Purchase Amount:</strong></p><h2>{:.2f}</h2></div>".format(variance), unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-container'><p><strong>Standard Deviation of Purchase Amount:</strong></p><h2>{:.2f}</h2></div>".format(standard_deviation), unsafe_allow_html=True)

    # Calculate Z-scores
    df['Z-Score'] = (df['Purchase Amount ($)'] - mean_purchase_amount) / standard_deviation

    # Plot Z-Scores distribution in a histogram using Set1 color palette
    fig = go.Figure()

    # Define Set1 color palette
    set1_colors = px.colors.qualitative.Set1

    # Z-Scores distribution
    fig.add_trace(go.Histogram(x=df['Z-Score'], name='Z-Scores', 
                               marker_color=set1_colors[0], opacity=0.75))

    # Update layout for the figure with fixed height and width
    fig.update_layout(
        title='Z-Score Distribution of Purchase Amount',
        xaxis_title='Z-Score',
        yaxis_title='Count',
        template='plotly_white',
        height=600,  # Fixed height
        width=900,   # Fixed width
        bargap=0.2,  # Adjusts the gap between bars for better visibility
    )

    # Show plot in Streamlit
    st.plotly_chart(fig)

    # Display Z-score range
    z_min, z_max = df['Z-Score'].min(), df['Z-Score'].max()
    st.markdown("<h3 class='metric-header'>Z-Score Summary</h3>", unsafe_allow_html=True)
    st.markdown(f"**Z-score range:** {z_min:.2f} to {z_max:.2f}")

    # Streamlit separator
    st.markdown("---")  # Separator


# Basic Insights - Q3
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Top Product Categories Based on Purchases</h2>", unsafe_allow_html=True)

    if 'Product Category' in df.columns and 'Number of Items Purchased' in df.columns:
        # Create a slider for the number of top categories to display
        num_top_categories = st.slider("Select the number of top categories to display:", 1, 8, 3)

        top_categories = df.groupby("Product Category")["Number of Items Purchased"].sum().sort_values(ascending=False).head(num_top_categories)

        # Create the bar chart
        fig = px.bar(
            top_categories,
            x=top_categories.index,
            y=top_categories.values,
            labels={'x': 'Product Category', 'y': 'Count'},
            title=f'Top {num_top_categories} Product Categories',
            color=top_categories.index,
            color_discrete_sequence=px.colors.qualitative.Set1
        )

        # Annotations for the top categories
        annotations = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']

        for i in range(len(top_categories)):
            fig.add_annotation(
                x=top_categories.index[i],
                y=top_categories.values[i],
                text=f'{annotations[i]} Place',
                showarrow=True,
                arrowhead=2,
                ax=0, ay=-40,
                font=dict(size=14, color="white"),
                bgcolor="red",
                bordercolor="red",
                borderwidth=2,
                borderpad=4,
                arrowcolor="red"
            )

        # Show the plot
        st.plotly_chart(fig)
    else:
        st.error("The uploaded dataset does not contain the required columns for product categories and item counts.")

    st.markdown("---")  # Separator

# Basic Insights - Q4
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Analysis of Return Customers</h2>", unsafe_allow_html=True)

    if 'Return Customer' in df.columns and 'Gender' in df.columns:
        # Count of Return Customers vs. Non-Return Customers
        return_customer_counts = df['Return Customer'].value_counts()
        total_customers = return_customer_counts.sum()
        return_customer_percentages = (return_customer_counts / total_customers * 100).round(2)

        # Gender selection dropdown
        gender_selection = st.selectbox("Select Gender:", ["All", "Male", "Female", "Other"])

        # Filter data based on selected gender
        if gender_selection != "All":
            df = df[df['Gender'] == gender_selection]

        # Re-calculate return customer counts after filtering
        return_customer_counts = df['Return Customer'].value_counts()

        # Create a bar chart
        fig = go.Figure()

        # Add trace for return vs non-return customers
        fig.add_trace(go.Bar(
            x=return_customer_counts.index.map({True: 'Return Customers', False: 'Non-Return Customers'}),
            y=return_customer_counts.values,
            marker_color=px.colors.qualitative.Set1,
            text=[f'{count} ({percent:.2f}%)' for count, percent in zip(return_customer_counts.values, return_customer_percentages)]
            
        ))

        # Update layout and customize aesthetics
        fig.update_layout(
            height=500,
           
            margin=dict(l=50, r=50, t=100, b=50),
            font=dict(family="Arial", size=14)
        )

        # Improve the look of the bars with lines
        fig.update_traces(marker_line_color='black', marker_line_width=1.5)

        # Display the combined chart
        st.plotly_chart(fig)
    else:
        st.error("The uploaded dataset does not contain the required columns for return customers and gender.")

    st.markdown("---")  # Separator


# Basic Insights - Q5: Average Review Score Distribution
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Average Review Score Distribution</h2>", unsafe_allow_html=True)

    if 'Review Score (1-5)' in df.columns:
        # Calculate mean for Review Score
        review_mean = df['Review Score (1-5)'].mean()

        # Creating a single figure
        fig = go.Figure()

        # Adding histogram for Review Scores
        fig.add_trace(go.Histogram(x=df['Review Score (1-5)'], name="Review Score Distribution", opacity=0.7))

        # Adding vertical line for mean
        fig.add_vline(x=review_mean, line_dash="dash", line_color="red")

        # Add annotation for mean
        fig.add_annotation(
            x=review_mean, 
            y=df['Review Score (1-5)'].value_counts().max(), 
            text=f"Average Review Score: {review_mean:.2f}",
            arrowhead=2,
            bgcolor="red",
            font=dict(color="white"),
            bordercolor="red",
            borderwidth=2,
            borderpad=2,
            arrowcolor="red",
            ax=-60, 
            ay=-20  
        )

        # Update layout
        fig.update_layout(
            #title_text="Average Review Score Distribution",
            xaxis_title_text="Review Score (1-5)",
            yaxis_title_text="Count",
            bargap=0.2,
            showlegend=False
        )

        # Show the plot
        st.plotly_chart(fig)
    else:
        st.error("The uploaded dataset does not contain a 'Review Score (1-5)' column.")

    st.markdown("---")  # Separator

# Basic Insights - Q6: Average Delivery Time by Subscription Status
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Average Delivery Time by Subscription Status</h2>", unsafe_allow_html=True)

    if 'Subscription Status' in df.columns and 'Delivery Time (days)' in df.columns:
        # Create a DataFrame for visualization
        avg_delivery_time = df.groupby("Subscription Status")["Delivery Time (days)"].mean().reset_index()

        # Create a vertical bar chart
        bar_fig = px.bar(
            avg_delivery_time,
            x='Delivery Time (days)',
            y='Subscription Status',
            #title='Average Delivery Time by Subscription Status',
            labels={'Delivery Time (days)': 'Average Delivery Time (days)', 'Subscription Status': 'Subscription Status'},
            color='Subscription Status',
            color_discrete_sequence=px.colors.qualitative.Set1,  # Use a color sequence
            orientation='h'  # Horizontal bar chart
        )

        # Show the vertical bar chart
        st.plotly_chart(bar_fig)
    else:
        st.error("The uploaded dataset does not contain the required columns for subscription status and delivery time.")

    st.markdown("---")  # Separator

# Basic Insights - Q7: Number of Customers by Subscription Status
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Number of Customers by Subscription Status</h2>", unsafe_allow_html=True)

    if 'Subscription Status' in df.columns:
        # Prepare the data for visualization
        subscription_counts = df["Subscription Status"].value_counts().reset_index()
        subscription_counts.columns = ['Subscription Status', 'Count']

        # Create a bar chart
        bar_fig = px.bar(
            subscription_counts,
            x='Subscription Status',
            y='Count',
            #title='Number of Customers by Subscription Status',
            labels={'Count': 'Number of Customers'},
            color='Subscription Status',
            color_discrete_sequence=px.colors.qualitative.Set1,
        )

        # Show the bar chart
        st.plotly_chart(bar_fig)
        
    else:
        st.error("The uploaded dataset does not contain a 'Subscription Status' column.")

    st.markdown("---")  # Separator

# Basic Insights - Q8: Percentage of Customers by Device Type
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Percentage of Customers by Device Type</h2>", unsafe_allow_html=True)

    if 'Device Type' in df.columns:
        # Count occurrences of each device type
        device_counts = df["Device Type"].value_counts()
        total_counts = device_counts.sum()
        device_percentages = (device_counts / total_counts) * 100

        # Create a DataFrame for percentages
        device_percentage_df = pd.DataFrame({
            'Device Type': device_counts.index,
            'Percentage': device_percentages.values
        })

        # Create a pie chart to visualize the percentages
        pie_fig = px.pie(
            device_percentage_df,
            values='Percentage',
            names='Device Type',
            #title='Percentage of Customers by Device Type',
            color='Device Type',
            color_discrete_sequence=px.colors.qualitative.Set1,
            hole=0.3  # To make it a donut chart
        )

        # Add annotations to the pie chart
        pie_fig.update_traces(textinfo='percent+label', textfont_size=14)

        # Update layout for better aesthetics
        pie_fig.update_layout(
            #title_font_size=20,
            legend_title_text='Device Type',
            margin=dict(l=40, r=40, t=60, b=40),  # Adjust margins for clarity
        )

        # Show the pie chart
        st.plotly_chart(pie_fig)
    
    else:
        st.error("The uploaded dataset does not contain a 'Device Type' column.")
        
    st.markdown("---")  # Separator


# Basic Insights - Q9: Average Purchase Amount Based on Discount Status
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Average Purchase Amount Based on Discount Status</h2>", unsafe_allow_html=True)

    if 'Discount Availed' in df.columns and 'Purchase Amount ($)' in df.columns and 'Gender' in df.columns and 'Age' in df.columns:
        # Create dropdown for gender selection
        gender_options = df['Gender'].unique().tolist()
        selected_gender = st.selectbox("Select Gender:", options=["All"] + gender_options)

        # Create slider for age selection
        age_range = st.slider("Select Age Range:", min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=(int(df['Age'].min()), int(df['Age'].max())))

        # Filter the dataframe based on the selected gender and age range
        filtered_df = df.copy()

        if selected_gender != "All":
            filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
        
        filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]

        # Calculate average purchase amount based on discount status
        avg_purchase = filtered_df.groupby("Discount Availed")["Purchase Amount ($)"].mean().reset_index()

        # Map True/False to meaningful labels
        avg_purchase['Discount Availed'] = avg_purchase['Discount Availed'].map({True: 'Discount', False: 'No Discount'})

        # Create a bar chart
        bar_fig = px.bar(
            avg_purchase,
            x='Discount Availed',
            y='Purchase Amount ($)',
            title='Average Purchase Amount for Customers Who Availed Discounts',
            labels={'Discount Availed': 'Discount Status', 'Purchase Amount ($)': 'Average Amount'},
            color='Discount Availed',
            color_discrete_sequence=px.colors.qualitative.Set1,
        )

        # Adding data labels on top of the bars
        bar_fig.update_traces(
            texttemplate='%{y:.2f}', 
            textposition='outside',
            marker=dict(line=dict(width=1, color='black')),
            textfont_size=12
        )

        # Update layout for better aesthetics
        bar_fig.update_layout(
            title_font_size=20,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            font=dict(size=12),
            xaxis=dict(title=dict(standoff=10)),
            yaxis=dict(title=dict(standoff=10)),
            showlegend=False,
            height=500
        )

        # Show the bar chart
        st.plotly_chart(bar_fig)

        
    else:
        st.error("The uploaded dataset does not contain the required columns: 'Discount Availed', 'Purchase Amount ($)', 'Gender', or 'Age'.")
        
    st.markdown("---")  # Separator

# Basic Insights - Q10: Most Common Payment Method Used by Customers
if insight_level == "Basic Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Most Common Payment Method Used by Customers</h2>", unsafe_allow_html=True)

    # Create a dropdown for gender selection with an 'All' option set as default
    gender_options = df['Gender'].unique().tolist()
    gender_options.append('All')  # Add option for all genders
    selected_gender = st.selectbox("Select Gender:", gender_options, index=len(gender_options) - 1)  # Default to 'All'

    # Create a multi-select box for payment methods to filter
    payment_options = df['Payment Method'].unique().tolist()
    selected_payment = st.multiselect("Select Payment Methods to View:", payment_options, default=payment_options)

    # Check if 'Payment Method' exists in DataFrame
    if 'Payment Method' in df.columns:
        # Filter the DataFrame based on the selected gender
        filtered_df = df.copy()

        # Apply gender filter if selected
        if selected_gender != 'All':
            filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

        # Apply payment method filter
        if selected_payment:
            filtered_df = filtered_df[filtered_df['Payment Method'].isin(selected_payment)]

        # Count occurrences of each payment method
        payment_counts = filtered_df["Payment Method"].value_counts().reset_index()
        payment_counts.columns = ['Payment Method', 'Count']

        # Create a bar chart
        payment_fig = px.bar(
            payment_counts,
            x='Payment Method',
            y='Count',
            title='Most Common Payment Methods Used by Customers',
            labels={'Payment Method': 'Payment Method', 'Count': 'Number of Customers'},
            color='Payment Method',
            color_discrete_sequence=px.colors.qualitative.Set1,
        )

        # Adding annotation for the most common payment method
        if not payment_counts.empty:
            most_common_payment = payment_counts.iloc[0]  # Get the most common payment method
            payment_fig.add_annotation(
                x=most_common_payment['Payment Method'], 
                y=most_common_payment['Count'],
                text=f"Most Common: {most_common_payment['Payment Method']}",
                arrowhead=2,
                bgcolor="red",
                font=dict(color="white"),
                bordercolor="red",
                borderwidth=2,
                borderpad=2,
                arrowcolor="red",
                ax=0,
                ay=-40
            )

        # Update layout for better aesthetics
        payment_fig.update_layout(
            title_font_size=20,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            font=dict(size=12),
            showlegend=False,
            height=400
        )

        # Show the bar chart
        st.plotly_chart(payment_fig)
    else:
        st.error("The uploaded dataset does not contain the required column: 'Payment Method'.")


        
# Intermediate Insights - Q1
if insight_level == "Intermediate Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Average Review Scores by Payment Method</h2>", unsafe_allow_html=True)

    # Create a dropdown for gender selection
    gender_options = df['Gender'].unique().tolist()
    gender_options.append('All')  # Add option for all genders
    selected_gender = st.selectbox("Select Gender:", gender_options, index=len(gender_options) - 1)  # Default to 'All'

    # Filter the DataFrame based on the selected gender
    filtered_df = df.copy()

    # Apply gender filter if selected
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

    # Calculate the average review score for each payment method
    average_review_scores = filtered_df.groupby("Payment Method")["Review Score (1-5)"].mean().reset_index()

    # Create a bar chart for average review scores
    average_review_fig = px.bar(
        average_review_scores,
        x='Payment Method',
        y='Review Score (1-5)',
        title='Average Review Scores by Payment Method',
        labels={'Review Score (1-5)': 'Average Review Score'},
        color='Payment Method',
        color_discrete_sequence=px.colors.qualitative.Set1,
    )

    # Sort the average review scores based on the order of payment counts
    payment_counts = filtered_df["Payment Method"].value_counts().index.tolist()
    average_review_fig.update_xaxes(categoryorder='array', categoryarray=payment_counts)

    # Add annotation for the most common payment method
    if not average_review_scores.empty:
        most_common_payment_method = payment_counts[0]
        mean_review_score = average_review_scores[average_review_scores['Payment Method'] == most_common_payment_method]['Review Score (1-5)'].values[0]

        average_review_fig.add_annotation(
            x=most_common_payment_method,
            y=mean_review_score,
            text="Avg. Review (Most Common): {:.2f}".format(mean_review_score),
            arrowhead=2,
            bgcolor="red",
            font=dict(color="white"),
            bordercolor="red",
            borderwidth=2,
            borderpad=2,
            arrowcolor="red",
            ax=0,
            ay=-40
        )

    # Update layout for better aesthetics
    average_review_fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        font=dict(size=12),
        height=400,
        yaxis_tickformat='.1f'
    )

    # Show the bar chart
    st.plotly_chart(average_review_fig)

# Separator
st.markdown("---")


# Intermediate Insights - Q2
if insight_level == "Intermediate Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Time Spent vs. Purchase Amount</h2>", unsafe_allow_html=True)

    # Create scatter plot for correlation
    fig = px.scatter(
        df, 
        x='Time Spent on Website (min)',  
        y='Purchase Amount ($)',  
        title='Correlation between Time Spent on Website and Purchase Amount',
        labels={
            'Time Spent on Website (min)': 'Time Spent on Website (min)', 
            'Purchase Amount ($)': 'Purchase Amount ($)'
        },
        size='Purchase Amount ($)', 
        color='Time Spent on Website (min)',  
        color_continuous_scale=px.colors.sequential.Plasma 
    )

    # Customizing axis labels and limits
    fig.update_layout(
        xaxis_title='Time Spent on Website (min)',
        yaxis_title='Purchase Amount ($)',
        width=1800  # Set canvas width
    )

    # Show the plot
    st.plotly_chart(fig)



# Intermediate Insights - Q3
if insight_level == "Intermediate Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Customer Satisfaction Among Return Customers</h2>", unsafe_allow_html=True)

    # Calculate satisfied return customers
    satisfied_return_customers = df[(df["Review Score (1-5)"] >= 4) & (df["Return Customer"] == True)]
    num_satisfied_return_customers = len(satisfied_return_customers)

    # Total return customers
    total_return_customers = len(df[df["Return Customer"] == True])

    # Total customers
    total_customers = len(df)

    # Calculate the percentages
    percentage_satisfied_return_customers = (num_satisfied_return_customers / total_return_customers) * 100
    percentage_satisfied_customers = (num_satisfied_return_customers / total_customers) * 100

    # Data for the pie charts
    satisfied_return_count = num_satisfied_return_customers
    not_satisfied_return_count = total_return_customers - num_satisfied_return_customers
    satisfied_total_count = num_satisfied_return_customers
    not_satisfied_total_count = total_customers - num_satisfied_return_customers

    # Create dropdown for pie chart selection
    chart_type = st.selectbox("Select Pie Chart:", options=["All Customers", "Return Customers"], index=0)

    # Create subplots for pie charts
    fig = make_subplots(
        rows=1, cols=1, 
        specs=[[{'type':'pie'}]],  # Only one pie chart to display based on selection
    )

    if chart_type == "Return Customers":
        # Pie chart for return customers
        fig.add_trace(go.Pie(
            labels=['Satisfied Return Customers', 'Not Satisfied Return Customers'],
            values=[satisfied_return_count, not_satisfied_return_count],
            hole=.3,
            marker=dict(colors=px.colors.qualitative.Set1),  # Set1 colors
            textinfo='percent+label',  # Display percentage and label
            textfont=dict(size=14),  # Increase font size for visibility
        ))
        fig.update_layout(title_text='Return Customer Satisfaction', height=400)

    else:  # All Customers
        # Pie chart for all customers
        fig.add_trace(go.Pie(
            labels=['Satisfied & Returning Customers', 'Other Customers'],
            values=[satisfied_total_count, not_satisfied_total_count],
            hole=.3,
            marker=dict(colors=px.colors.qualitative.Set1),  # Set1 colors
            textinfo='percent+label',  # Display percentage and label
            textfont=dict(size=14),  # Increase font size for visibility
        ))
        fig.update_layout(title_text='Overall Customer Satisfaction', height=400)

    # Show the figure in Streamlit
    st.plotly_chart(fig)

    # Streamlit separator
    st.markdown("---")  # Separator

# -------------------------------------------

# Intermediate Insights - Q4
if insight_level == "Intermediate Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Items Purchased vs. Customer Satisfaction</h2>", unsafe_allow_html=True)

    fig = px.scatter(
        df,
        x='Customer Satisfaction',  # Customer satisfaction score
        y='Number of Items Purchased',  # Number of items purchased
        title='Correlation between Number of Items Purchased and Customer Satisfaction',

        size='Number of Items Purchased',  # Optional: Size based on the number of items purchased
        color='Customer Satisfaction',  # Color based on customer satisfaction
        color_discrete_sequence=px.colors.qualitative.Set1,  # Use your preferred color scheme
    )

    # Customize axis labels and limits
    fig.update_layout(
        xaxis_title='Customer Satisfaction Level',
        yaxis_title='Number of Items Purchased'
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Streamlit separator
    st.markdown("---")  # Separator

# -------------------------------------------

# Intermediate Insights - Q5
if insight_level == "Intermediate Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Highest Average Purchase By Location</h2>", unsafe_allow_html=True)

    # Corrected coordinates for cities in Bangladesh
    location_coordinates = {
        'Dhaka': {'lat': 23.8103, 'lon': 90.4125},
        'Chittagong': {'lat': 22.3569, 'lon': 91.7832},
        'Khulna': {'lat': 22.8456, 'lon': 89.5403},
        'Rajshahi': {'lat': 24.3745, 'lon': 88.6042},
        'Sylhet': {'lat': 24.8978, 'lon': 91.8714},
        'Barisal': {'lat': 22.7010, 'lon': 90.3535},
        'Rangpur': {'lat': 25.7439, 'lon': 89.2752},
        'Mymensingh': {'lat': 24.7471, 'lon': 90.4203}
    }

    # Calculate average purchase amount by location
    average_purchase = df.groupby("Location")["Purchase Amount ($)"].mean().reset_index()

    # Get top locations
    top_locations = average_purchase.nlargest(7, "Purchase Amount ($)")

    # Add the latitude and longitude to the top_locations DataFrame
    top_locations['Latitude'] = top_locations['Location'].map(lambda x: location_coordinates[x]['lat'])
    top_locations['Longitude'] = top_locations['Location'].map(lambda x: location_coordinates[x]['lon'])

    # Define ordinal suffixes for the ranks
    ordinal_suffixes = ['st', 'nd', 'rd'] + ['th'] * 4  # Adding 'th' for ranks above 3
    ranks = [f"{i+1}{ordinal_suffixes[i]}" for i in range(len(top_locations))]

    # Create a radio button for selecting the rank of the location
    selected_rank = st.radio("Select the rank of location:", options=ranks, index=1)  # Default to the 2nd highest

    # Get the selected location based on the rank
    selected_index = int(selected_rank[:-2]) - 1  # Extract number and convert to index
    selected_location = top_locations.iloc[selected_index]

    # Get the latitude and longitude for the selected location
    lat = selected_location['Latitude']
    lon = selected_location['Longitude']

    # Create a scatter mapbox using the average purchase amount
    fig = px.scatter_mapbox(
        top_locations, 
        lat='Latitude', 
        lon='Longitude', 
        size='Purchase Amount ($)',  # Use average purchase amount for bubble size
        color='Purchase Amount ($)',  # Use average purchase amount for color
        hover_name='Location',
        hover_data={'Latitude': False, 'Longitude': False, 'Purchase Amount ($)': True},
        title='Average Purchase Amount Heatmap by Location in Bangladesh',
        zoom=6,  # Zoom level focused on Bangladesh
        center={'lat': 23.685, 'lon': 90.3563},  # Center of Bangladesh
        height=600,
        color_continuous_scale=px.colors.sequential.Plasma 
    )

    # Add a marker and annotation for the selected location
    fig.add_trace(go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers+text',
        marker=go.scattermapbox.Marker(size=14, color='red'),  
        showlegend=False
    ))

    # Use open-street-map for the background map style
    fig.update_layout(mapbox_style="open-street-map")

    # Show the map in Streamlit
    st.plotly_chart(fig)


    
# Critical Thinking Insights - Q1
if insight_level == "Critical Thinking Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Factors Influencing Return Customer Classification</h2>", unsafe_allow_html=True)

    # New DataFrame for visualization  
    visualization_df = df.copy()

    # Bin Age
    visualization_df['Age Group'] = pd.cut(visualization_df['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])

    # Bin Time Spent on Website
    visualization_df['Website Engagement Time Group'] = pd.cut(visualization_df['Time Spent on Website (min)'], bins=[0, 5, 10, 20, 30, 60, float('inf')], labels=['0-5', '6-10', '11-20', '21-30', '31-60', '60+'])

    # Bin the 'Purchase Amount ($)' into categories for better visualization
    bins = [0, 50, 100, 200, 500, 1000, 2000, 5000, float('inf')]
    labels = ['0-50', '50-100', '100-200', '200-500', '500-1000', '1000-2000', '2000-5000', '5000+']
    visualization_df['Purchase Amount Group'] = pd.cut(visualization_df['Purchase Amount ($)'], bins=bins, labels=labels, right=False)

    # List of columns excluding the new categories
    factors_columns = ['Gender', 'Location', 'Product Category', 'Device Type', 
                       'Payment Method', 'Discount Availed', 'Number of Items Purchased', 
                       'Review Score (1-5)', 'Delivery Time (days)', 'Subscription Status', 
                       'Customer Satisfaction']

    # Create a Plotly figure with subplots for each factor (3 insights per row)
    num_columns = 3
    num_rows = (len(factors_columns) + 3) // num_columns + 1  # +1 for additional factors

    # Create the subplots
    fig = make_subplots(rows=num_rows, cols=num_columns, 
                        subplot_titles=['Age Group', 'Website Engagement Time Group', 'Purchase Amount Group'] + factors_columns,
                        vertical_spacing=0.1)

    # Age Group
    age_data = visualization_df.groupby('Age Group')['Return Customer'].mean().reset_index()
    fig.add_trace(go.Bar(x=age_data['Age Group'], y=age_data['Return Customer'], name='Age Group'), row=1, col=1)

    # Website Engagement Time Group
    time_data = visualization_df.groupby('Website Engagement Time Group')['Return Customer'].mean().reset_index()
    fig.add_trace(go.Bar(x=time_data['Website Engagement Time Group'], y=time_data['Return Customer'], name='Website Engagement'), row=1, col=2)

    # Purchase Amount Group
    purchase_data = visualization_df.groupby('Purchase Amount Group')['Return Customer'].mean().reset_index()
    fig.add_trace(go.Bar(x=purchase_data['Purchase Amount Group'], y=purchase_data['Return Customer'], name='Purchase Amount'), row=1, col=3)

    # Other Factors
    for i, column in enumerate(factors_columns):
        row = (i // num_columns) + 2  # Start from the second row
        col = (i % num_columns) + 1
        grouped_data = visualization_df.groupby(column)['Return Customer'].mean().reset_index()
        fig.add_trace(
            go.Bar(x=grouped_data[column], y=grouped_data['Return Customer'], name=column),
            row=row, col=col
        )
        fig.update_xaxes(title_text=column, row=row, col=col)
        fig.update_yaxes(title_text='Return Rate', row=row, col=col)

    fig.update_layout(height=1800, width=1200, title_text="Return Rate by Various Factors", showlegend=False)

    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Streamlit separator
    st.markdown("---")  # Separator

# Critical Thinking Insights - Q2
if insight_level == "Critical Thinking Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Impact of Payment Methods on Customer Satisfaction and Return Rates</h2>", unsafe_allow_html=True)

    # Calculate the percentage of each satisfaction level for each payment method
    satisfaction_distribution = df.groupby(['Payment Method', 'Customer Satisfaction']).size().unstack(fill_value=0)
    satisfaction_distribution = satisfaction_distribution.div(satisfaction_distribution.sum(axis=1), axis=0)

    # Calculate return rates
    return_rates = df.groupby('Payment Method')['Return Customer'].mean()

    # Create subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Define colors from Set1 palette
    set1_colors = px.colors.qualitative.Set1

    # Add stacked bar chart for satisfaction levels
    for idx, satisfaction_level in enumerate(['Low', 'Medium', 'High']):
        fig.add_trace(
            go.Bar(x=satisfaction_distribution.index, 
                   y=satisfaction_distribution[satisfaction_level], 
                   name=f'Satisfaction: {satisfaction_level}',
                   text=[f'{val:.1%}' for val in satisfaction_distribution[satisfaction_level]],
                   textposition='inside',
                   marker_color=set1_colors[idx]),  # Set color from Set1 palette
            secondary_y=False
        )

    # Add line chart for return rates with enhanced visibility
    fig.add_trace(
        go.Scatter(x=return_rates.index, y=return_rates.values, 
                   name='Return Rate', mode='lines+markers',
                   line=dict(color='orange', width=3),  # Thicker orange line for better visibility
                   marker=dict(size=10, color='orange', line=dict(color='black', width=1.5)),  # Black border for markers, larger size
                   text=[f'{val:.2%}' for val in return_rates.values],
                   textposition='top center',
                   textfont=dict(size=16, color='black', family='Arial'),  # Increase font size and set color to black
                   texttemplate='<b>%{text}</b>',  # Make text bold for better visibility
                   hoverinfo='text'),
        secondary_y=True
    )

    # Update layout
    fig.update_layout(
        title='Customer Satisfaction Distribution and Return Rates by Payment Method',
        barmode='stack',
        xaxis_title='Payment Method',
        yaxis_title='Proportion of Customers',
        yaxis2_title='Return Rate',
        legend_title='Metrics'
    )

    fig.update_yaxes(tickformat='.0%', secondary_y=False)
    fig.update_yaxes(tickformat='.0%', secondary_y=True)

    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Streamlit separator
    st.markdown("---")  # Separator

# Critical Thinking Insights - Q3
if insight_level == "Critical Thinking Insights":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Location's Influence on Purchase Amount and Delivery Time</h2>", unsafe_allow_html=True)

    # Group by location and calculate metrics
    location_analysis = df.groupby('Location').agg({
        'Purchase Amount ($)': 'mean',
        'Delivery Time (days)': 'mean'
    }).reset_index()

    # Rename columns for clarity
    location_analysis.columns = ['Location', 'Avg Purchase Amount ($)', 'Avg Delivery Time (days)']

    # Create a bubble chart with size based on Average Delivery Time
    fig = px.scatter(location_analysis, 
                     x='Avg Purchase Amount ($)', 
                     y='Avg Delivery Time (days)',
                     size='Avg Delivery Time (days)',  # Size based on average delivery time
                     color='Location',
                     hover_name='Location',
                     text='Location',
                     size_max=30,
                     title='Location Impact on Purchase Amount and Delivery Time',
                     color_continuous_scale=px.colors.qualitative.Set2)  # Choose a color scale

    # Update traces for better visibility
    fig.update_traces(textposition='top center', 
                      marker=dict(line=dict(width=1, color='DarkSlateGrey')))  # Add border around bubbles

    # Update layout for better readability
    fig.update_layout(
        height=600, 
        width=900,
        xaxis_title='Average Purchase Amount ($)',
        yaxis_title='Average Delivery Time (days)',
        legend_title='Location',
        title_x=0.5,  # Center the title
        title_font=dict(size=18),  # Increase title font size
        xaxis=dict(showgrid=True, gridcolor='LightGray'),  # Add grid lines
        yaxis=dict(showgrid=True, gridcolor='LightGray')
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Streamlit separator
    st.markdown("---")  # Separator



# Own Findings - Q1
if insight_level == "Own Findings":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Spending Habits and Return Rates by Age Group</h2>", unsafe_allow_html=True)

    # Create age groups
    df['Age_Group'] = pd.cut(df['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])

    # Calculate average spending and return rate for each age group
    age_group_stats = df.groupby('Age_Group').agg({
        'Purchase Amount ($)': 'mean',
        'Return Customer': 'mean'
    }).reset_index()

    age_group_stats['Return Rate'] = age_group_stats['Return Customer'] * 100

    # Define Set1 color palette
    set1_colors = px.colors.qualitative.Set1

    # Create the figure
    fig = go.Figure()

    # Add bar chart for average purchase amount using Set1 colors
    fig.add_trace(go.Bar(
        x=age_group_stats['Age_Group'],
        y=age_group_stats['Purchase Amount ($)'],
        name='Avg. Purchase Amount',
        marker_color=set1_colors[1],  # Set color for bars
        yaxis='y',
        offsetgroup=1
    ))

    # Add line chart for return rate with Set1 colors
    fig.add_trace(go.Scatter(
        x=age_group_stats['Age_Group'],
        y=age_group_stats['Return Rate'],
        name='Return Rate',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='orange', width=3),  # Orange line with a bit more width
        marker=dict(size=10, color='orange', line=dict(color='black', width=1.5))  # Black border for markers
    ))

    # Update the layout
    fig.update_layout(
        #title='Spending Habits and Return Rates by Age Group',
        xaxis=dict(title='Age Group'),
        yaxis=dict(title='Average Purchase Amount ($)', side='left', showgrid=False),
        yaxis2=dict(title='Return Rate (%)', side='right', overlaying='y', showgrid=False),
        legend=dict(x=1.1, y=1, bgcolor='rgba(255, 255, 255, 0.5)'),
        barmode='group',
        height=600,
        width=1000
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Streamlit separator
    st.markdown("---")  # Separator

# Own Findings - Q2
if insight_level == "Own Findings":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Product Category Preferences by Location</h2>", unsafe_allow_html=True)

    # Get unique locations and product categories
    locations = df['Location'].unique()
    product_categories = df['Product Category'].unique()

    # Create a cross-tabulation of Location and Product Category
    location_product_counts = pd.crosstab(df['Location'], df['Product Category'])

    # Calculate the percentage of each product category within each location
    location_product_percentages = location_product_counts.div(location_product_counts.sum(axis=1), axis=0) * 100

    # Create a heatmap with annotations
    fig = px.imshow(location_product_percentages,
                    labels=dict(x="Product Category", y="Location", color="Percentage"),
                    x=location_product_percentages.columns,
                    y=location_product_percentages.index,
                    color_continuous_scale="Viridis",
                    text_auto=True)  # Add annotations

    fig.update_layout(#title="Product Category Preferences by Location",
                      xaxis_title="Product Category",
                      yaxis_title="Location",
                      height=1000, 
                      width=1000)

    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Streamlit separator
    st.markdown("---")  # Separator

# Own Findings - Q3
if insight_level == "Own Findings":
    st.markdown("<h2 style='text-align: center; color: #1ABC9C;'>Average Spending by Product Category and Gender</h2>", unsafe_allow_html=True)

    # Group the data by Product Category and Gender, then calculate the average purchase amount
    product_gender_stats = df.groupby(['Product Category', 'Gender'])['Purchase Amount ($)'].mean().unstack()

    # Sort the product categories by the total average purchase amount across genders
    sorted_product_gender_stats = product_gender_stats.loc[
        product_gender_stats.mean(axis=1).sort_values(ascending=False).index
    ]

    # Create a bar plot using Set1 colors
    fig = px.bar(sorted_product_gender_stats, 
                 #title='Average Spending by Product Category and Gender',
                 labels={'value': 'Average Purchase Amount ($)', 'Product Category': 'Product Category'},
                 barmode='group',
                 color_discrete_sequence=set1_colors  # Set color palette to Set1
                 )  

    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Product Category',
        yaxis_title='Average Purchase Amount ($)',
        xaxis_tickangle=-45,
        legend_title='Gender',
        template='plotly_white',  # Change the template for a cleaner look
        height=600  # Increase height for better visibility
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Streamlit separator
    st.markdown("---")  # Separator

  


else:
    st.info("Please upload a CSV file to get started.")
