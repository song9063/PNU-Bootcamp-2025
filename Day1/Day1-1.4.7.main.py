from products import db

def get_products_of_category(category, page, per_page=1):
    startIndex = (page - 1) * per_page
    endIndex = startIndex + per_page
    return db.get(category, [])[startIndex:endIndex]

electronics = get_products_of_category('electronics', '1')
print(electronics)