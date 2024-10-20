import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Home Page Title and Description
st.title("E-commerce Customer Behavior Dashboard")
st.subheader("Explore insights into customer behavior, purchasing patterns, and satisfaction.")

# Introduction Text
st.write("""
Welcome to the interactive dashboard that provides insights into e-commerce customer behavior. 
This dashboard is divided into three levels of insights:
- **Basic Insights**: Get an overview of basic customer metrics and patterns.
- **Intermediate Insights**: Dive deeper into customer correlations and behaviors.
- **Critical Thinking Insights**: Explore more complex analyses, uncovering deeper business insights.
""")

# Data Upload Section
st.header("Upload Your Dataset")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Load DataFrame if a file is uploaded
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Data loaded successfully!")

    # Navigation Section
    st.markdown("## Select Insight Level")
    insight_level = st.selectbox("Choose Insight Level", ["Basic Insights", "Intermediate Insights", "Critical Thinking Insights","Own Findings"])

    # Basic Insights - Q1
    if insight_level == "Basic Insights":
        st.markdown("### Q1: Find Mean, Median, and Mode (Age)")

        if 'Age' in df.columns:
            age_mean = df['Age'].mean()
            age_median = df['Age'].median()
            age_mode = df['Age'].mode()[0]

            # Creating a single figure
            fig = go.Figure()

            # Adding histogram
            fig.add_trace(go.Histogram(x=df['Age'], name="Age Distribution", opacity=0.7))

            # Adding vertical lines for mean, median, and mode
            fig.add_vline(x=age_mean, line_dash="dash", line_color="red")
            fig.add_vline(x=age_median, line_dash="dash", line_color="green")
            fig.add_vline(x=age_mode, line_dash="dash", line_color="blue")

            # Add annotations
            fig.add_annotation(
                x=age_mean, y=df['Age'].value_counts().max() * 0.9,
                text=f"Mean: {age_mean:.2f}",
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
                x=age_median, y=df['Age'].value_counts().max() * 0.9,
                text=f"Median: {age_median:.2f}",
                arrowhead=2,
                bgcolor="green",
                font=dict(color="white"),
                bordercolor="green",
                borderwidth=2,
                borderpad=2,
                arrowcolor="green",
                ax=60, ay=-20  
            )

            fig.add_annotation(
                x=age_mode, y=df['Age'].value_counts().max() * 0.9,
                text=f"Mode: {age_mode}",
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
            st.error("The uploaded dataset does not contain an 'Age' column.")

    # Basic Insights - Q2
    if insight_level == "Basic Insights":
        st.markdown("### Q2: Find Variance, Standard Deviation, and Z-Score (Purchase Amount)")

        if 'Purchase Amount ($)' in df.columns:
            purchase_amount = df['Purchase Amount ($)']
            variance = np.var(purchase_amount)
            std_dev = np.std(purchase_amount)
            mean_purchase_amount = np.mean(purchase_amount)
            z_scores = (purchase_amount - mean_purchase_amount) / std_dev

            # Create a subplot with 3 rows
            fig = go.Figure()

            # Row 1: Purchase Amount Distribution (Variance)
            fig.add_trace(go.Histogram(x=purchase_amount, name='Purchase Amount', 
                                         marker_color='lightblue', opacity=0.75))

            fig.add_vline(x=mean_purchase_amount, line_dash="dash", line_color="red", 
                           annotation_text="Mean", annotation_position="top right")
            fig.add_vline(x=mean_purchase_amount + np.sqrt(variance), line_dash="dash", line_color="blue",
                           annotation_text="Mean + √Variance", annotation_position="top right")
            fig.add_vline(x=mean_purchase_amount - np.sqrt(variance), line_dash="dash", line_color="blue",
                           annotation_text="Mean - √Variance", annotation_position="top right")

            # Update layout
            fig.update_layout(height=400, width=700, title_text="Purchase Amount Distribution (Variance)",
                              xaxis_title="Purchase Amount ($)", yaxis_title="Count", showlegend=False)

            # Show plot
            st.plotly_chart(fig)

            # Print summary statistics
            st.write(f"Variance: {variance:.2f}")
            st.write(f"Standard Deviation: {std_dev:.2f}")
            st.write(f"Z-score range: {z_scores.min():.2f} to {z_scores.max():.2f}")
        else:
            st.error("The uploaded dataset does not contain a 'Purchase Amount ($)' column.")

    # Basic Insights - Q3
    if insight_level == "Basic Insights":
        st.markdown("### Q3: What are the Top Three Product Categories Based on the Number of Purchases?")

        if 'Product Category' in df.columns and 'Number of Items Purchased' in df.columns:
            top_3 = df.groupby("Product Category")["Number of Items Purchased"].sum().sort_values(ascending=False)

            # Create the bar chart
            fig = px.bar(
                top_3,
                x=top_3.index,
                y=top_3.values,
                labels={'x': 'Product Category', 'y': 'Count'},
                title='Top 3 Product Categories',
                color=top_3.index,
            )

            # Annotations for the top 3 categories
            annotations = ['1st', '2nd', '3rd']

            # Ensure we only add annotations for the number of bars available (up to 3)
            for i in range(min(3, len(top_3))):  # Iterate only for the number of available bars (max 3)
                fig.add_annotation(
                    x=top_3.index[i],  # Category label
                    y=top_3.values[i],  # Value of the bar
                    text=f'{annotations[i]} Place',  # Add custom ranking labels (1st, 2nd, 3rd)
                    showarrow=True,  # Show an arrow pointing to the bar
                    arrowhead=2,
                    ax=0, ay=-40,  # Adjust arrow positioning
                    font=dict(size=14, color="white"),  # Font size and color
                    bgcolor="red",  # Background color of the annotation box
                    bordercolor="red",  # Border color for visibility
                    borderwidth=2,  # Border width
                    borderpad=4,  # Padding within the annotation box
                    arrowcolor="red"  # Arrow color matching the box
                )

            # Show the plot
            st.plotly_chart(fig)
        else:
            st.error("The uploaded dataset does not contain the required columns for product categories and item counts.")

    # Basic Insights - Q4
    if insight_level == "Basic Insights":
        st.markdown("### Q4: How Many Customers are Classified as Return Customers?")

        if 'Return Customer' in df.columns and 'Gender' in df.columns:
            # First chart: Count of Return Customers vs. Non-Return Customers
            return_customer_counts = df['Return Customer'].value_counts()
            total_customers = return_customer_counts.sum()
            return_customer_percentages = (return_customer_counts / total_customers * 100).round(2)  # Calculate percentages to 2 decimal places

            # Second chart: Distribution of Return Customers by Gender
            return_customers_by_gender = df[df['Return Customer'] == True].groupby('Gender').size().reset_index(name='Count')
            total_return_customers = return_customers_by_gender['Count'].sum()
            return_customers_by_gender['Percentage'] = (return_customers_by_gender['Count'] / total_return_customers * 100).round(2)

            # Create subplots with 2 rows and 1 column
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=(
                    'Count of Return Customers vs. Non-Return Customers', 
                    'Distribution of Return Customers by Gender'
                ),
                vertical_spacing=0.15  # Increase space between rows
            )

            # First chart (Return vs. Non-Return Customers) - add trace to first row
            fig.add_trace(
                go.Bar(
                    x=return_customer_counts.index.map({True: 'Return Customers', False: 'Non-Return Customers'}), 
                    y=return_customer_counts.values, 
                    marker_color=px.colors.qualitative.Set1, 
                    text=[f'{count} ({percent:.2f}%)' for count, percent in zip(return_customer_counts.values, return_customer_percentages)],  # Add count and percentage (2 decimal points)
                    textposition='auto',
                    name="Return vs Non-Return"
                ),
                row=1, col=1
            )

            # Second chart (Return Customers by Gender) - add trace to second row
            fig.add_trace(
                go.Bar(
                    x=return_customers_by_gender['Gender'], 
                    y=return_customers_by_gender['Count'], 
                    marker_color=px.colors.qualitative.Set1, 
                    text=[f'{count} ({percent:.2f}%)' for count, percent in zip(return_customers_by_gender['Count'], return_customers_by_gender['Percentage'])],  # Add count and percentage (2 decimal points)
                    textposition='auto',
                    name="Return Customers by Gender"
                ),
                row=2, col=1
            )

            # Update layout and customize aesthetics
            fig.update_layout(
                height=800,  # Height of the plot
                title_text="Return Customer Analysis",  # Overall title
                title_x=0.5,  # Center title
                title_font=dict(size=24, family='Arial, bold'),  # Make the main title bigger
                showlegend=False,  # No need for legend since charts are separate
                plot_bgcolor='white',  # Background color
                xaxis=dict(showgrid=False),  # No vertical gridlines
                yaxis=dict(showgrid=False),  # No horizontal gridlines
                margin=dict(l=50, r=50, t=100, b=50),  # Margins for clarity
                font=dict(family="Arial", size=14)  # General font for text
            )

            # Improve the look of the bars with lines
            fig.update_traces(marker_line_color='black', marker_line_width=1.5)

            # Change subplot title styles
            fig.update_annotations(
                dict(
                    font_size=18, 
                    font_family="Arial, bold",
                    yshift=10  # Shift titles upwards for clarity
                )
            )

            # Add background shading to the second plot for contrast
            fig.add_shape(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=0.45,  # Covers the second plot area
                fillcolor="lightgrey", opacity=0.2, line_width=0
            )

            # Display the combined chart
            st.plotly_chart(fig)
        else:
            st.error("The uploaded dataset does not contain the required columns for return customers and gender.")

    # Basic Insights - Q5
    if insight_level == "Basic Insights":
        st.markdown("### Q5: What is the Average Review Score Given by Customers?")

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
                title_text="Average Review Score Distribution",
                xaxis_title_text="Review Score (1-5)",
                yaxis_title_text="Count",
                bargap=0.2,
                showlegend=False
            )

            # Show the plot
            st.plotly_chart(fig)
        else:
            st.error("The uploaded dataset does not contain a 'Review Score (1-5)' column.")

    # Basic Insights - Q6
    if insight_level == "Basic Insights":
        st.markdown("### Q6: How Does the Average Delivery Time Vary Between Subscription Statuses?")

        if 'Subscription Status' in df.columns and 'Delivery Time (days)' in df.columns:
            # Create a DataFrame for visualization
            avg_delivery_time = df.groupby("Subscription Status")["Delivery Time (days)"].mean().reset_index()

            # Create a vertical bar chart
            bar_fig = px.bar(
                avg_delivery_time,
                x='Delivery Time (days)',
                y='Subscription Status',
                title='Average Delivery Time by Subscription Status',
                labels={'Delivery Time (days)': 'Average Delivery Time (days)', 'Subscription Status': 'Subscription Status'},
                color='Subscription Status',
                color_discrete_sequence=px.colors.qualitative.Set1,  # Use a color sequence
                orientation='h'  # Horizontal bar chart
            )

            # Show the vertical bar chart
            st.plotly_chart(bar_fig)
        else:
            st.error("The uploaded dataset does not contain the required columns for subscription status and delivery time.")

    # Basic Insights - Q7
    if insight_level == "Basic Insights":
        st.markdown("### Q7: How Many Customers are Subscribed to the Service?")

        if 'Subscription Status' in df.columns:
            # Prepare the data for visualization
            subscription_counts = df["Subscription Status"].value_counts().reset_index()
            subscription_counts.columns = ['Subscription Status', 'Count']

            # Create a bar chart
            bar_fig = px.bar(
                subscription_counts,
                x='Subscription Status',
                y='Count',
                title='Number of Customers by Subscription Status',
                labels={'Count': 'Number of Customers'},
                color='Subscription Status',
                color_discrete_sequence=px.colors.qualitative.Set1,
            )

            # Show the bar chart
            st.plotly_chart(bar_fig)
        else:
            st.error("The uploaded dataset does not contain a 'Subscription Status' column.")
            
        # Basic Insights - Q8
