class CleanPayments:
    @staticmethod
    def clean(df):
        import pandas as pd  # Import pandas inside the class

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
        df_custumer = pd.read_csv('data/olist_customers_dataset.csv')
       
        # Merge the voucher amounts into the original dataframe
        df = pd.merge(df, df_custumer, on="customer_id", how="left")
        print(df.head())
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
            'payment_installments': 'first',
            'payment_value': 'sum',
            'have_voucher': 'first',
            'payment_value_voucher': 'first',
            'customer_unique_id': 'first',
            'customer_zip_code_prefix': 'first',
            'customer_city': 'first',
            'customer_state': 'first'
    
        }).reset_index()
        print(final_df.head())


        return final_df

    @staticmethod
    def kpi(df):
        total_orders = len(df)
        total_payment = df['payment_value'].sum()
        average_payment = df['payment_value'].mean()

        return {'Total Orders': total_orders, 'Total Payment': total_payment, 'Average Payment': average_payment}


import pandas as pd
df_payments = pd.read_csv('data/olist_order_payments_dataset.csv')
cleaned_df = CleanPayments.clean(df_payments)
