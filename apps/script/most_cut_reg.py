class MostCutReg:
    @staticmethod
    def clean(df):
        import pandas as pd
      
      
      # Read the customer dataframe
        customers = "data/olist_data/olist_customers_dataset.csv"
        customers_rd = pd.read_csv(customers)  #engine='python', encoding='utf-8',error_bad_lines=False
      
        # Read the order dataframe
        order_list = "data/olist_orders_dataset.csv"
        order_list_rd = pd.read_csv(order_list)
      
       # Left join in order to have the orders and the customers on the same dataframe
        customers_with_orders = pd.merge(customers_rd, order_list_rd, left_on='customer_id', right_on='customer_id')
     
        return customers_with_order
    @staticmethod
    def kpi(df):

         #Create a new dataframe for the customers per states
         cps=customers_with_orders.groupby('customer_state')['order_id'].count()
      
         #Adding labels for the count columns
         cps_count.columns = ["Customers_per_states"]
      
        #Sorting the count from the highest to the lowest
         final_csp=cps_count.sort_values(by='Customers_per_states', ascending=False)
       

            # Displaying the number of customers pre state
        print(final_csp)




        return {'Customers per state': final_csp}