if insight_level == "Basic Insights":
    st.markdown("### Q8: What Percentage of Customers Used Devices to Make Purchases? (Mobile, Desktop, Tablet)")

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
            title='Percentage of Customers by Device Type',
            color='Device Type',
            color_discrete_sequence=px.colors.qualitative.Set1,
            hole=0.3  # To make it a donut chart
        )

        # Add annotations to the pie chart
        pie_fig.update_traces(textinfo='percent+label', textfont_size=14)

        # Update layout for better aesthetics
        pie_fig.update_layout(
            title_font_size=20,
            legend_title_text='Device Type'
        )

        # Show the pie chart
        st.plotly_chart(pie_fig)
    else:
        st.error("The uploaded dataset does not contain a 'Device Type' column.")
        
    # Basic Insights - Q9
if insight_level == "Basic Insights":
    st.markdown("### Q9: What is the Average Purchase Amount for Customers Who Availed Discounts Compared to Those Who Didn’t?")

    if 'Discount Availed' in df.columns and 'Purchase Amount ($)' in df.columns:
        # Calculate average purchase amount based on discount status
        avg_purchase = df.groupby("Discount Availed")["Purchase Amount ($)"].mean().reset_index()

        # Map True/False to meaningful labels
        avg_purchase['Discount Availed'] = avg_purchase['Discount Availed'].map({True: 'Discount', False: 'No Discount'})

        # Create a bar chart
        bar_fig = px.bar(
            avg_purchase,
            x='Discount Availed',
            y='Purchase Amount ($)',
            title='Average Purchase Amount Based on Discount Availed',
            labels={'Discount Availed': 'Discount Status', 'Purchase Amount ($)': 'Average Amount'},
            color='Discount Availed',
            color_discrete_sequence=px.colors.qualitative.Set1,
        )

        # Adding data labels on top of the bars
        bar_fig.update_traces(
            texttemplate='%{y:.2f}', 
            textposition='outside',
            marker=dict(line=dict(width=1, color='black')),
            textfont_size=12  # Adjust text size for labels
        )

        # Update layout for better aesthetics
        bar_fig.update_layout(
            title_font_size=20,  # Title font size
            xaxis_title_font_size=14,  # X-axis title font size
            yaxis_title_font_size=14,  # Y-axis title font size
            font=dict(size=12),  # General font size
            xaxis=dict(title=dict(standoff=10)),  # Space between x-axis title and labels
            yaxis=dict(title=dict(standoff=10)),  # Space between y-axis title and labels
            showlegend=False,  # Hide the legend since it's not needed
            height=500  # Adjust height for better visibility
        )

        # Show the bar chart
        st.plotly_chart(bar_fig)
    else:
        st.error("The uploaded dataset does not contain the required columns: 'Discount Availed' or 'Purchase Amount ($)'.")
        
    # Basic Insights - Q10
