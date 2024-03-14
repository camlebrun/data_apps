class ProdCatSales:
    @staticmethod
    def clean(df):
        import pandas as pd
      
      
      # Read the item category data frame(dataframe contaning the orders linked with products)
        item_cat="data/olist_data/olist_order_items_dataset.csv"
        item_cat_rd = pd.read_csv(item_cat)

      # Read the customers dataframe
        customers = "data/olist_data/olist_customers_dataset.csv"
        customers_rd = pd.read_csv(customers)  #engine='python', encoding='utf-8',error_bad_lines=False

      # Read the product dataframe(dataframe containing the product description with the category name)
        products = "data/olist_data/olist_products_dataset.csv"
        products_rd = pd.read_csv(products)   

        # Read the order dataframe
        order_list = "data/olist_orders_dataset.csv"
        order_list_rd = pd.read_csv(order_list)

        #Create dataframe for products and category only
        az = pd.DataFrame(products_rd[['product_id', 'product_category_name']])
        az

        #Create the inventory dataframe
        inventory = pd.DataFrame(item_cat_rd[['order_id','product_id','price','freight_value']])
        inventory

        

       # Left join in order to have the complete inventory(orders+product_type+)
        invent_complet = pd.merge(az,item_cat_rd, left_on='product_id', right_on='product_id')

      #  Getting rid of useless columns
        cln_inv=invent_complet.drop(['shipping_limit_date','seller_id'],axis=1)
      # Creating the product category viz
        prod_cat_sales_viz = pd.merge(cln_inv,customers_with_complete, left_on='order_id', right_on='order_id')
      #Getting rid of the NaN
        prod_cat_sales_viz_clean=prod_cat_sales_viz.dropna()

    #Creating custom cat
        
        custom_categories = {
    'Beauty': ['perfumaria', 'beleza_saude', 'cool_stuff', 'fashion_bolsas_e_acessorios', 'relogios_presentes'],
    'Home,Tools and Decoration': ['construcao_ferramentas_iluminacao','construcao_ferramentas_jardim','construcao_ferramentas_seguranca','sinalizacao_e_seguranca','artigos_de_festas','construcao_ferramentas_ferramentas','construcao_ferramentas_construcao','casa_conforto','moveis_cozinha_area_de_servico_jantar_e_jardim','moveis_sala','la_cuisine','utilidades_domesticas','artigos_de_natal','moveis_colchao_e_estofado','artes_e_artesanato','moveis_escritorio','ferramentas_jardim','artes','moveis_decoracao','flores','cama_mesa_banho', 'utilidades_domesticas', 'casa_construcao', 'casa_conforto','casa_conforto_2','portateis_cozinha_e_preparadores_de_alimentos'],
    'Electronics,Appliance and Toys': ['climatizacao','tablets_impressao_imagem','portateis_casa_forno_e_cafe','eletroportateis','consoles_games','eletrodomesticos','eletrodomesticos_2','pcs','telefonia','dvds_blu_ray','tablets_impressao_imagem','brinquedos','eletronicos', 'informatica_acessorios', 'eletroportateis', 'consoles_games', 'eletrodomesticos','pc_gamer'],
    'Sports': ['esporte_lazer', 'fashion_esporte'],
    'Books and Media': ['livros_importados','cds_dvds_musicais','instrumentos_musicais','audio','musica','livros_interesse_geral', 'livros_tecnicos', 'livros_importados', 'cds_dvds_musicais','moveis_quarto','cine_foto'],
    'Health':['beleza_saude','bebes','seguros_e_servicos','fraldas_higiene'],
    'Food':['alimentos','alimentos_bebidas','bebidas'],
    'Fashion':['malas_acessorios','fashion_roupa_masculina','fashion_roupa_feminina','fashion_roupa_infanto_juvenil','fashion_bolsas_e_acessorios','fashion_underwear_e_moda_praia','fashion_calcados'],
    'Office':['moveis_escritorio','telefonia_fixa','papelaria'],
    'Animals':['pet_shop'],
    'Industry':['automotivo','agro_industria_e_comercio','climatizacao','industria_comercio_e_negocios','market_place']
        }

      # Create a function to map custom categories to original categories
        def map_custom_category(category):
            for custom_category, categories in custom_categories.items():
                if category in categories:
                    return custom_category
            
                return 'Other'  # Default category if no match found
        #Merging with the customers_with_complete to have an outlook of the sales next to the category

        prod_cat_ord = pd.merge(customers_with_complete, prod_cat_sales_viz_clean, left_on='order_id', right_on='order_id')
         # Apply the function to create a new column with custom categories
        prod_cat_ord['custom_category'] = prod_cat_ord['product_category_name'].apply(map_custom_category)
      
      
        return prod_cat_ord
    @staticmethod
    def kpi(df):

      
     
      # Group by custom category and count the number of occurrences
      #grouped_counts = prod_cat_ord.groupby('custom_category').size().reset_index(name='count')

        ae=prod_cat_ord.groupby('custom_category')['payment_value_y'].sum().reset_index()
        ae.sort_values(by='payment_value_y',ascending=False)
