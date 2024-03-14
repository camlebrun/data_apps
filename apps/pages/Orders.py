import streamlit as st
import pandas as pd
import plotly.express as px
from script.gold.gold_payments import KpiCalculator

st.set_page_config(page_title='Orders', layout='wide')

# Title using Markdown
st.markdown("<h1 style='text-align: center;'>Orders</h1>", unsafe_allow_html=True)

calculator = KpiCalculator('data/cleaned_payments.csv')

# Custom page names in the sidebar
selected_page = st.sidebar.radio("Go to", ["Orders over Time", "Delayed Orders", "Average Delay by State", "Statistics on Delayed Orders", "Statistics on Delayed Orders Over Time"])

if selected_page == "Orders over Time":
    st.header('Orders over Time')

    result = calculator.orders_status()
    orders_status = result['Orders status']

    order_count_data = calculator.count_orders_over_time_days()
    order_count_data['order_purchase_date'] = order_count_data['order_purchase_date'].astype(str)

    # Create the line plot using Plotly Express
    fig_order_count = px.line(order_count_data, x='order_purchase_date', y='count', title='Count of Orders Over Time',
                              labels={'order_purchase_date': 'Date', 'count': 'Number of Orders'})

    # Display the plot in Streamlit
    st.plotly_chart(fig_order_count, use_container_width=True)

elif selected_page == "Delayed Orders":
    st.header('Delayed Orders')

elif selected_page == "Average Delay by State":
    st.header('Average Delay by State')
    dely_per_state = calculator.nb_delay_orders().groupby('customer_state').agg({'delay': 'mean'}).reset_index()
    fig = px.bar(dely_per_state, x='customer_state', y='delay', title='Average Delay by State',
                 labels={'customer_state': 'State', 'delay': 'Average Delay'})
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Statistics on Delayed Orders":
    st.header('Statistics on Delayed Orders')
    st.write('The table below shows the statistics on delayed orders.')
    st.dataframe(calculator.stat_on_delay_orders(), use_container_width=True)

elif selected_page == "Statistics on Delayed Orders Over Time":
    st.header('Statistics on Delayed Orders Over Time')
    st.write('The table below shows the statistics on delayed orders over time.')
    st.dataframe(calculator.stat_on_delay_orders_over_time(), use_container_width=True)