if insight_level == "Basic Insights":
    st.markdown("### Q10: What is the Most Common Payment Method Used by Customers?")

    if 'Payment Method' in df.columns:
        # Count occurrences of each payment method
        payment_counts = df["Payment Method"].value_counts().reset_index()
        payment_counts.columns = ['Payment Method', 'Count']

        # Create a bar chart
        payment_fig = px.bar(
            payment_counts,
            x='Payment Method',
            y='Count',
            title='Most Common Payment Methods Used by Customers',
            labels={'Payment Method': 'Payment Method', 'Count': 'Number of Customers'},
            color='Payment Method',
            color_continuous_scale=px.colors.sequential.Viridis,
        )

        # Adding annotation for the most common payment method
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
            ax=0,  # Adjust position as needed
            ay=-40  # Adjust position as needed
        )

        # Update layout for better aesthetics
        payment_fig.update_layout(
            title_font_size=20,  # Title font size
            xaxis_title_font_size=14,  # X-axis title font size
            yaxis_title_font_size=14,  # Y-axis title font size
            font=dict(size=12),  # General font size
            showlegend=False,  # Hide the legend since it's not needed
            height=400  # Adjust height for better visibility
        )

        # Show the bar chart
        st.plotly_chart(payment_fig)
    else:
        st.error("The uploaded dataset does not contain the required column: 'Payment Method'.")
        
