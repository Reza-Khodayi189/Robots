from pyrubi import Client
import asyncio
from time import sleep
from colorama import Fore

bot = Client("Self")

def get_guid(id:str):
	a = bot.get_chat_info_by_username(id)
	type = a["type"]
	if type == "Channel":
		guid = a["channel"]["channel_guid"]
	elif type == "User":
		guid = a["user"]["user_guid"]
		last_id = a["chat"]["last_message_id"]
	return {"guid": guid, "last_id": last_id}

def get_messages():
	try:
		user = get_guid("") # آیدی فرد رو بذارید
		idd = ""
		get = bot.get_messages_interval(user["guid"], idd)["messages"]
		my_guid = get_guid("")["guid"] # آیدی خودتون
		num = 0
		for msg in get:
			msg_id = msg["message_id"]
			text = msg["text"]
			if idd == "":
				idd = msg_id
			guid = msg["author_object_guid"]
			if guid == my_guid:
				bot.delete_messages(guid, message_ids=[idd])
				num += 1
				print(text)
	except Exception as e:
		print(e)

while True:
	get_messages()
