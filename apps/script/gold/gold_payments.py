import pandas as pd

class KpiCalculator:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def best_payment_method(self):
        paym_type = self.data.groupby('payment_type')['order_id'].count().sort_values(ascending=False)
        return {'Payment type usage': paym_type}
# Compare this snippet from apps/script/gold/gold_payments.py:
    def best_region(self):
        sales_per_state = self.data.groupby('customer_state')['payment_value'].sum().reset_index()
        sales_per_state=sales_per_state.sort_values(by='payment_value', ascending=False)
        sales_per_state['payment_value']=sales_per_state['payment_value'].map("R${:,.0f}K".format)
        return {'Sales per state': sales_per_state}
    def must_customer_region(self):
        cps=self.data.groupby('customer_state')['order_id'].count()
        cps_count = pd.DataFrame(cps)
        cps_count.columns = ["Customers_per_states"]
        #Sorting the count from the highest to the lowest
        final_csp=cps_count.sort_values(by='Customers_per_states', ascending=False)
        return {'Customers per state': final_csp}


    def orders_status(self):
        # Filter out canceled orders
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        orders_status = filtered_data['order_status'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
        return {'Orders status': orders_status}

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
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(filtered_data['order_purchase_timestamp'])
        return filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.to_period("M"))['payment_value'].sum()

    def revenues_per_year(self):
        # Filter out canceled orders and ensure 'order_purchase_timestamp' is in datetime format
        filtered_data = self.data[self.data['order_status'] != 'canceled']
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(filtered_data['order_purchase_timestamp'])
        return filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.to_period("Y"))['payment_value'].sum()