import pandas as pd


class KpiSellers:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def total_sellers(self):
        return self.data['seller_id'].nunique()

    def sellers_per_state(self):
        return self.data['seller_state'].value_counts()

    def sellers_per_city(self):
        return self.data['seller_city'].value_counts()

    def sellers_per_category(self):
        return self.data['product_category_name'].value_counts()

    @staticmethod
    def kpi(df):
        total_sellers = len(df['seller_id'].unique())
        total_items = len(df)
        average_items_per_seller = df.groupby(
            'seller_id').size().mean().astype(int)
        count_seller = df['seller_id'].value_counts().head(10)
        sum_price = df.groupby('seller_state')['price'].sum()
        count_seller_state = df['seller_state'].value_counts().head(1000)
        count_seller_city = df['seller_city'].value_counts().head(1000)

        return {
            'Total Sellers': total_sellers,
            'Total Items': total_items,
            'Average Items per Seller': average_items_per_seller,
            'Count seller': count_seller,
            'Sum price': sum_price,
            'Count seller state': count_seller_state,
            'Count seller city': count_seller_city
        }
