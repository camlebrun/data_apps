import pandas as pd


class KpiCalculator:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)


    def revenues_per_year(self):
            # Filter out canceled orders and ensure 'order_purchase_timestamp' is
            # in datetime format
            filtered_data = self.data[self.data['order_status'] != 'canceled']
            filtered_data['order_purchase_timestamp'] = pd.to_datetime(
                filtered_data['order_purchase_timestamp'])
            return filtered_data.groupby(
                filtered_data['order_purchase_timestamp'].dt.to_period("Y"))['payment_value'].sum()

    def revenues_per_payment_type_per_year(self):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])
        return filtered_data.groupby([filtered_data['order_purchase_timestamp'].dt.to_period(
            "Y"), 'payment_type'])['payment_value'].sum()

    def revenues_per_state_per_year(self, selected_region):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])

        # Filter data for the selected region
        filtered_data = filtered_data[filtered_data['customer_state']
                                      == selected_region]

        # Group by year and sum payment values, reset index to convert the
        # result into a DataFrame
        result = filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.to_period("Y"))[
            'payment_value'].sum().reset_index()

        return result
    def total_revenue(self):
            # Filter out canceled orders
            filtered_data = self.data[self.data['order_status'] != 'canceled']
            return filtered_data['payment_value'].sum()

    def revenues_per_payment_type(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        return filtered_data.groupby('payment_type')['payment_value'].sum()

    def revenues_per_month(self):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])
        return filtered_data.groupby(
            filtered_data['order_purchase_timestamp'].dt.to_period("M"))['payment_value'].sum()

    def revenues_per_year(self):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])
        return filtered_data.groupby(
            filtered_data['order_purchase_timestamp'].dt.to_period("Y"))['payment_value'].sum()

    def revenues_per_custom_period(self, period='year', start=None, end=None):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])

        # Set start and end dates if provided
        if start:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] >= pd.to_datetime(
                start)]
        if end:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] <= pd.to_datetime(
                end)]

        # Group by year and sum payment values
        if period == 'year':
            revenues = filtered_data.groupby(
                filtered_data['order_purchase_timestamp'].dt.to_period("Y"))['payment_value'].sum()
        else:
            raise ValueError("Invalid period. Please use 'year'.")

        return revenues
    def revenues_per_custom_period_month(self, period='month', start=None, end=None):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])

        # Set start and end dates if provided
        if start:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] >= pd.to_datetime(
                start)]
        if end:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] <= pd.to_datetime(
                end)]

        # Group by month and sum payment values
        if period == 'month':
            revenues = filtered_data.groupby(
                filtered_data['order_purchase_timestamp'].dt.to_period("M"))['payment_value'].sum()
        else:
            raise ValueError("Invalid period. Please use 'month'.")

        return revenues
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

    def revenues_and_orders_per_custom_period(
            self, period='year', start=None, end=None):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])

        # Set start and end dates if provided
        if start:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] >= pd.to_datetime(
                start)]
        if end:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] <= pd.to_datetime(
                end)]

        # Group by year and sum payment values
        if period == 'year':
            revenues = filtered_data.groupby(
                filtered_data['order_purchase_timestamp'].dt.to_period("Y"))['payment_value'].sum()
            orders = filtered_data.groupby(
                filtered_data['order_purchase_timestamp'].dt.to_period("Y"))['order_id'].count()
        else:
            raise ValueError("Invalid period. Please use 'year'.")

        return revenues, orders


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

    def total_revenue(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        return filtered_data['payment_value'].sum()

    def revenues_per_payment_type(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        return filtered_data.groupby('payment_type')['payment_value'].sum()

    def revenues_per_month(self):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])
        return filtered_data.groupby(
            filtered_data['order_purchase_timestamp'].dt.to_period("M"))['payment_value'].sum()


    def revenues_per_custom_period(self, period='year', start=None, end=None):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])

        # Set start and end dates if provided
        if start:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] >= pd.to_datetime(
                start)]
        if end:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] <= pd.to_datetime(
                end)]

        # Group by year and sum payment values
        if period == 'year':
            revenues = filtered_data.groupby(
                filtered_data['order_purchase_timestamp'].dt.to_period("Y"))['payment_value'].sum()
        else:
            raise ValueError("Invalid period. Please use 'year'.")

        return revenues
    def revenues_per_custom_period_month(self, period='month', start=None, end=None):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is
        # in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(
            filtered_data['order_purchase_timestamp'])

        # Set start and end dates if provided
        if start:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] >= pd.to_datetime(
                start)]
        if end:
            filtered_data = filtered_data[filtered_data['order_purchase_timestamp'] <= pd.to_datetime(
                end)]

        # Group by month and sum payment values
        if period == 'month':
            revenues = filtered_data.groupby(
                filtered_data['order_purchase_timestamp'].dt.to_period("M"))['payment_value'].sum()
        else:
            raise ValueError("Invalid period. Please use 'month'.")

        return revenues
    def best_region(self):
        sales_per_state = self.data.groupby('customer_state')[
            'payment_value'].sum().reset_index()
        sales_per_state = sales_per_state.sort_values(
            by='payment_value', ascending=False)
        sales_per_state['payment_value'] = sales_per_state['payment_value']
        return {'Sales per state': sales_per_state}
    def must_customer_region(self):
        cps = self.data.groupby('customer_state')['order_id'].count()
        cps_count = pd.DataFrame(cps)
        cps_count.columns = ["Customers_per_states"]
        # Sorting the count from the highest to the lowest
        final_csp = cps_count.sort_values(
            by='Customers_per_states', ascending=False)
        return {'Customers per state': final_csp}