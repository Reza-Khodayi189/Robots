from rubpy import Client, filters
from rubpy.types import Updates
import os, json, random
from time import sleep

bot = Client("Self")

modir = []

random.seed()

WALLET_FILE = "wallets.json"

def format(amount):
    try:
        return f"{int(amount):,}"  # English comma
    except:
        return str(amount)

def load_wallets():
	if os.path.exists(WALLET_FILE):
		with open(WALLET_FILE, "r") as f:
			return json.load(f)
	return {}

def save_wallets():
	with open(WALLET_FILE, "w") as f:
		json.dump(wallets, f)

def get_title(guid):
	get = bot.get_user_info(guid)
	get = get.to_dict
	get = get["user"]
	title = get["first_name"]
	if "username" not in get:
		return {"title": title, "id": None}
	id = get["username"]
	return {"title": title, "id": id}

wallets = load_wallets()


@bot.on_message_updates(filters.is_group, filters.is_text)
def login(m: Updates):
	try:
		text:str = m.text
		guid = m.author_guid
		if text == "بازی":
			if guid not in wallets:
				wallets[guid] = 1000
				save_wallets()
				title = get_title(guid)["title"]
				sleep(1)
				m.reply(f"👤 کاربر گرامی {title} حساب کاربری شما ساخته شد و 1,000 سکه شارژ شد. ✨")
			else:
				title = get_title(guid)["title"]
				sleep(1)
				m.reply(f"👤 کاربر گرامی {title} حساب کاربری شما ساخته شده است. ✓")
	except Exception as e:
		m.reply(e)


@bot.on_message_updates(filters.is_group, filters.is_text)
def shart(m: Updates):
	try:
		text = m.text.strip()
		guid = m.author_guid
		if text.startswith("شرط"):
			if guid in wallets:
				text = text.split()
				if len(text) != 3 or not text[1].isdigit():
					sleep(1)
					m.reply("❗ فرمت درست:\n\nشرط <مقدار> <زوج یا فرد>")
					return
				amount = int(text[1])
				if amount < 100:
					sleep(1)
					m.reply("🔴 حداقل شرط 100 سکه است.")
					return
				if amount > wallets[guid]:
					sleep(1)
					m.reply("❌ موجودی کافی نداری.")
					return
				
				chance = text[2]
				if chance == "فرد" or chance == "زوج":
					chance = ["فرد", "زوج"]
					result = random.choice(chance)
					if result == "زوج":
						wallets[guid] += amount
						sleep(1)
						m.reply(f"🎉 بردی! {format(amount)} سکه گرفتی.\n💼 موجودی:\n{format(wallets[guid])}")
					if result == "فرد":
						wallets[guid] -= amount
						sleep(1)
						m.reply(f"😢 باختی! {format(amount)} سکه از دست دادی.\n💼 موجودی:\n{format(wallets[guid])}")
					save_wallets()
				else:
					m.reply("مقدار نادرست")
			else:
				title = get_title(guid)["title"]
				sleep(1)
				m.reply(f"👤 کاربر گرامی {title} لطفا اول «ثبت نام» بکنید.")
	except Exception as e:
		m.reply(e)

@bot.on_message_updates(filters.is_text, filters.commands("موجودی", ""), filters.is_group)
def mojodi(m: Updates):
	try:
		guid = m.author_guid
		if guid in wallets:
			sleep(1)
			wall = format(wallets[guid])
			m.reply(f"💼 موجودی شما: {wall} سکه")
		else:
			title = get_title(guid)["title"]
			sleep(1)
			m.reply(f"👤 کاربر گرامی {title} لطفا اول «ثبت نام» بکنید.")
	except Exception as e:
		m.reply(e)

@bot.on_message_updates(filters.is_text, filters.commands("برتر", ""), filters.is_group)
def karbran(m: Updates):
	try:
		guid = m.author_guid
		top = sorted(wallets.items(), key=lambda x: x[1], reverse=True)[:5]
		result = "🏆 جدول کاربران برتر بازی\n\n"
		for i, (uid, bal) in enumerate(top, 1):
			try:
				title = get_title(uid)["title"]
			except:
				title = "بدون نام"
			label = title
			result += f"{i}. {label} — {format(bal)} سکه\n"
		sleep(1)
		m.reply(result)
	except Exception as e:
		m.reply(e)

@bot.on_message_updates(filters.is_text, filters.commands("شارژ", ""), filters.is_group)
def sharj(m: Updates):
	try:
		text = m.text.split()
		guid = m.author_guid
		target = m.object_guid
		if guid in modir:
			if m.reply_message_id:
				reply_id = m.reply_message_id
				get = bot.get_messages_by_id(target, reply_id).messages[0]
				user_guid = get.author_object_guid
				if len(text) == 2 and text[1].isdigit():
					amount = int(text[1])
					wallets[user_guid] += amount
					save_wallets()
					title = get_title(user_guid)["title"]
					amount = format(amount)
					sleep(1)
					m.reply(f"✅ {amount} سکه به حساب کاربر {title} اضافه شد.")
				else:
					sleep(1)
					m.reply("💳 فرمت درست:\n🔹 شارژ 1,000 (با ریپلای)")
					return
	except Exception as e:
		m.reply(e)

@bot.on_message_updates(filters.is_group, filters.is_text, filters.commands("انتقال", ""))
def entegal(m: Updates):
	try:
		text = m.text.split()
		target = m.object_guid
		guid = m.author_guid
		if m.reply_message_id:
			reply_id = m.reply_message_id
			get = bot.get_messages_by_id(target, reply_id).messages[0]
			user_guid = get.author_object_guid
			if len(text) != 2 or not text[1].isdigit():
				sleep(1)
				m.reply("❗ فرمت درست: /انتقال <مقدار>")
				return
			amount = int(text[1])
			if amount <= 0:
				sleep(1)
				m.reply("❗️ مقدار انتقال نامعتبر است.")
				return
			if amount > wallets[guid]:
				sleep(1)
				m.reply("❗️ مقدار انتقال بیشتر از موجودی است.")
				return
			if user_guid not in wallets:
				title = get_title(user_guid)["title"]
				sleep(1)
				m.reply(f"❗️ کاربر {title} در ربات «ثبت نام» نکرده است.")
				return
			if guid not in wallets:
				title = get_title(guid)["title"]
				sleep(1)
				m.reply(f"👤 کاربر گرامی {title} لطفا اول «ثبت نام» بکنید.")
			wallets[guid] -= amount
			wallets[user_guid] += amount
			save_wallets()
			title = get_title(user_guid)["title"]
			sleep(1)
			amount = format(amount)
			m.reply(f"✅ {amount} سکه با موفقیت به کاربر {title} منتقل شد.")
	except Exception as e:
		m.reply(e)

@bot.on_message_updates(filters.is_group, filters.is_text, filters.commands("راهنما", ""))
def help(m: Updates):
	try:
		sleep(1)
		m.reply('''📋 دستورات قابل استفاده:

• بازی — ثبت نام در بازی

• شرط 500 « فرد یا زوج» — بخت‌آزمایی سکه‌ای 🎲

• موجودی — ببین چی تو جیبه 😏

• برتر — جدول 5 پولدار اول 💰

•انتقال 500 — انتقال به کسی که ریپلای کردی

• شارژ 1000 — با ریپلای (فقط مدیر)

• راهنما — همین پیامی که الان می‌بینی 📘''')
	except Exception as e:
		m.reply(e)



bot.run()
