import pandas as pd


class KpiCalculator:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def best_payment_method(self):
        paym_type = self.data.groupby('payment_type')[
            'order_id'].count().sort_values(ascending=False)
        return {'Payment type usage': paym_type}

    def payments_method_per_region(self):
        paym_type = self.data.groupby(['customer_state', 'payment_type'])[
            'order_id'].count().sort_values(ascending=False)
        return {'Payment type usage': paym_type}






    def average_order_value(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        return filtered_data['payment_value'].mean()

    def max_order_value(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        return filtered_data['payment_value'].max()

    def min_order_value(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        return filtered_data['payment_value'].min()

    def total_orders(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        return len(filtered_data)

    def orders_per_custom_period_month(self, period='month', start=None, end=None):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])

        # Set start and end dates if provided
        if start:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] >= pd.to_datetime(start)]
        if end:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] <= pd.to_datetime(end)]

        # Group by month and count the number of orders
        if period == 'month':
            orders = filtered_data.groupby(
                filtered_data['order_purchase_timestamp'].dt.to_period("M")).size()
        else:
            raise ValueError("Invalid period. Please use 'month'.")

        return orders


