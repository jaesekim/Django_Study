from django.shortcuts import render

def price(request, name, nums):
    product_price = {
        "라면": 980,
        "홈런볼": 1500,
        "칙촉": 2300, 
        "식빵": 1800
        }
    if name in product_price:
        context = {
            'status' : True,
            'name' : name,
            'price' : product_price[name] * nums,
            'nums': nums
        }
        
    else:
        context = {
            'status' : False,
            'name' : name,
            'product_price' : product_price
        }

    return render(request, 'prices_app/price.html', context)