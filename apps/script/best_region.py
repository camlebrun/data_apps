class RegionTable:
    @staticmethod
    def clean(df):
        import pandas as pd
      
      # Read the payment dataframe
        payment = pd.read_csv('data/olist_order_payments_dataset.csv')
      
      # Read the customer dataframe
        customers = "data/olist_data/olist_customers_dataset.csv"
        customers_rd = pd.read_csv(customers)  #engine='python', encoding='utf-8',error_bad_lines=False
      
        # Read the order dataframe
        order_list = "data/olist_orders_dataset.csv"
        order_list_rd = pd.read_csv(order_list)
      
       # First Left join in order to have the orders and the customers on the same dataframe
        customers_with_orders = pd.merge(customers_rd, order_list_rd, left_on='customer_id', right_on='customer_id')
      
      #  Second Left join add the payment info to the previous join
      customers_with_complete = pd.merge(customers_with_orders, payment_type_rd, left_on='order_id', right_on='order_id')


        return customers_with_complete
    @staticmethod
    def kpi(df):

        
        # Group by to have the list of scel
        sales_per_state = customers_with_complete.groupby('customer_state')['payment_value'].sum().reset_index()
        sales_per_state=sales_per_state.sort_values(by='payment_value', ascending=False)

        # Displaying the total sales per state
        print(sales_per_state)




        return {'Sales per states': sales_per_state}