# Intermediate Insights - Q1
if insight_level == "Intermediate Insights":
    st.markdown("### Q1: What are the average review scores of users of the most common payment method?")

    # Calculate the average review score for each payment method
    average_review_scores = df.groupby("Payment Method")["Review Score (1-5)"].mean().reset_index()

    # Create a bar chart for average review scores
    average_review_fig = px.bar(
        average_review_scores,
        x='Payment Method',
        y='Review Score (1-5)',
        title='Average Review Scores by Payment Method',
        labels={'Review Score (1-5)': 'Average Review Score'},
        color='Payment Method',
        color_continuous_scale=px.colors.sequential.YlGnBu,
    )

    # Sort the average review scores based on the order of payment counts
    payment_counts = df["Payment Method"].value_counts().index.tolist()
    average_review_fig.update_xaxes(categoryorder='array', categoryarray=payment_counts)

    # Add annotation for the most common payment method
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
    
# Intermediate Insights - Q2
if insight_level == "Intermediate Insights":
    st.markdown("### Q2: What is the correlation between time spent on the website and purchase amount? Do customers who spend more time on the website purchase more items?")

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
    st.plotly_chart(fig)  # Use st.plotly_chart to display the figure in Streamlit
    
    # Intermediate Insights - Q3
if insight_level == "Intermediate Insights":
    st.markdown("### Q3: What percentage of customers are satisfied (rating of 4 or 5) and are also returncustomers?")

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

    # Print the results (you can also display these in Streamlit if needed)
    print(f"Percentage of satisfied return customers: {percentage_satisfied_return_customers:.2f}%")
    print(f"Percentage of satisfied customers among all customers: {percentage_satisfied_customers:.2f}%")

    # Data for the pie charts
    satisfied_return_count = num_satisfied_return_customers
    not_satisfied_return_count = total_return_customers - num_satisfied_return_customers
    satisfied_total_count = num_satisfied_return_customers
    not_satisfied_total_count = total_customers - num_satisfied_return_customers

    # Create subplots for pie charts
    fig = make_subplots(
        rows=1, cols=2, 
        specs=[[{'type':'pie'}, {'type':'pie'}]],
        subplot_titles=('Return Customers', 'All Customers')
    )

    # Pie chart for return customers
    fig.add_trace(go.Pie(
        labels=['Satisfied Return Customers', 'Not Satisfied Return Customers'],
        values=[satisfied_return_count, not_satisfied_return_count],
        hole=.3,
        marker=dict(colors=['green', 'red']),  # Maintain your colors
    ), row=1, col=1)

    # Pie chart for all customers
    fig.add_trace(go.Pie(
        labels=['Satisfied & Returning Customers', 'Other Customers'],
        values=[satisfied_total_count, not_satisfied_total_count],
        hole=.3,
        marker=dict(colors=['blue', 'orange']),  # Maintain your colors
    ), row=1, col=2)

    # Update layout
    fig.update_layout(
        title_text='Customer Satisfaction Analysis',
        height=400,  # Adjust height if needed
    )

    # Show the figure in Streamlit
    st.plotly_chart(fig)  # Use st.plotly_chart to display the figure in Streamlit
    
