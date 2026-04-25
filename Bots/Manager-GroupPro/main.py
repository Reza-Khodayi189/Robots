from rubpy import Client, filters, utils
from rubpy.types import Updates
from random import randint, choice, random
import pyrubi
from bs4 import BeautifulSoup
import os, json, asyncio, requests, re, urllib, time, jdatetime
from sargarmi import Sargarmi

bot = Client("myself")
app = pyrubi.Client("myself")

s = Sargarmi()
status = json.loads(open("Files/status.json", "r", encoding="utf-8").read())
Admins = list(status["Admins"])
Black_List, AdminGold, sokhango_status = [], [], True

my_guid = app.get_me()["user"]["user_guid"]

check = os.path.exists("Files/yad.json")
if check == False:
	open("Files/yad.json","w").write("{}")
check = os.path.exists("Files/asl.json")
if check == False:
	open("Files/asl.json","w").write("{}")
check = os.path.exists("Files/lagb.json")
if check == False:
	open("Files/lagb.json","w").write("{}")

def is_reply(client: Updates):
	try:
		reply_id = client.reply_app_id
		get = bot.get_apps_by_id(client.object_guid, reply_id)
		guid = get.apps[0].author_object_guid
		if guid == my_guid:
			return True
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش ریپلای پیام :\n\n{e}")

def Link(text:str):
	if status["locks"]["Link"]:
		links = status["Links"]
		for check in links:
			if check in text:
				return True

def Fosh(text:str):
	if status["locks"]["Fosh"]:
		links = status["fosh"]
		for check in links:
			if check in text:
				return True


def warn_user(client: Updates, guid:str, type):
	try:
		try:
			with open("Files/warn_list.json", "r", encoding="utf-8") as f:
				warning_user = json.load(f)
		except FileNotFoundError:
			warning_user = {type: []}
		warning_user[type].append(guid)
		with open("Files/warn_list.json", "w", encoding="utf-8") as f:
			json.dump(warning_user, f, ensure_ascii=False, indent=4)
		warning_user = json.loads(open("Files/warn_list.json", "r", encoding="utf-8").read())
		warns = warning_user[type]
		if guid in warns:
			num = int(warns.count(guid))
			warn_del = status["num_bans"][type]
			if num < warn_del:
				client.delete()
				aa = utils.Mention("کاربر", guid)
				client.reply(f'''🔔 {aa} گرامی اخطار دریافت کرد

دلیل: ارسال {type}

وضعیت اخطار: {num} از {warn_del}

لطفاً از تکرار مورد خودداری فرمایید.''')
			if num == warn_del:
				client.delete()
				aa = utils.Mention("کاربر", guid)
				client.reply(f"🚫 {aa} گرامی شما به دلیل رعایت نکردن قوانین ریم شدید. ❗️")
				if status["ban_member"]:
					bot.ban_member(client.object_guid, guid)
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش اخطار به کاربر :\n\n{e}")


@bot.on_app_updates(filters.is_group, filters.is_text)
def Invite_group(client: Updates):
	try:
		text = client.text
		target = client.object_guid
		app_id = client.app_id
		if text == "یک عضو از طریق لینک به گروه افزوده شد.":
			current_jdatetime = jdatetime.datetime.now()
			year = current_jdatetime.year
			month = current_jdatetime.month
			day = current_jdatetime.day
			hour = current_jdatetime.hour
			minute = current_jdatetime.minute
			second = current_jdatetime.second
			date = f"{year}/{month}/{day}"
			time = f"{hour}:{minute}:{second}"
			result = bot.get_apps_by_id(target, app_id)
			result = result.to_dict
			result = result["apps"][0]
			type = result["type"]
			if type == "Event":
				data = result["event_data"]
				data = data["performer_object"]["object_guid"]
				result = bot.get_info(client.author_guid)
				result = result.to_dict
				guid = result["user"]["user_guid"]
				name = result["user"]["first_name"]
				client.reply(f'''به گروه ما خوش اومدی [عزیزم]({guid}) 🌱😍

● تاریخ:  {date}
● ساعت: {time}''')
		elif text == "یک عضو گروه را ترک کرد.":
			result = bot.get_apps_by_id(target, app_id)
			result = result.apps[0]
			type = result.type
			if type == "Event":
				client.reply("یه خوشتیپ کم شد ):")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش خوش آمد گویی :\n\n{e}")


