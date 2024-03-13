class OrderS:
    @staticmethod
    def clean(df):
        import pandas as pd
      
      
      # Read the orders dataframe
        orders = "data/olist_data/olist_orders_dataset.csv"  #engine='python', encoding='utf-8',error_bad_lines=False
         
        order_list_rd = pd.read_csv(order_list)
       
        return customers_with_order
    @staticmethod
    def kpi(df):

          # Displaying the distribution of every order status as a percentange
          os=order_list_rd['order_status'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
          os

            # Displaying the distribution
        print(os)


        return {'Order Status': final_csp}