# Intermediate Insights - Q4
if insight_level == "Intermediate Insights":
    st.markdown("### Q4: What is the relationship between the number of items purchased and customer satisfaction?")

    import plotly.express as px

    # Create a scatter plot for the relationship between items purchased and customer satisfaction
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

# Intermediate Insights - Q5
if insight_level == "Intermediate Insights":
    st.markdown("### Q5: Which location has the 2nd highest average purchase amount?")



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

    # Add the latitude and longitude to the DataFrame
    df['Latitude'] = df['Location'].map(lambda x: location_coordinates[x]['lat'])
    df['Longitude'] = df['Location'].map(lambda x: location_coordinates[x]['lon'])

    # Calculate average purchase amount by location
    average_purchase = df.groupby("Location")["Purchase Amount ($)"].mean().reset_index()

    # Merge average purchase with location coordinates
    merged_df = pd.merge(average_purchase, df[['Location', 'Latitude', 'Longitude']].drop_duplicates(), on="Location")

    # Get the location with the second highest average purchase amount
    second_highest_location = merged_df.nlargest(2, "Purchase Amount ($)").iloc[-1]

    # Create a scatter mapbox using the average purchase amount
    fig = px.scatter_mapbox(
        merged_df, 
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
        color_continuous_scale=px.colors.sequential.Plasma  # Set your preferred color scale
    )

    # Add a marker and annotation for the second-highest location using graph_objects
    fig.add_trace(go.Scattermapbox(
        lat=[second_highest_location['Latitude']],
        lon=[second_highest_location['Longitude']],
        mode='markers+text',
        marker=go.scattermapbox.Marker(size=14, color='red'),  # Use red color for the marker
        text=f"2nd Highest: {second_highest_location['Location']}",
        textposition="bottom right",
        textfont=dict(color='black'),  # Set text color for the annotation
        showlegend=False
    ))

    # Use open-street-map for the background map style
    fig.update_layout(mapbox_style="open-street-map")

    # Show the map in Streamlit
    st.plotly_chart(fig)
    
