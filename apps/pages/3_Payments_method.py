import streamlit as st
import pandas as pd
import plotly.express as px
from script.gold.gold_payments import KpiCalculator

st.set_page_config(page_title='Payments method', layout='wide')
st.write(
    f"""
    <div style="text-align:center">
        <h1>Payments method</h1>
    </div>
    """,
    unsafe_allow_html=True
)


calculator = KpiCalculator('data/cleaned_payments.csv')

# Function to convert payment type string to human-readable format


def format_payment_type(payment_type):
    return payment_type.replace("_", " ").capitalize()


# Displaying the analysis of most used payment methods using st.metrics
st.write('## [Global] Analysis of most used payment methods')
st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.warning(
    "Please note that only percentages greater than or equal to 1% are displayed.")

result = calculator.best_payment_method()
col1, col2 = st.columns(2)
for key, value in result.items():
    if key == 'Payment type usage':
        total_orders = sum(value)
        for payment_type, count in value.items():
            percentage = (count / total_orders) * 100
            if percentage >= 1:  # Check if percentage is greater than or equal to 1
                delta_percentage = f"{percentage:.2f}%"
                formatted_payment_type = format_payment_type(payment_type)
                if payment_type in ['credit_card', 'boleto']:
                    col1.metric(
                        formatted_payment_type,
                        value=count,
                        delta=delta_percentage)
                else:
                    col2.metric(
                        formatted_payment_type,
                        value=count,
                        delta=delta_percentage)

    else:
        col1.metric(key, value)

st.header('Regional Analysis')
st.info(
    "In this section, we will analyze the payment methods per region, sales per state, customers per state, and order status.\n\n"
    "To enhance your analysis, you can filter the data by state using the dropdown menu provided.")
# Displaying the analysis of payment methods per region using charts
st.write('### Analysis of payment methods')
result = calculator.payments_method_per_region()
payment_type_usage = result['Payment type usage']
payment_type_usage = payment_type_usage.unstack().fillna(0)

# Add a select box for choosing a region
selected_region = st.selectbox('Select Region', payment_type_usage.index)

# Filter the data for the selected region
selected_region_data = payment_type_usage.loc[selected_region]

# Create a pie chart for the selected region with labels as percentages
fig = px.pie(
    selected_region_data,
    values=selected_region_data.values,
    names=selected_region_data.index,
    title=f'Payment Methods for {selected_region}',
    labels={
        'value': 'Percentage'})
st.plotly_chart(fig, use_container_width=True)


# Displaying Sales per State as a bar chart
st.header('Sales per state')
result = calculator.best_region()
sales_per_state = result['Sales per state']
sales_per_state = sales_per_state.sort_values(
    by='payment_value', ascending=True)  # Sort in ascending order
fig = px.bar(
    sales_per_state,
    x='customer_state',
    y='payment_value',
    title='Sales per State',
    labels={
        'payment_value': 'Payment Value'})
st.plotly_chart(fig, use_container_width=True)


# Displaying Customers per State as a bar chart
st.header('Customers per state')
result = calculator.must_customer_region()
customers_per_state = result['Customers per state']
fig = px.bar(
    customers_per_state,
    x=customers_per_state.index,
    y='Customers_per_states',
    title='Customers per State',
    labels={
        'Customers_per_states': 'Number of Customers'})
st.plotly_chart(fig, use_container_width=True)
