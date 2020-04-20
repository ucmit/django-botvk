from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
from django.shortcuts import render
import json, vk, random

# Создаём сессию по своему ключу
session = vk.Session(access_token="Секретный ключик")
vkAPI = vk.API(session)

# Центральная функция-обработчик версия API - 5.103
@csrf_exempt
def bot(request):
	body = json.loads(request.body)
	# Вывод в терминал тело JSON 
	print(body)


	# Подтверждение сервера
	if body == { "type": "confirmation", "group_id": 194135848 }: # Берём запрос и ответ в CallBack API
		return HttpResponse("b20b175a")


	# Определяем тип запроса. В данном случае "новое сообщение"
	if body["type"] == "message_new":
		# Определяем 
		userID = body["object"]["message"]["from_id"]
		if body["object"]["message"]["text"] == "/start":
			msg = "Привет! Меня зовут Ботик-ВК!"
			# Команда messages.send() подробнее в https://vk.com/dev/methods
			vkAPI.messages.send(user_id = userID, message = msg, random_id = random.randint(1, 99999999999999999), v=5.103)
	return HttpResponse("ok")
# ---Конец функции---
	