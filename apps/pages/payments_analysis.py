import streamlit as st
import pandas as pd
import plotly.express as px
from script.gold.gold_payments import KpiCalculator

st.set_page_config(page_title='Payments Analysis', layout='wide')
st.title('Payments Analysis')

calculator = KpiCalculator('data/cleaned_payments.csv')

# Displaying the analysis of most used payment methods using st.metrics
st.write('## Analysis of most used payment methods')
result = calculator.best_payment_method()
col1, col2, col3 = st.columns(3)
for key, value in result.items():
    if key == 'Payment type usage':
        for payment_type, count in value.items():
            if payment_type in ['credit_card', 'boleto']:
                col1.metric(payment_type, count)
            elif payment_type == 'debit_card':
                col2.metric(payment_type, count)
            else:
                col3.metric(payment_type, count)
    else:
        col1.metric(key, value)

# Displaying Sales per State as a bar chart
st.header('Sales per state')
result = calculator.best_region()
sales_per_state = result['Sales per state']
fig = px.bar(sales_per_state, x='customer_state', y='payment_value', title='Sales per State', labels={'payment_value': 'Payment Value'})
st.plotly_chart(fig, use_container_width=True)

# Displaying Customers per State as a bar chart
st.header('Customers per state')
result = calculator.must_customer_region()
customers_per_state = result['Customers per state']
fig = px.bar(customers_per_state, x=customers_per_state.index, y='Customers_per_states', title='Customers per State', labels={'Customers_per_states': 'Number of Customers'})
st.plotly_chart(fig, use_container_width=True)

# Displaying Orders Status as a bar chart
st.header('Orders status')
result = calculator.orders_status()
orders_status = result['Orders status']
fig = px.pie(values=orders_status, names=orders_status.index, title='Orders Status')
st.plotly_chart(fig, use_container_width=True)

#st.header('Orders status')
#result = calculator.orders_status()
#orders_status = result['Orders status']
#fig = px.bar(x=orders_status.index, y=orders_status, title='Orders Status', labels={'y': 'Percentage'})
#st.plotly_chart(fig, use_container_width=True)

# Displaying Average Order Value, Max Order Value, Min Order Value, Total Orders, and Total Revenue
st.header('Order Statistics')
average_order_value = calculator.average_order_value()
max_order_value = calculator.max_order_value()
min_order_value = calculator.min_order_value()
total_orders = calculator.total_orders()
total_revenue = calculator.total_revenue()

st.write(f"Average Order Value: ${average_order_value:.2f}")
st.write(f"Max Order Value: ${max_order_value:.2f}")
st.write(f"Min Order Value: ${min_order_value:.2f}")
st.write(f"Total Orders: {total_orders}")
st.write(f"Total Revenue: ${total_revenue:.2f}")

# Displaying Revenues per Payment Type as a bar chart
st.header('Revenues Analysis')
revenues_per_payment_type = calculator.revenues_per_payment_type()
fig = px.bar(revenues_per_payment_type, x=revenues_per_payment_type.index, y='payment_value', title='Revenues per Payment Type', labels={'payment_value': 'Payment Value'})
st.plotly_chart(fig, use_container_width=True)

# Displaying Revenues per Month as a bar chart
st.subheader('Revenues per Month')
revenues_per_month = calculator.revenues_per_month()
revenues_per_month.index = revenues_per_month.index.astype(str)  # Convert Period index to string
fig = px.bar(revenues_per_month, x=revenues_per_month.index, y='payment_value', title='Revenues per Month', labels={'payment_value': 'Payment Value'})
st.plotly_chart(fig, use_container_width=True)

# Displaying Revenues per Year as a bar chart
st.subheader('Revenues per Year')
revenues_per_year = calculator.revenues_per_year()
revenues_per_year.index = revenues_per_year.index.astype(str)  # Convert Period index to string
fig = px.bar(revenues_per_year, x=revenues_per_year.index, y='payment_value', title='Revenues per Year', labels={'payment_value': 'Payment Value'})
st.plotly_chart(fig, use_container_width=True)
