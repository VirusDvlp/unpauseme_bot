import requests

# URL адрес, на который будет отправлен запрос
# url = 'http://127.0.0.1:8095/callback/dating_bot'
url = 'https://telegram.birthmatrix.ru:49165/callback/dating_bot'


# Создание объекта ImmutableMultiDict с данными
data = {
    #'_param_DAsimple_user_id': 5139856256,
    '_param_Unpauseme_user_id': 1005462960,
    'payment_status': 'success'
}

print(111111)
# Отправка POST-запроса
# response = requests.post(url, data=data, verify=False)
response = requests.post(url, data=data)
# response = requests.get(url, verify=False)

# Проверка статуса ответа
if response.status_code == 200:
    print('POST-запрос успешно отправлен')
else:
    print('Ошибка при отправке POST-запроса')



    
