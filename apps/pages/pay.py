import pandas as pd
import streamlit as st
import plotly.express as px

# Set page title and layout
st.set_page_config(page_title='Payments Analysis', layout='wide')

# Read the data
try:
    df = pd.read_csv('data/cleaned_payments.csv')
except FileNotFoundError:
    st.error("File not found. Please make sure the file path is correct.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()

# Convert 'order_purchase_timestamp' to datetime
df['order_purchase_date'] = pd.to_datetime(df['order_purchase_timestamp']).dt.date

# Title
st.title('Payments Analysis')

# Calculate KPIs
total_revenue = df['payment_value'].sum()
average_order_value = df['payment_value'].mean()
total_orders = len(df)

# Display KPIs
st.header("Key Performance Indicators")
st.write(f"Total Revenue: ${total_revenue:.2f}")
st.write(f"Average Order Value: ${average_order_value:.2f}")
st.write(f"Total Orders: {total_orders}")

# Time series for payment value over time
fig_payment_value = px.histogram(df, x='order_purchase_date', y='payment_value', title='Payment Value Over Time',
                                 labels={'order_purchase_date': 'Date', 'payment_value': 'Payment Value'})
st.plotly_chart(fig_payment_value, use_container_width=True)

# Time series for voucher payment value over time
fig_voucher_payment = px.histogram(df, x='order_purchase_date', y='payment_value_voucher',
                                   title='Voucher Payment Value Over Time',
                                   labels={'order_purchase_date': 'Date', 'payment_value_voucher': 'Voucher Payment Value'})
st.plotly_chart(fig_voucher_payment, use_container_width=True)

# Count of orders over time
count_orders_over_time = df.groupby('order_purchase_date').size().reset_index(name='count')
fig_order_count = px.line(count_orders_over_time, x='order_purchase_date', y='count', title='Count of Orders Over Time',
                          labels={'order_purchase_date': 'Date', 'count': 'Number of Orders'})
st.plotly_chart(fig_order_count, use_container_width=True)

# Add explanations or context
st.write("""
    This dashboard provides insights into the payments data, including trends in payment value, voucher payment value,
    and the count of orders over time. Explore the plots to gain a better understanding of the data.
""")
