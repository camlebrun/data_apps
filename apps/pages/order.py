import streamlit as st
import pandas as pd
import plotly.express as px
from script.gold.gold_payments import KpiCalculator


st.set_page_config(page_title='Orders', layout='wide')
st.write(
    f"""
    <div style="text-align:center">
        <h1>Orders</h1>
    </div>
    """,
    unsafe_allow_html=True
)

calculator = KpiCalculator('data/cleaned_payments.csv')# Displaying Orders Status as a bar chart
st.header('Orders status')
result = calculator.orders_status()
orders_status = result['Orders status']


# Create a pie chart to visualize the distribution of orders by status
fig_orders_status = px.pie(values=orders_status['proportion'], names=orders_status['order_status'], title='Orders Status')

# Display the pie chart
st.plotly_chart(fig_orders_status, use_container_width=True)


order_count_data = calculator.count_orders_over_time_days()

order_count_data['order_purchase_date'] = order_count_data['order_purchase_date'].astype(str)
# Create the line plot using Plotly Express
fig_order_count = px.line(order_count_data, x='order_purchase_date', y='count', title='Count of Orders Over Time',
                          labels={'order_purchase_date': 'Date', 'count': 'Number of Orders'})

# Display the plot in Streamlit
st.plotly_chart(fig_order_count, use_container_width=True)
