import streamlit as st
import pandas as pd
import plotly.express as px
from script.gold.gold_orders import KpiCalculator

st.set_page_config(page_title='Orders', layout='wide')

# Title using Markdown
st.markdown(
    "<h1 style='text-align: center;'>Orders</h1>",
    unsafe_allow_html=True)

# Creation d'un plot pour la geolocalisation



calculator = KpiCalculator('data/cleaned_payments.csv')

# Custom page names in the sidebar
selected_page = st.sidebar.radio("Go to",
                                 ["Orders over Time",
                                  "Sales per Category",
                                  "Map of Orders per Region",
                                  "Delayed Orders",
                                  "Average Delay by State",
                                  "Statistics on Delayed Orders",
                                  "Evolutions of Delayed Orders Over Time"])

if selected_page == "Orders over Time":
    st.header('Orders over Time')

    result = calculator.orders_status()
    orders_status = result['Orders status']

    order_count_data = calculator.count_orders_over_time_days()
    order_count_data['order_purchase_date'] = order_count_data['order_purchase_date'].astype(
        str)

    # Create the line plot using Plotly Express
    fig_order_count = px.line(
        order_count_data,
        x='order_purchase_date',
        y='count',
        title='Count of Orders Over Time',
        labels={
            'order_purchase_date': 'Date',
            'count': 'Number of Orders'})

    # Display the plot in Streamlit
    st.plotly_chart(fig_order_count, use_container_width=True)
elif selected_page == "Sales per Category":
    st.header('Sales per Categories')
    sales_per_categories = pd.read_csv('data/cat_sales.csv')
    
    # Grouping data by category and summing up sales value
    sales_per_category = sales_per_categories.groupby('custom_category')['payment_value_y'].sum().reset_index()

    fig = px.pie(sales_per_category,
                 values='payment_value_y',
                 names='custom_category',
                 title='Sales Distribution per Category',
                 )
    fig.update_traces(textinfo='percent+label')  # Displaying percentage and label on the chart
    fig.update_layout(title_x=0.5)  # Centering the title
    
    st.plotly_chart(fig, use_container_width=True)



elif selected_page == "Delayed Orders":
    st.header('Delayed Orders')
    st.dataframe(calculator.nb_delay_orders(), use_container_width=True)
elif selected_page == "Map of Orders per Region":
    geolocation = pd.read_csv('data/olist_geolocation_dataset.csv')
    data = geolocation
    st.header('Map of Orders per Region')
    st.write('The map above shows the distribution of orders per region.')
    st.map(data, latitude='geolocation_lat', longitude='geolocation_lng', use_container_width=True)
    

elif selected_page == "Average Delay by State":
    st.header('Average Delay by State')
    dely_per_state = calculator.nb_delay_orders().groupby(
        'customer_state').agg({'delay': 'mean'}).reset_index()
    fig = px.bar(
        dely_per_state,
        x='customer_state',
        y='delay',
        title='Average Delay by State',
        labels={
            'customer_state': 'State',
            'delay': 'Average Delay'})
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Statistics on Delayed Orders":
    st.header('Statistics on Delayed Orders')
    st.write('The table below shows the statistics on delayed orders.')
    st.dataframe(calculator.stat_on_delay_orders(), use_container_width=True)

elif selected_page == "Evolutions of Delayed Orders Over Time":
    st.header('Evolutions of Delayed Orders Over Time')
    st.write(
        'The line plot below shows the median delay over time for delayed orders.')

    # Calculate median delay over time
    median_delay_over_time = calculator.stat_on_delay_orders_over_time()

    # Check if there is data to display
    if not median_delay_over_time.empty:
        # Plot the median delay over time
        fig_median_delay = px.line(
            x=median_delay_over_time.index.to_timestamp(),
            y=median_delay_over_time.values,
            title='Median Delay Over Time',
            labels={
                'x': 'Date',
                'y': 'Median Delay'})
        st.plotly_chart(fig_median_delay, use_container_width=True)
    else:
        st.write(
            "No data available for displaying the evolutions of delayed orders over time.")
