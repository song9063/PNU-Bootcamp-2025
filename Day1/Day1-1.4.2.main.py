db = {
    '전자제품': [
        'MacBook', 'iPad', 'iPhone', 'iPod'
    ],
    '스포츠용품': [
        '축구공', '농구공', '야구공', '배구공'
    ]
}

strIn = '전자제품'
arRet = db.get(strIn, [])

strIn = '주방용품'
try:
    arRet = db[strIn]
except KeyError:
    arRet = []

print(arRet)