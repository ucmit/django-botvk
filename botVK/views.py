from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
from django.shortcuts import render
import json, vk, random
import sqlite3
import database

# Создаём сессию по своему ключу
session = vk.Session(access_token="931d33285661908411a5c25841bdcccee83a1d92181122b9f2b087d688a80aa820659c9d8070c36e0d283")
vkAPI = vk.API(session)

# Центральная функция-обработчик версия API - 5.103
@csrf_exempt
def bot(request):
	body = json.loads(request.body)
	# Вывод в терминал тело JSON 
	print(body)

	# Подтверждение сервера
	if body == { "type": "confirmation", "group_id": 194135848 }: # Берём запрос и ответ в CallBack API
		return HttpResponse("b940e67c")

	# Определяем тип запроса. В данном случае "новое сообщение"
	if body["type"] == "message_new":
		
		msg = body["object"]["message"]["text"]
		payload = body["object"]["message"]["payload"]
		userID = body["object"]["message"]["from_id"]
		userInfo = vkAPI.users.get(user_ids = userID, v=5.103)[0]
		answ = ""
		attach = ""		

		if payload == """{"command":"start"}""":
			keyboardStart(request, userID)


		# #Учим бота новым словам
		# if msg[:6] == "/teach":
		# 	pos = msg.find("?")
		# 	newMsg = msg[7:pos].replace(" ", "")
		# 	newAnsw = msg[pos+1:]
		# 	database.insert("answer", ["msg", "answ"], [newMsg, newAnsw])
		# 	answ = "Я добавил новый запрос '{0}', давай попробуй =)".format(newMsg)

		# if answ == "":
		# 	for i in database.get("answer"):
		# 		if msg == i["msg"]:
		# 			answ = i["answ"]
		# 			break
		# 		else:
		# 			answ = "Я не знаю такой команды. Можешь научить меня используя команду /teach ЗАПРОС ? ОТВЕТ"

		sendAnswer(userID, answ, attach)

	return HttpResponse("ok")
# ---Конец функции---
	

def sendAnswer(userID, answ = "", attach = "", keyboard = ""):
	vkAPI.messages.send(user_id = userID, message = answ, attachment=attach, keyboard=keyboard, random_id = random.randint(1, 99999999999999999), v=5.103)

def keyboardStart(request, userID):
	answ = "Привет! Выбери свою группу пользователя!"
	keyboard = json.dumps({
		"one_time": True,

		"buttons":[[
			{
				"action": {
					"type":"text",
					"label":"Администратор",
					"payload": """{"command":"admin"}"""
				},
				"color":"negative"
			}
		]]
	})
	


	sendAnswer(userID, answ, keyboard = keyboard)




# lastMsg = vkAPI.messages.getHistory(user_id = userID, count = 2, v=5.103)["items"][1]["text"]
# if lastMsg == "Зимой и летом одним цветом. Что это?":
# 	if msg == "Ёлка":
# 		answ = "Поздравляю! Ты угадал!"
# 	else: 
# 		answ = "уууууууууу...."
# 	msg = ""

# if msg == "/start":
# 	answ = """Hello, there some commands you can use:
# 	1) /cheer [Чот забыл сделать😡]
# 	2) /dance
# 	3) /say [message]
# 	4) /myName
# 	5) /riddle"""
# elif msg == "/dance":
# 	attach = "doc223329963_541202194"
# elif msg[:4] == "/say":
# 	answ = msg[5:]
# elif msg == "/myName":
# 	answ = "Your name is {0} {1}".format(userInfo["first_name"], userInfo["last_name"])
# elif msg == "/riddle":
# 	answ = "Зимой и летом одним цветом. Что это?"

# def confirm(request):
# 	body = json.loads(request.body)
# 	if body == { "type": "confirmation", "group_id": 194135848 }: # Берём запрос и ответ в CallBack API
# 		return HttpResponse("2cd42a34")
# 	else:
# 		return HttpResponse("ok")