from dataclasses import dataclass
from typing import Optional
from products import db

@dataclass
class ProductFetchParams:
    category: str
    page: int = 1
    per_page: int = 5

def get_products_of_category(params: ProductFetchParams) -> Optional[list]:
    startIndex = (params.page - 1) * params.per_page
    endIndex = startIndex + params.per_page
    return db.get(params.category, [])[startIndex:endIndex]

params = ProductFetchParams('electronics')
electronics = get_products_of_category(params)
print(electronics)