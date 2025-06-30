import time

import requests


def get_payment_link(uid):
    url = "https://andwhatifyes.payform.ru/"
    data = {
        "order_id": int(time.time()),
        "_param_Unpauseme_user_id": uid,
        "products[0][price]": 1580,
        "products[0][quantity]": 1,
        "products[0][name]": "Чек-лист «Как не стать временной: ОБЕРЕГ на старте отношений»",
        "do": "link",
        "discount_value": 790
    }

    if uid in [1005462960, 381576126]:
        data["demo_mode"] = 1
    
    req = requests.post(url, data=data)
    return req.text
