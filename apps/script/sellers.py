import pandas as pd
import os

state_dict = {
    'SP': 'São Paulo',
    'RN': 'Rio Grande do Norte',
    'AC': 'Acre',
    'RJ': 'Rio de Janeiro',
    'ES': 'Espírito Santo',
    'MG': 'Minas Gerais',
    'BA': 'Bahia',
    'SE': 'Sergipe',
    'PE': 'Pernambuco',
    'AL': 'Alagoas',
    'PB': 'Paraíba',
    'CE': 'Ceará',
    'PI': 'Piauí',
    'MA': 'Maranhão',
    'PA': 'Pará',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'RR': 'Roraima',
    'DF': 'Distrito Federal',
    'GO': 'Goiás',
    'RO': 'Rondônia',
    'TO': 'Tocantins',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'RS': 'Rio Grande do Sul',
    'PR': 'Paraná',
    'SC': 'Santa Catarina'
}
class SellersTable:
    def __init__(
            self,
            items_path='data/olist_order_items_dataset.csv',
            sellers_path='data/olist_sellers_dataset.csv',
            geo_path='data/olist_geolocation_dataset.csv',
            last_index_file='last_index.txt'):
        self.df_items = pd.read_csv(items_path)
        self.df_sellers = pd.read_csv(sellers_path)
        self.df_geo = pd.read_csv(geo_path)
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
        new_data = self.retrieve_new_data()  # Retrieve new data based on the last index
        if new_data.empty:
            print("No new data to process.")
            return
        cleaned_df = self.clean(new_data)  # Process the new data
        self.save_last_index(len(self.df_items))  # Update the last index
        print("Incremental update completed.")

    def retrieve_new_data(self):
        if self.last_index < len(self.df_items):
            new_data = self.df_items.iloc[self.last_index:]
        else:
            new_data = pd.DataFrame()
        return new_data

    def clean(self, df):
        cleaned_df = pd.merge(df, self.df_sellers, on="seller_id", how="left")
        cleaned_df= cleaned_df['seller_state'].map(state_dict)
        cleaned_df.to_csv('data/cleaned_sellers.csv', index=False)
        return cleaned_df


if __name__ == "__main__":
    sellers_table = SellersTable()
    print("Last Index:", sellers_table.get_last_index())
    sellers_table.incremental_update()