@bot.on_app_updates(filters.is_text, filters.is_group, filters.commands("تنظیم", ""))
def SetWarn(client: Updates):
	try:
		text:str = client.text
		type = text.split()[1]
		num = text.split()[2]
		if type == "لینک":
			status["num_bans"]["link"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "آیدی":
			status["num_bans"]["id"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "فوروارد":
			status["num_bans"]["forward"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "عکس":
			status["num_bans"]["image"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "فایل":
			status["num_bans"]["file"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "گیف":
			status["num_bans"]["gif"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "ویس":
			status["num_bans"]["voice"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "موسیقی":
			status["num_bans"]["music"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "ویدیو":
			status["num_bans"]["video"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "لوکیشن":
			status["num_bans"]["location"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "استیکر":
			status["num_bans"]["sticker"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "نظرسنجی":
			status["num_bans"]["poll"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "هایپرلینک":
			status["num_bans"]["hyperlink"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "استوری":
			status["num_bans"]["story"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "پیام":
			status["num_bans"]["text"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "فهش":
			status["num_bans"]["fosh"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "کدهنگی":
			status["num_bans"]["code"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		if type == "اخطار":
			status["num_bans"]["warn"] = int(num)
			with open("Files/status.json", "w", encoding="utf-8") as f:
				json.dump(status, f, ensure_ascii=False, indent=4)
			client.reply(f"✅ تعداد اخطار {type} به {num} تغییر کرد.")
		
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش تنظیم اخطار :\n\n{e}")


@bot.on_app_updates(filters.commands("گفتگو خاموش", ""), filters.is_text, filters.is_group)
def Falsesokhan(client: Updates):
	try:
		if client.author_guid in AdminGold:
			global sokhango_status
			sokhango_status = False
			client.reply("سخنگو خاموش شد.")
		else:
			client.reply("زجه نزن ادمین نیستی")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش سخنگو :\n\n{e}")


@bot.on_app_updates(filters.commands("گفتگو روشن", ""), filters.is_text, filters.is_group)
def Truesokhan(client: Updates):
	try:
		if client.author_guid in AdminGold:
			global sokhango_status
			sokhango_status = True
			client.reply("سخنگو روشن شد.")
		else:
			client.reply("زجه نزن ادمین نیستی")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش سخنگو :\n\n{e}")


@bot.on_app_updates(filters.is_text, filters.is_group)
def sokhango(client: Updates):
	text = client.text
	try:
		if sokhango_status:
			if True:
				guid = client.author_guid
				target = client.object_guid
				data = json.loads(open("Files/yad.json", "r",encoding = 'utf-8').read())
				text = client.text.strip()
				if not text:
					return
				if text in data:
					replies = data[text]
					if isinstance(replies, list) and replies:
						reply = choice(replies)
					client.reply(reply)
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش سخنگو :\n\n{e}")


@bot.on_app_updates(filters.is_text)
def AddGroup(client: Updates):
	try:
		guid = client.author_guid
		text = client.text
		if guid == status["maker"]:
			if text.startswith("افزودن گروه"):
				link = text.split()[2]
				time = text.split()[3]
				if link.startswith("https://rubika.ir/joing/"):
					if not time == []:
						if time.isdigit():
							guid = bot.join_group(link)
							guid = guid.group.group_guid
							get = bot.get_group_info(guid)
							get = get.group
							title = get.group_title
							status["groups"][guid] = {"title": title, "time": int(time)}
							with open("Files/status.json", "w", encoding="utf-8") as f:
								json.dump(status, f, ensure_ascii=False, indent=4)
							#get = requests.get(f"http://reza-lucifer.freehost.io/eshterak/eshterak_open.php?user_name={link}&duration={time}").json()
							client.reply(f"گروه « {title} » به گروه های فعال اضافه شد.\n\nمدت اشتراک گروه: {time} روز")
						else:
							client.reply("❗️مدت زمان اشتراک گروه را به صورت «عدد» وارد کنید.")
					else:
						client.reply("مدت اشتراک گروه یافت نشد. ❗️")
				if link.startswith("g0"):
					if not time == []:
						if time.isdigit():
							get = bot.get_group_info(link)
							get = get.group
							title = get.group_title
							status["groups"][link] = {"title": title, "time": int(time)}
							with open("Files/status.json", "w", encoding="utf-8") as f:
								json.dump(status, f, ensure_ascii=False, indent=4)
							#get = requests.get(f"http://reza-lucifer.freehost.io/eshterak/eshterak_open.php?user_name={link}&duration={time}").json()
							client.reply(f"گروه « {title} » به گروه های فعال اضافه شد.\n\nمدت اشتراک گروه: {time} روز")
						else:
							client.reply("❗️مدت زمان اشتراک گروه را به صورت «عدد» وارد کنید.")
					else:
						client.reply("مدت اشتراک گروه یافت نشد. ❗️")
	except Exception as e:
		client.reply(f"خطایی رخ داد در افزودن گروه :\n\n{e}")



@bot.on_app_updates(filters.is_group)
def zed_file(client: Updates):
	try:
		guid = client.author_guid
		target = client.object_guid
		if target in status["groups"]:
			result = True
			if result:
				if not guid in Admins:
					if client.file_inline:
						client.file_inline.type
						if type == "Image":
							if status["locks"]["Photo"]:
								warn_user(client, guid, "photo")
						if type == "Video":
							if status["locks"]["Video"]:
								warn_user(client, guid, "video")
						if type == "Voice":
							if status["locks"]["Voice"]:
								warn_user(client, guid, "voice")
						if type == "Music":
							if status["locks"]["Music"]:
								warn_user(client, guid, "music")
						if type == "File":
							if status["locks"]["File"]:
								warn_user(client, guid, "file")
						if type == "Gif":
							if status["locks"]["Gif"]:
								warn_user(client, guid, "gif")
						if type == "Music":
							if status["locks"]["Music"]:
								warn_user(client, guid, "music")
					else:
						if client.sticker:
							if status["locks"]["Sticker"]:
								warn_user(client, guid, "sticker")
						if client.poll:
							if status["locks"]["Poll"]:
								warn_user(client, guid, "poll")
						if client.location:
							if status["locks"]["Location"]:
								warn_user(client, guid, "location")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش قفل فایل :\n\n{e}")


@bot.on_app_updates(filters.is_group, filters.is_text)
def zed_text(client: Updates):
	try:
		text:str = client.text
		guid = client.author_guid
		target = client.object_guid
		if target in status["groups"]:
			result = True
			if result:
				if not guid in Admins:
					if Link(text):
						warn_user(client, guid, "link")
					if client.is_forward:
						if status["locks"]["Forward"]:
							warn_user(client, guid, "forward")
					if utils.is_username(text):
						if status["locks"]["id"]:
							warn_user(client, guid, "id")
					if client.is_text:
						if status["locks"]["Code"]:
							num = len(text.split("."))
							if num > 10:
								warn_user(client, guid, "code")
					if Fosh(text):
						warn_user(client, guid, "fosh")
					if client.medadata:
						for part in client.metadata.meta_data_parts:
							if part.type == 'Link':
								if status["locks"]["HyperLink"]:
									warn_user(client, guid, "hyperlink")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش قفل لینک :\n\n{e}")

@bot.on_app_updates(filters.is_group, filters.is_text)
def sargarmi(client: Updates):
	try:
		if client.object_guid in status["groups"]:
			target = client.object_guid
			result = True
			if result:
				text:str = client.text
				if text.startswith("بیو"):
					client.reply(s.bio())
				if text.startswith("جوک"):
					client.reply(s.jok())
				if text.startswith("داستان"):
					client.reply(s.dastan())
				if text.startswith("دیالوگ"):
					client.reply(s.dialog())
				if text.startswith("الکی مثلا"):
					client.reply(s.alaky())
				if text.startswith("چالش"):
					client.reply(s.chalesh())
				if text.startswith("تاس"):
					num = ["⬤", "⬤ ⬤", "⬤ ⬤\n⬤", "⬤ ⬤\n⬤ ⬤", "⬤ ⬤\n⬤ ⬤\n⬤", "⬤ ⬤\n⬤ ⬤\n⬤ ⬤"]
					client.reply(choice(num))

	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش سرگرمی :\n\n{e}")


@bot.on_app_updates(filters.is_group, filters.is_text)
def karbordi(client: Updates):
	try:
		text = client.text
		target = client.object_guid
		guid = client.author_guid
		if client.object_guid in status["groups"]:
			target = client.object_guid
			result = True
			if result:
				if text.startswith("کال") or text.startswith("ویسکال"):
					if guid in Admins:
						bot.create_group_voice_chat(target)
						client.reply("✓ ویسکال ایجاد شد.")
				if text.startswith("قطع کال") or text.startswith("قطع ویسکال"):
					if guid in Admins:
						a = app.create_voice_chat(client.object_guid)
						a = a["exist_group_voice_chat"]["voice_chat_id"]
						a = app.discard_voice_chat(target, a)
						client.reply("✓ ویسکال بسته شد.")
				if text.startswith("پین") or text.startswith("سنجاق"):
					if guid in Admins:
						if client.reply_app_id:
							msg_id = client.reply_app_id
							bot.set_pin(target, msg_id)
							client.reply("✓ پیام سنجاق شد.")
				if text.startswith("بن") or text.startswith("ریم") or text.startswith("سیک"):
					if guid in Admins:
						if client.reply_app_id:
							result = bot.get_apps_by_id(client.object_guid, [client.reply_app_id])
							result = result.to_dict.get('apps')[0]
							if not result.get('author_object_guid') in Admins:
								result = bot.get_info(result.get('author_object_guid'))
								result = result.to_dict
								guid = result.get('user').get('user_guid')
								name = result.get('user').get('first_name')
								client.ban_member(client.object_guid, guid)
								client.reply(f"»  کاربر  [{name}]({guid}) بن شد. ↺")
							else:
								client.reply('کاربر مورد نظر در گروه ادمین است.')
						else:
							username = client.text.split()[1].replace("@", "")
							member = bot.get_object_by_username(username)
							guid = member.user.user_guid
							name = member.user.first_name
							bot.ban_member(client.object_guid, guid)
							client.reply(f"»  کاربر  [{name}]({guid}) بن شد. ↺")
				if text.startswith("سکوت"):
					if guid in Admins:
						if client.reply_app_id:
							result = bot.get_apps_by_id(client.object_guid, [client.reply_app_id])
							result = result.to_dict.get('apps')[0]
							if not result.get('author_object_guid') in Admins:
								result = bot.get_info(result.get('author_object_guid'))
								result = result.to_dict
								guid = result.get('user').get('user_guid')
								name = result.get('user').get('first_name')
								Black_List.append(guid)
								client.reply(f"»  کاربر  [{name}]({guid}) ساکت شد. ↺")
							else:
								client.reply('کاربر مورد نظر در گروه ادمین است.')
						else:
							username = client.text.split()[1].replace("@", "")
							member = bot.get_object_by_username(username)
							guid = member.user.user_guid
							name = member.user.first_name
							Black_List.append(guid)
							client.reply(f"»  کاربر  [{name}]({guid}) ساکت شد. ↺")
				
				if text.startswith("حذف سکوت"):
					if guid in Admins:
						if client.reply_app_id:
							result = bot.get_apps_by_id(client.object_guid, [client.reply_app_id])
							result = result.to_dict.get('apps')[0]
							if not result.get('author_object_guid') in Admins:
								result = bot.get_info(result.get('author_object_guid'))
								result = result.to_dict
								guid = result.get('user').get('user_guid')
								name = result.get('user').get('first_name')
								Black_List.remove(guid)
								client.reply(f"»  کاربر  [{name}]({guid}) از لیست سکوت حذف شد. ↺")
							else:
								client.reply('کاربر مورد نظر در گروه ادمین است.')
						else:
							username = client.text.split()[1].replace("@", "")
							member = bot.get_object_by_username(username)
							guid = member.user.user_guid
							name = member.user.first_name
							Black_List.remove(guid)
							client.reply(f"»  کاربر  [{name}]({guid}) از لیست سکوت حذف شد. ↺")
				
				if text.startswith("بستن گروه") or text.startswith("گروه بسته"):
					if guid in Admins:
						bot.set_group_default_access(client.object_guid, [])
						client.reply("گروه با موفقیت بسته شد.")
				if text.startswith("بازکردن گروه") or text.startswith("گروه باز"):
					if guid in Admins:
						bot.set_group_default_access(client.object_guid, ['SendMessages','AddMember','ViewAdmins'])
						client.reply("گروه با موفقیت باز شد.")
				
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش کاربردی :\n\n{e}")


@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands("ثبت لقب", ""))
def savelagb(client: Updates):
	try:
		if client.author_guid in Admins:
			if client.reply_app_id:
				inlagb = client.text.replace("ثبت لقب", "")
				reply_id = client.reply_app_id
				get = bot.get_apps_by_id(client.object_guid, reply_id)
				get = get.apps[0]
				guid = get.author_object_guid
				readli = json.loads("".join(open("Files/lagb.json","r",encoding = "utf-8").read()))
				readli.update(dict({f"{guid}":f"{inlagb}"}))
				wri = open("Files/lagb.json","w", encoding = "utf-8").write(json.dumps(readli))
				client.reply("لقب ثبت شد (:")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش ثبت لقب :\n\n{e}")

@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands("ثبت اصل"))
def saveasl(client: Updates):
	try:
		inasl = client.text.replace("ثبت اصل", "")
		if client.author_guid in Admins:
			if client.reply_app_id:
				reply_id = client.reply_app_id
				get = bot.get_apps_by_id(client.object_guid, reply_id)
				get = get.apps[0]
				readli = json.loads("".join(open("Files/asl.json","r",encoding = "utf-8").read()))
				guid = get.author_object_guid
				if inasl != "":
					readli.update(dict({f"{guid}":f"{inasl}"}))
					wri = open("Files/asl.json","w", encoding = "utf-8").write(json.dumps(readli))
					readli = json.loads("".join(open("Files/asl.json","r",encoding = "utf-8").read()))
					client.reply(f"اصلش ثبت شد ← {inasl}")
				else:
					text = get.text
					readli.update(dict({f"{guid}":f"{text}"}))
					wri = open("Files/asl.json","w", encoding = "utf-8").write(json.dumps(readli))
					readli = json.loads("".join(open("Files/asl.json","r",encoding = "utf-8").read()))
					client.reply("اصلش ثبت شد ← {text}")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش ثبت اصل :\n\n{e}")

msgs, msgs_group = [], []
@bot.on_app_updates(filters.is_group)
def numMessages(client: Updates):
	try:
		guid = client.author_guid
		target = client.object_guid
		msgs.append(guid)
		msgs_group.append(target)
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش شمارش پیام :\n\n{e}")

@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands(["آمارم", "امارم"], ""))
def amaram(client: Updates):
	asl = json.loads(open('Files/asl.json','r',encoding = 'utf-8').read())
	lagb = json.loads(open("Files/lagb.json","r",encoding = "utf-8").read())
	guid = client.author_guid
	try:
		if guid in asl:
			asl = asl[guid]
		else:
			asl = "ناشناس"
		if guid in lagb:
			lagb = lagb[guid]
		else:
			lagb = "لبقی ثبت نشده"
		get = bot.get_info(guid)
		get = get.to_dict
		get = get["user"]
		name = get["first_name"]
		bio = get["bio"]
		num_msg = 0
		num_warrn = 0
		warning_user = json.loads(open("Files/warn_list.json", "r", encoding="utf-8").read())
		if guid in msgs:
			num_msg = msgs.count(guid)
		if guid in warning_user:
			num_warrn = warning_user.count(guid)
		if guid in AdminGold:
			msg = f'''◄  مقام 〔 ادمین ویژه ⭐ 〕

•  اسم : {name}
•  آخرین بازدید : دریافت نشد.
•  لقب : {lagb}
•  اصل : {asl}
•  تعداد پیام : {num_msg}
•  تعداد اخطار : {num_warrn}

•  {guid}

─┅━━━━━━━┅─

{bio}'''
		else:
			msg = f'''◄  مقام 〔 کاربر عادی 👤 〕

•  لقب : {lagb}
•  اصل : {asl}
•  تعداد پیام : {num_msg}
•  تعداد اخطار : {num_warrn}

•  {guid}

─┅━━━━━━━┅─

{bio}'''
		client.reply(msg)
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش آمارم :\n\n{e}")

@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands(["آمارش", "امارش"], ""))
def amaresh(client: Updates):
	asl = json.loads(open('Files/asl.json','r',encoding = 'utf-8').read())
	lagb = json.loads(open("Files/lagb.json","r",encoding = "utf-8").read())
	try:
		if client.reply_app_id:
			reply_id = client.reply_app_id
			get = bot.get_apps_by_id(client.object_guid, reply_id)
			get = get.apps[0]
			guid = get.author_object_guid
			if guid in asl:
				asl = asl[guid]
			else:
				asl = "ناشناس"
			if guid in lagb:
				lagb = lagb[guid]
			else:
				lagb = "لبقی ثبت نشده"
			get = bot.get_info(guid)
			get = get.to_dict
			get = get["user"]
			name = get["first_name"]
			bio = get["bio"]
			num_msg = 0
			num_warrn = 0
			warning_user = json.loads(open("Files/warn_list.json", "r", encoding="utf-8").read())
			if guid in msgs:
				num_msg = msgs.count(guid)
			if guid in warning_user:
				num_warrn = warning_user.count(guid)
			if guid in AdminGold:
				msg = f'''◄  مقام 〔 ادمین ویژه ⭐ 〕

•  اسم : {name}
•  آخرین بازدید : دریافت نشد.
•  لقب : {lagb}
•  اصل : {asl}
•  تعداد پیام : {num_msg}
•  تعداد اخطار : {num_warrn}

•  {guid}

─┅━━━━━━━┅─

{bio}'''
			else:
				msg = f'''◄  مقام 〔 کاربر عادی 👤 〕

•  لقب : {lagb}
•  اصل : {asl}
•  تعداد پیام : {num_msg}
•  تعداد اخطار : {num_warrn}

•  {guid}

─┅━━━━━━━┅─

{bio}'''
			client.reply(msg)
		else:
			client.reply("روی کاربر ریپ بزنید.")
	except Exception as e:
		print(e)

@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands("ویژه", ""))
def setAdminVijie(client: Updates):
	try:
		if client.reply_app_id:
			reply_id = client.reply_app_id
			get = bot.get_apps_by_id(client.object_guid, reply_id)
			get = get.apps[0]
			guid = get.author_object_guid
			get = bot.get_group_admin_members(client.object_guid)
			get = get.to_dict
			get = get["in_chat_members"]
			for data in get:
				type = data["join_type"]
				if type == "Creator":
					mem_guid = data["member_guid"]
					if mem_guid == guid:
						AdminGold.append(guid)
						client.reply("کاربر ادمین ویژه شد.")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش ادمین ویژه :\n\n{e}")


@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands("اصلم", ""))
def aslam(client: Updates):
	try:
		guid = client.author_guid
		asl = json.loads(open("Files/asl.json","r",encoding = "utf-8").read())
		if guid in asl:
			client.reply(f"◉ اصلت » **{asl[guid]}** ๛")
		else:
			client.reply("اصلی برای شما ثبت نشده است.")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش اصلم :\n\n{e}")

@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands("اصلش", ""))
def aslesh(client: Updates):
	try:
		asl = json.loads(open("Files/asl.json","r",encoding = "utf-8").read())
		if client.reply_app_id:
			reply_id = client.reply_app_id
			get = bot.get_apps_by_id(client.object_guid, reply_id)
			get = get.apps[0]
			guid = get.author_object_guid
			if guid in asl:
				client.reply(f"◉ اصلش » **{asl[guid]}** ๛")
			else:
				client.reply("هیچ اصلی ثبت نشده است.")
		else:
			client.reply("روی کاربر ریپ نکرده اید")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش اصلش :\n\n{e}")


#@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands("گروه ها", ""))
#def SendGroup(client: Updates):
#	try:
#		if client.author_guid == status["maker"]:
#			groups = status["groups"]
#			text = ""
#			num = 0
#			for group in groups:
#				title = groups[group]["title"]
#				result = requests.get(f"http://reza-lucifer.freehost.io/eshterak/eshterak.php?user_name={group}").json()
#				time = result["remaining_days"]
#				num += 1
#				text += f'''{num} - {title}  
#⏳ {time} روز
#🔗 {group}  
#━─┅🌀┅─━'''
#			client.reply(text)
#	except Exception as e:
#		client.reply(f"❗️خطایی رخ داد : {e}")



@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands("ارتقا", ""))
def SetAdmin(client: Updates):
	try:
		try:
			with open("Files/status.json", "r", encoding="utf-8") as f:
				status = json.load(f)
		except FileNotFoundError:
			status = {"Admins": []}
		if client.reply_app_id:
			if client.author_guid == status["maker"]:
				reply_id = client.reply_app_id
				get = bot.get_apps_by_id(client.object_guid, [reply_id])
				get = get.apps[0]
				guid = get.author_object_guid
				if guid not in status.get("Admins", []):
					status["Admins"].append(guid)
					with open("Files/status.json", "w", encoding="utf-8") as f:
						json.dump(status, f, ensure_ascii=False, indent=4)
					client.reply("✅ کاربر با موفقیت به لیست ادمین‌ها اضافه شد.")
				else:
					client.reply("ℹ️ این کاربر قبلاً در لیست ادمین‌ها هست.")
			else:
				client.reply("❗️لطفاً دستور را روی پیام یکی از کاربران ریپلای کنید.")
				
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش ارتقا :\n\n{e}")



@bot.on_app_updates(filters.is_group, filters.is_text, filters.commands(["عزل", "تنزیل"], ""))
def RemoveAdmin(client: Updates):
	try:
		try:
			with open("Files/status.json", "r", encoding="utf-8") as f:
				status = json.load(f)
		except FileNotFoundError:
			status = {"Admins": []}
		if client.reply_app_id:
			if client.author_guid == status["maker"]:
				reply_id = client.reply_app_id
				app = bot.get_apps_by_id(client.object_guid, [reply_id]).apps[0]
				user_guid = app.author_object_guid
				if user_guid in status.get("Admins", []):
					status["Admins"].remove(user_guid)
					with open("Files/status.json", "w", encoding="utf-8") as f:
						json.dump(status, f, ensure_ascii=False, indent=4)
	
					client.reply("✅ کاربر با موفقیت از لیست ادمین‌ها حذف شد.")
				else:
					client.reply("ℹ️ این کاربر ادمین نیست.")
			else:
				client.reply("❗️لطفاً دستور را روی پیام کاربر ریپلای کنید.")
	except Exception as e:
		client.reply(f"خطایی رخ داد در بخش تنزیل :\n\n{e}")



bot.run()