# Critical Thinking Insights - Q1
if insight_level == "Critical Thinking Insights":
    st.markdown("### Q1: What factors contribute most to a customer being classified as a return customer?")

    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

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

# Critical Thinking Insights - Q2
if insight_level == "Critical Thinking Insights":
    st.markdown("### Q2: How do payment methods influence customer satisfaction and return rates?")

    # Calculate the percentage of each satisfaction level for each payment method
    satisfaction_distribution = df.groupby(['Payment Method', 'Customer Satisfaction']).size().unstack(fill_value=0)
    satisfaction_distribution = satisfaction_distribution.div(satisfaction_distribution.sum(axis=1), axis=0)

    # Calculate return rates
    return_rates = df.groupby('Payment Method')['Return Customer'].mean()

    # Create subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add stacked bar chart for satisfaction levels
    for satisfaction_level in ['Low', 'Medium', 'High']:
        fig.add_trace(
            go.Bar(x=satisfaction_distribution.index, 
                   y=satisfaction_distribution[satisfaction_level], 
                   name=f'Satisfaction: {satisfaction_level}',
                   text=[f'{val:.1%}' for val in satisfaction_distribution[satisfaction_level]],
                   textposition='inside'),
            secondary_y=False
        )

    # Add line chart for return rates
    fig.add_trace(
        go.Scatter(x=return_rates.index, y=return_rates.values, 
                   name='Return Rate', mode='lines+markers',
                   line=dict(color='red', width=2),
                   marker=dict(size=8),
                   text=[f'{val:.2%}' for val in return_rates.values],
                   textposition='top center'),
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

# Critical Thinking Insights - Q3
if insight_level == "Critical Thinking Insights":
    st.markdown("### Q3: How does the location influence both purchase amount and delivery time?")

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

# Own Findings - Q1
if insight_level == "Own Findings":
    st.markdown("### Q1: What are the spending habits of different age groups, and how does this influence their return rates?")

    # Create age groups
    df['Age_Group'] = pd.cut(df['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])

    # Calculate average spending and return rate for each age group
    age_group_stats = df.groupby('Age_Group').agg({
        'Purchase Amount ($)': 'mean',
        'Return Customer': 'mean'
    }).reset_index()

    age_group_stats['Return Rate'] = age_group_stats['Return Customer'] * 100

    # Create the figure
    fig = go.Figure()

    # Add bar chart for average purchase amount
    fig.add_trace(go.Bar(
        x=age_group_stats['Age_Group'],
        y=age_group_stats['Purchase Amount ($)'],
        name='Avg. Purchase Amount',
        yaxis='y',
        offsetgroup=1
    ))

    # Add line chart for return rate
    fig.add_trace(go.Scatter(
        x=age_group_stats['Age_Group'],
        y=age_group_stats['Return Rate'],
        name='Return Rate',
        yaxis='y2',
        mode='lines+markers'
    ))

    # Update the layout
    fig.update_layout(
        title='Spending Habits and Return Rates by Age Group',
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

# Own Findings - Q2
if insight_level == "Own Findings":
    st.markdown("### Q2: How do product preferences vary across different locations?")

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

    fig.update_layout(title="Product Category Preferences by Location",
                      xaxis_title="Product Category",
                      yaxis_title="Location",
                      height=1000, 
                      width=1000)

    # Show the plot in Streamlit
    st.plotly_chart(fig)

# Own Findings - Q3
if insight_level == "Own Findings":
    st.markdown("### Q3: How do purchasing patterns differ between genders in terms of product categories and average spend?")

    # Group the data by Product Category and Gender, then calculate the average purchase amount
    product_gender_stats = df.groupby(['Product Category', 'Gender'])['Purchase Amount ($)'].mean().unstack()

    # Sort the product categories by the total average purchase amount across genders
    sorted_product_gender_stats = product_gender_stats.loc[
        product_gender_stats.mean(axis=1).sort_values(ascending=False).index
    ]

    # Create a bar plot
    fig = px.bar(sorted_product_gender_stats, 
                 title='Average Spending by Product Category and Gender',
                 labels={'value': 'Average Purchase Amount ($)', 'Product Category': 'Product Category'},
                 barmode='group'
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








    


else:
    st.info("Please upload a CSV file to get started.")
