from products import db

def get_products_of_category(category, page, per_page):
    return db.get(category, [])

electronics = get_products_of_category('electronics')
living = get_products_of_category('living')
print(electronics, living)