import pandas as pd


class KpiCalculator:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def orders_status(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']

        # Calculate the percentage distribution of orders by status
        orders_status = filtered_data['order_status'].value_counts(
            normalize=True).mul(100).round(1)

        # Create a DataFrame with the order status and their respective
        # proportions
        orders_status_df = pd.DataFrame(
            {'order_status': orders_status.index, 'proportion': orders_status.values})

        return {'Orders status': orders_status_df}
    def count_orders_over_time_days(self):
        # select order status not canceled
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        # Convert 'order_purchase_timestamp' to datetime
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])
        # Group by date and count the number of orders, reset index to convert
        # the result into a DataFrame
        result = filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.to_period("D"))[
            'order_id'].count().reset_index()
        result.columns = ['order_purchase_date', 'count']
        return result
    def nb_delay_orders(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])
        filtered_data['order_approved_at'] = pd.to_datetime(
            filtered_data['order_approved_at'])
        filtered_data['order_delivered_carrier_date'] = pd.to_datetime(
            filtered_data['order_delivered_carrier_date'])
        filtered_data['order_delivered_customer_date'] = pd.to_datetime(
            filtered_data['order_delivered_customer_date'])
        filtered_data['order_estimated_delivery_date'] = pd.to_datetime(
            filtered_data['order_estimated_delivery_date'])
        filtered_data['delay'] = (
            filtered_data['order_delivered_customer_date'] -
            filtered_data['order_estimated_delivery_date']).dt.days
        return filtered_data[filtered_data['delay'] > 0]

    def stat_on_delay_orders(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])
        filtered_data['order_approved_at'] = pd.to_datetime(
            filtered_data['order_approved_at'])
        filtered_data['order_delivered_carrier_date'] = pd.to_datetime(
            filtered_data['order_delivered_carrier_date'])
        filtered_data['order_delivered_customer_date'] = pd.to_datetime(
            filtered_data['order_delivered_customer_date'])
        filtered_data['order_estimated_delivery_date'] = pd.to_datetime(
            filtered_data['order_estimated_delivery_date'])
        filtered_data['delay'] = (
            filtered_data['order_delivered_customer_date'] -
            filtered_data['order_estimated_delivery_date']).dt.days
        return filtered_data[filtered_data['delay'] > 0]['delay'].describe()

    def stat_on_delay_orders_over_time(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])
        filtered_data['order_approved_at'] = pd.to_datetime(
            filtered_data['order_approved_at'])
        filtered_data['order_delivered_carrier_date'] = pd.to_datetime(
            filtered_data['order_delivered_carrier_date'])
        filtered_data['order_delivered_customer_date'] = pd.to_datetime(
            filtered_data['order_delivered_customer_date'])
        filtered_data['order_estimated_delivery_date'] = pd.to_datetime(
            filtered_data['order_estimated_delivery_date'])
        filtered_data['delay'] = (
            filtered_data['order_delivered_customer_date'] -
            filtered_data['order_estimated_delivery_date']).dt.days
        return filtered_data[filtered_data['delay'] > 0].groupby(
            filtered_data['order_purchase_timestamp'].dt.to_period("M"))['delay'].median()
