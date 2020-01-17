import os
import json
import requests

from _config_datas import NB_CATEGORIES, NB_PAGES, MINPRODINCAT, NB_PRODUCT, PRODUCTS_PER_PAGE

class GetDatas:

    def __init__(self):
        self.final_cat = []
        self.categories_info = {}
        self.products_infos_list = []
        self.categories_id_list = []
        self.cat_prod_relation = []
        self.get_categories()
        self.get_products()
        self.get_categories_per_product()

    def get_categories(self):
        """
        This method loads categories from OpenFoodFacts API
        and create a json file with datas
        """

        list_filtered_cat = []
        url = 'https://fr.openfoodfacts.org/categories.json'
        data = requests.get(url).json()

        # Get categories datas in a list so they can be treated as needed
        for item in data["tags"]:
            list_filtered_cat.append(item)
        i = 0
        for cat in list_filtered_cat:
            # limit the number of categories to the number chosen in config
            if i < NB_CATEGORIES:
                # limit the categories to the ones which have a lot of products
                if cat["products"] > MINPRODINCAT:
                    self.final_cat.append(cat)
                    i += 1

        self.truncate_datas("categories")
        self.get_info_from_categories()

    def get_info_from_categories(self):
        """
        This method get datas needed to load products pages with Json class
        """
        cat_url_names = []
        cat_names = []

        for category in self.final_cat:
            # get only names of categories in the url to use it for API search requests
            url = category["url"]
            url = url[39:]
            cat_url_names.append(url)
            # get names of categories to name related files
            cat_names.append(category["name"])
            # create a dictionnary for each category with those elements
            self.categories_info = {x:y for x, y in zip(cat_names, cat_url_names)}

    def get_products(self):
        """
        This method loads products from OpenFoodFacts API
        This method is called after sorting datas with Sorted_datas class
        which defines which categories to get and allow to get informations
        such as names (for file's names) and url names (to call urls)
        """

        for name, urlnames in self.categories_info.items():
            for i in range(1, (NB_PAGES+1)):
                url = 'https://world.openfoodfacts.org/cgi/search.pl?\
                    search_tag=categories&search_terms={}&\
                    purchase_places=France&page_size={}&page={}&json=1'.format(
                        urlnames, str(PRODUCTS_PER_PAGE), str(i))
                data = requests.get(url).json()

        # Filter Products getting product's datas into lists
        for name in self.categories_info.keys():
            for i in range(1, (NB_PAGES + 1)):
                for prod in data["products"]:
                    try:
                        self.products_infos_list.append({
                            "id" : prod["id"],
                            "product_name" : prod["product_name"],
                            "nutrition_grade_fr" : prod["nutrition_grade_fr"],
                            "url" : prod["url"]
                            })
                        self.categories_id_list.append(prod["categories_hierarchy"])
                    except KeyError:
                        pass

        self.truncate_datas("products")

    def truncate_datas(self, data_type):
        """ truncate datas to sizes defined for each element in the database"""

        if data_type == "categories":
            for cat in self.final_cat:
                cat["id"] = cat["id"][:80]
                cat["name"] = cat["name"][:80]
                cat["url"] = cat["url"][:255]
                if "sameAs" in cat.keys():
                    del cat["sameAs"]

        elif data_type == "products":
            for prod in self.products_infos_list:
                prod["id"] = prod["id"][:80]
                prod["product_name"] = prod["product_name"][:80]
                prod["url"] = prod['url'][:255]

    def get_categories_per_product(self):
        """
        This method get datas to insert in the table Asso_Prod_Cat
        wich links products and categories
        NB : a product can belong to more than one category
        """

        i = 0
        while i < len(self.products_infos_list)-1:
            product_id = self.products_infos_list[i]['id']   #get product's id

            for category_id in self.categories_id_list[i]:  # get category's id

                info_cat = (category_id, product_id)

                if info_cat not in self.cat_prod_relation:  # check if not duplication
                    self.cat_prod_relation.append(info_cat)
                else:
                    pass
            i += 1

if __name__ == "__main__":
    datas = GetDatas()
    print(datas.cat_prod_relation)
    # print(datas.categories_id_list)
