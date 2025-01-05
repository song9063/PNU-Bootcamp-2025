import json
apiResponse = {
    "id": 1,
    "name": "iPhone",
    "on_sale": True,
    "price": 1000.0,
    "colors": ["black", "white"],
    "option": {
        "storage": 128,
        "charger": None
    }
}

strJsonData = json.dumps(apiResponse)
print(strJsonData)

strJsonData = json.dumps(apiResponse, indent=4)
print(strJsonData)