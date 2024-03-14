import streamlit as st
from script.gold.gold_payments import KpiCalculator
import pandas as pd

# Function to calculate metrics and display them


def calculate_and_display_metrics(start_date, end_date):
    calculator = KpiCalculator('data/cleaned_payments.csv')
    # Calculate revenues and orders for the selected custom period
    revenues, orders = calculator.revenues_and_orders_per_custom_period(
        period='year', start=start_date, end=end_date)

    # Calculate total revenue and orders for each year within the selected
    # range
    total_revenues = {index.year: value for index, value in revenues.items()}
    total_orders = {index.year: value for index, value in orders.items()}

    # Extract revenues and orders for the start_date and end_date
    revenue_start_date = total_revenues.get(start_date.year, 0)
    revenue_end_date = total_revenues.get(end_date.year, 0)
    order_start_date = total_orders.get(start_date.year, 0)
    order_end_date = total_orders.get(end_date.year, 0)

    # Calculate the difference and percentage difference for revenues
    revenue_diff = revenue_end_date - revenue_start_date
    percentage_revenue_diff = (
        revenue_diff / revenue_start_date) * 100 if revenue_start_date != 0 else 0

    # Calculate the difference and percentage difference for orders
    order_diff = order_end_date - order_start_date
    percentage_order_diff = (order_diff / order_start_date) * \
        100 if order_start_date != 0 else 0

    # Display metrics with difference and percentage difference
    col1, col2 = st.columns(2)
    with col1:
        st.write('### Revenue')
        st.metric(label=f" {end_date} VS {start_date}",
                  value=revenue_diff,
                  delta=f"{percentage_revenue_diff:.2f}%")
    with col2:
        st.write('### Orders')
        st.metric(label=f" {end_date} VS {start_date}",
                  value=order_diff,
                  delta=f"{percentage_order_diff:.2f}%")

# Main function


def main():
    # Create an instance of the KpiCalculator class
    calculator = KpiCalculator('data/cleaned_payments.csv')

    # Convert minimum and maximum dates to datetime
    min_date = pd.to_datetime(
        calculator.data['order_purchase_timestamp'].min())
    max_date = pd.to_datetime(
        calculator.data['order_purchase_timestamp'].max())

    # Streamlit page configuration
    st.set_page_config(page_title='Year-over-Year Analysis', layout='wide')

    # Page title
    st.title('Year-over-Year Analysis')
    st.write('Welcome to the Year-over-Year Analysis Dashboard! This dashboard provides insights into the year-over-year performance of the business.')
    st.info('Select a custom period to compare the performance of the business over the years.')
    # Sidebar inputs for custom period selection
    st.sidebar.header('Custom Period Selection')

    # Get default date values
    default_start_date, default_end_date = min_date, max_date
    start_date = st.sidebar.date_input("Start date:", value=default_start_date)
    end_date = st.sidebar.date_input("End date:", value=default_end_date)

    # Validate date range
    if start_date > end_date:
        st.error("Error: End date cannot be earlier than start date.")
        return

    # Calculate and display metrics
    calculate_and_display_metrics(start_date, end_date)


if __name__ == "__main__":
    main()
