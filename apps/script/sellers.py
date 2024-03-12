import pandas as pd

class SellersTable:
    def __init__(self, items_path='data/olist_order_items_dataset.csv', sellers_path='data/olist_sellers_dataset.csv'):
        self.df_items = pd.read_csv(items_path)
        self.df_sellers = pd.read_csv(sellers_path)

    @staticmethod
    def clean(df_items, df_sellers):
        cleaned_df = pd.merge(df_items, df_sellers, on="seller_id", how="left")
        return cleaned_df

    @staticmethod
    def kpi(df):
        total_sellers = len(df['seller_id'].unique())
        total_items = len(df)
        average_items_per_seller = df.groupby('seller_id').size().mean().astype(int)
        
        # Count the number of items per seller
        count_seller = df['seller_id'].value_counts().sort_values(ascending=False).head(10)
        
        # Sum of price by seller_state
        sum_price = df.groupby('seller_state')['price'].sum()
        
        # Count the number of items per region
        count_seller_state = df['seller_state'].value_counts().sort_values(ascending=False).head(10)

        return {
            'Total Sellers': total_sellers,
            'Total Items': total_items,
            'Average Items per Seller': average_items_per_seller,
            'Count seller': count_seller,
            'Sum price': sum_price,
            'Count seller state': count_seller_state
        }


