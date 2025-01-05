from products import db

def get_products_of_category(category, page, per_page):
    startIndex = (page - 1) * per_page
    endIndex = startIndex + per_page
    
    items = db.get(category, [])
    return items[startIndex:endIndex]

electronics = get_products_of_category('electronics', 1, 5)
living = get_products_of_category('living', 1, 5)
print(electronics, living)