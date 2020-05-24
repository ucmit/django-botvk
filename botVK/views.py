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
		return HttpResponse("8a7bcb98")


	# Определяем тип запроса. В данном случае "новое сообщение"
	if body["type"] == "message_new":
		# Основные параметры сообщения
		msg = body["object"]["message"]["text"]
		userID = body["object"]["message"]["from_id"]
		userInfo = vkAPI.users.get(user_ids = userID, v=5.103)[0]
		
		# Проверка на наличие полезной нагрузки в сообщении
		if "payload" in body["object"]["message"]:
			payload = body["object"]["message"]["payload"]
			# Загрузка клавиатуры, если команда start
			if payload == """{"command":"start"}""":
				keyboardStart(request, userID)
			else:
				# Попытка провести добавления пользователя по выбранной группе
				try:
					gpid = -1
					gpname = ""
					# Взависимости от команды, выбираем группу
					if payload == """{"command":"admin"}""":
						gpid = str(1)
						gpname = "Администратор"
					elif payload == """{"command":"mentor"}""":
						gpid = str(2)
						gpname = "Наставник"
					elif payload == """{"command":"student"}""":
						gpid = str(3)
						gpname = "Ученик"
					# Добавляем пользователя в группу и сообщаем ему об этом
					database.insert("user", ["id, groupId"], [str(userID), gpid])
					speak(request,userID, userInfo, answ = "Вы были добавлены в группу {0}".format(gpname))
				# Обработка любой ошибки [Скорее всего, пользователь уже есть в группе]
				except Exception as e:
					speak(request,userID, userInfo, answ = "Error")
		# Если нагрузки нет, общаемся с пользователем как обычно 
		else:
			speak(request,userID, userInfo, msg)

	return HttpResponse("ok")
# ---Конец функции---
	
# ======================================== Доп. функции ====================================
# !Функция отправки сообщения!
def sendAnswer(userID, answ = "", attach = "", keyboard = json.dumps({"buttons":[],"one_time":True})):
	vkAPI.messages.send(user_id = userID, message = answ, attachment=attach, keyboard=keyboard, random_id = random.randint(1, 99999999999999999), v=5.103)

# !Функция обработки сообщения сообщения!
def speak(request,userID, userInfo = "", msg = "",  answ = "", attach=""):
	# Специальные команды бота
	# #Учим бота новым словам
	if msg[:6] == "/teach":
		pos = msg.find("?")
		newMsg = msg[7:pos].replace(" ", "")
		newAnsw = msg[pos+1:]
		database.insert("answer", ["msg", "answ"], [newMsg, newAnsw])
		answ = "Я добавил новый запрос '{0}', давай попробуй =)".format(newMsg)
	# #Вывести список всех команд
	elif msg == "/list":
		answ = database.get("answer", ["msg"])
	# #Узнать в какой я группе
	elif msg == "/whoAmI":
		answ = """Вы относитесь к группе {0}""".format(database.getGroup(str(userID))[0]["groupName"])
	# #Посмотреть список пользователей
	elif msg == "/whoAreThey":
		answ = """Пользователи:\n"""
		for i in database.getGroup():
			answ += """id: {0}, group: {1}\n""".format(i["id"], i["groupName"])
	elif msg == "/changeMe":
		# 1) Удалить пользователя из базы
		database.deleteUser(userID)
		# 2) Вызвать клавиатуру 
		keyboardStart(request, userID)
		return 1


	# Поиск ответа в базе
	if answ == "":
		for i in database.get("answer"):
			if msg == i["msg"]:
				answ = i["answ"]					
				break
			else:
				answ = "Я не знаю такой команды. Можешь научить меня используя команду /teach ЗАПРОС ? ОТВЕТ"

	sendAnswer(userID, answ, attach)


# !Функция начальной клавиатуры!
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
			},
			{
				"action": {
					"type":"text",
					"label":"Наставник",
					"payload": """{"command":"mentor"}"""
				},
				"color":"positive"
			},
			{
				"action": {
					"type":"text",
					"label":"Ученик",
					"payload": """{"command":"student"}"""
				},
				"color":"primary"
			}
		]]
	})
	sendAnswer(userID, answ, keyboard = keyboard)





# ========================================================================================================================

# Рендер нашей страницы login.html

lg = {
	"success": False,
	"groups": database.get("groups")
}
@csrf_exempt
def login(request):
	global lg

	if request.method == "GET":
		if request.GET.get("login") == "admin" and request.GET.get("password") == "0000":
			lg["success"] = True

	if request.method == "POST":
		if (request.POST.get("message") and request.POST.get("group")) != None:
			for user in database.getGroup(groupID = request.POST.get("group")):
				sendAnswer(user["id"], answ = request.POST.get("message"))


	return render(request, "login.html", lg)








# =========================================================================================================================
















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

