db = {
    '전자제품': [
        'MacBook', 'iPad', 'iPhone', 'iPod'
    ],
    '스포츠용품': [
        '축구공', '농구공', '야구공', '배구공'
    ]
}

def get_products_of_category(category):
    return db.get(category, [])

elctorics = get_products_of_category('전자제품')
products = get_products_of_category('주방용품')
print(elctorics, products)