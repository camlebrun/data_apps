import pandas as pd
import os

class CleanPayments:
    def __init__(self, payments_path='data/olist_order_payments_dataset.csv', last_index_file='last_index_payments.txt'):
        self.df_payments = pd.read_csv(payments_path)
        self.last_index_file = last_index_file
        self.last_index = self.load_last_index()

    def load_last_index(self):
        if os.path.exists(self.last_index_file):
            with open(self.last_index_file, 'r') as file:
                return int(file.readline().strip())
        else:
            return 0

    def save_last_index(self, index):
        with open(self.last_index_file, 'w') as file:
            file.write(str(index))

    def get_last_index(self):
        return self.last_index

    def incremental_update(self):
        new_data = self.retrieve_new_data()
        if new_data.empty:
            print("No new data to process.")
            return
        cleaned_df = self.clean(new_data)
        self.save_last_index(self.last_index + len(new_data))  # Update the last index
        print("Incremental update completed.")

    def retrieve_new_data(self):
        if self.last_index < len(self.df_payments):
            new_data = self.df_payments.iloc[self.last_index:]
        else:
            new_data = pd.DataFrame()
        return new_data

    @staticmethod
    def clean(df):
        # Filter DataFrame for voucher payments
        voucher_payments = df[df['payment_type'] == 'voucher']

        # Replace credit_card, debit_card, and boleto with card
        df['payment_type'] = df['payment_type'].replace(['credit_card', 'debit_card', 'boleto'], 'card')

        # Assuming 'have_voucher' column is based on the payment type
        df['have_voucher'] = df['payment_type'] == 'voucher'

        # Calculate voucher amount per order
        voucher_amounts = voucher_payments.groupby('order_id')['payment_value'].sum().reset_index()
        voucher_amounts.rename(columns={'payment_value': 'payment_value_voucher'}, inplace=True)

        # Merge the voucher amounts into the original dataframe
        df = pd.merge(df, voucher_amounts, on="order_id", how="left")

        # Add order information
        df_orders = pd.read_csv('data/olist_orders_dataset.csv')
        df = pd.merge(df, df_orders, on="order_id", how="left")

        # Add customer information
        df_customers = pd.read_csv('data/olist_customers_dataset.csv')
        df = pd.merge(df, df_customers, on="customer_id", how="left")

        # Group by order_id and aggregate other columns
        final_df = df.groupby('order_id').agg({
            'customer_id': 'first',
            'order_status': 'last',
            'order_purchase_timestamp': 'first',
            'order_approved_at': 'first',
            'order_delivered_carrier_date': 'first',
            'order_delivered_customer_date': 'first',
            'order_estimated_delivery_date': 'first',
            'payment_type': 'first',
            'payment_value': 'sum',
            'have_voucher': 'first',
            'payment_value_voucher': 'first',
            'customer_unique_id': 'first',
            'customer_city': 'first',
            'customer_state': 'first'
        }).reset_index()
        final_df.to_csv('data/cleaned_payments.csv', index=False)
        return final_df



if __name__ == "__main__":
    clean_payments = CleanPayments()
    print("Last Index:", clean_payments.get_last_index())
    clean_payments.incremental_update()
