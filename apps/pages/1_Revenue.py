import streamlit as st
import pandas as pd
import plotly.express as px
from script.gold.gold_payments import KpiCalculator


st.set_page_config(page_title='Revenues', layout='wide')
st.write(
    f"""
    <div style="text-align:center">
        <h1>Revenues</h1>
    </div>
    """,
    unsafe_allow_html=True
)

calculator = KpiCalculator('data/cleaned_payments.csv')

st.markdown("## Global Analysis")
total_revenue = calculator.total_revenue()
average_order_value = calculator.average_order_value()
max_order_value = calculator.max_order_value()
min_order_value = calculator.min_order_value()

col1, col2 = st.columns(2)
with col1:
    st.metric('Average Order Value', f"${average_order_value:.2f}")
    st.metric('Max Order Value', f"${max_order_value:.2f}")
with col2:
    st.metric('Min Order Value', f"${min_order_value:.2f}")
    st.metric('Total Revenue', f"${total_revenue:.2f}")


# use revenues_per_month() to get the data
revenues_per_month = calculator.revenues_per_month()
revenues_per_month.index = revenues_per_month.index.astype(str)  # Convert Period index to string
fig_revenue_per_month = px.bar(revenues_per_month, x=revenues_per_month.index, y='payment_value', title='Revenues per Month', labels={'payment_value': 'Payment Value'})

# Add text annotations for each data point
for i, value in enumerate(revenues_per_month):
    fig_revenue_per_month.add_annotation(x=revenues_per_month.index[i], y=value, text=f"${value:.2f}", showarrow=True, arrowhead=2)

# Display the plot in Streamlit
# use revenues_per_year() to get the data
revenues_per_year = calculator.revenues_per_year()
revenues_per_year.index = revenues_per_year.index.astype(str)  # Convert Period index to string
# Create a line plot using Plotly Express
fig_payment_value_year = px.bar(revenues_per_year, x=revenues_per_year.index, y='payment_value', 
                                  title='Revenues per Year', labels={'payment_value': 'Payment Value'},
                                  text=revenues_per_year.values.round(2))

# Update text position
#fig_payment_value_year.update_traces(textposition='top center')
st.plotly_chart(fig_revenue_per_month, use_container_width=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_payment_value_year, use_container_width=True)
    # revenues_per_payment_type_per_year() to get the data

with col2:
    revenues_per_payment_type = calculator.revenues_per_payment_type()
    # Create a pie chart using Plotly Express
    fig = px.pie(revenues_per_payment_type, values='payment_value', names=revenues_per_payment_type.index, 
                title='Revenues per Payment Type')
    st.plotly_chart(fig, use_container_width=True)
    

st.markdown("## Regional Analysis")
col1, col2 = st.columns(2)
# Displaying Sales per State as a bar chart
result = calculator.best_region()
sales_per_state = result['Sales per state']
# Convert 'payment_value' column to numeric
sales_per_state['payment_value'] = pd.to_numeric(sales_per_state['payment_value'])

# Calculate total sales
total_sales = sales_per_state['payment_value'].sum()

# Calculate percentage
sales_per_state['percentage'] = (sales_per_state['payment_value'] / total_sales) * 100

# Format the text to be displayed on the bars
sales_per_state['text'] = sales_per_state.apply(lambda row: f"${row['payment_value']:.2f} ({row['percentage']:.2f}%)", axis=1)

# Plot the bar chart with data labels and percentages
fig_sales_per_state = px.bar(sales_per_state, x='customer_state', y='payment_value', 
             text='text', text_auto=True, labels={'payment_value': 'Payment Value'})

# Update the layout to adjust the font size of the labels
fig_sales_per_state.update_traces(texttemplate='%{text}', textposition='outside')
fig_sales_per_state.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')


# Displaying Customers per State as a bar chart
result = calculator.must_customer_region()
customers_per_state = result['Customers per state']
fig_customers_per_state = px.bar(customers_per_state, x=customers_per_state.index, y='Customers_per_states', labels={'Customers_per_states': 'Number of Customers'})
col1, col2 = st.columns(2)
with col1:
    st.markdown('<h3 style="text-align: center;">Revenues per State</h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_sales_per_state, use_container_width=True)
with col2:
    st.markdown('<h3 style="text-align: center;">Customers per State</h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_customers_per_state, use_container_width=True)

regions = sales_per_state['customer_state'].unique()
# Select a region
selected_region = st.selectbox('Select a region', regions)

# Filter data for the selected region
selected_region_data = calculator.revenues_per_state_per_year(selected_region)

# Convert 'order_purchase_timestamp' to datetime
#selected_region_data['order_purchase_timestamp'] = pd.to_datetime(selected_region_data['order_purchase_timestamp'])

# Extract year from 'order_purchase_timestamp'
selected_region_data['Year'] = selected_region_data['order_purchase_timestamp'].dt.year.astype(str)

# Select only the required columns
selected_data = selected_region_data[['Year', 'payment_value']]

# Create a line chart using Plotly Express
fig_revenue_per_state_per_year = px.bar(selected_data, x='Year', y='payment_value')

# Update layout of the chart
fig_revenue_per_state_per_year.update_layout(
    title="Revenue per State per Year",
    xaxis_title="Year",
    yaxis_title="Payment Value",
    showlegend=False  # Optional: to hide the legend
)

# Display the line chart
st.plotly_chart(fig_revenue_per_state_per_year, use_container_width=True)