import json
strJsonData = '''
{
    "id": 1,
    "name": "iPhone",
    "on_sale": true,
    "colors": ["black", "white"],
    "option": {
        "storage": 128,
        "charger": null
    }
}
'''
jsonData = json.loads(strJsonData)
nId = jsonData.get('id')
strName = jsonData.get('name', '')
nStorage = jsonData.get('option',{}).get('storage', 0)
arColors = jsonData.get('colors', [])
if jsonData.get('on_sale', False):
    print(f'Product {nId} {strName}({nStorage}) is on sale')
    
if len(arColors) > 0:
    print('Available colors:')
    for color in arColors:
        print(f'\t- {color}')