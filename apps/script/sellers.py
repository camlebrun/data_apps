class SellersTable:
    @staticmethod
    def clean(df):
        import pandas as pd
        df_items = pd.read_csv('data/olist_order_items_dataset.csv')
        # Add seller information
        df_sellers = pd.read_csv('data/olist_sellers_dataset.csv')
        cleaned_df = pd.merge(df_items, df_sellers, on="seller_id", how="left")

        return cleaned_df
    @staticmethod
    def kpi(df):
        total_sellers = len(df['seller_id'].unique())
        total_items = len(df)
        average_items_per_seller = total_items / total_sellers
        average_items_per_seller = df.groupby('seller_id').size().mean().astype(int)
        # count the number of items per seller
        count_seller = df['seller_id'].value_counts().sort_values(ascending=False).head(10)

        # sum of price  by seller_state
        sum_price = df.groupby('seller_state')['price'].sum()
        # count the number of items per region
        count_seller_state = df['seller_state'].value_counts().sort_values(ascending=False).head(10)




        return {'Total Sellers': total_sellers, 'Total Items': total_items, 'Average Items per Seller': average_items_per_seller, 'Count seller': count_seller, 'Sum price': sum_price, 'Count seller state': count_seller_state}