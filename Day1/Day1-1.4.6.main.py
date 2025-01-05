from products import db

def get_products_of_category(category, page, per_page):
    startIndex = (page - 1) * per_page
    endIndex = startIndex + per_page
    return db.get(category, [])[startIndex:endIndex]

page = 1
while True:
    electronics = get_products_of_category('electronics', page, 5)
    if len(electronics) == 0:
        break
    print(f'Page {page}: {electronics}')
    page += 1