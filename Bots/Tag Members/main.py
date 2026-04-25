from rubpy import Client, filters, utils
from rubpy.types import Updates

bot = Client("Self")

async def all_user(guid):
    get = await bot.get_group_all_members(guid)
    get = get.in_chat_members
    return [guid["member_guid"] for guid in get]

@bot.on_message_updates(filters.is_group)
async def main(app: Updates):
    text = app.text
    target = app.object_guid
    guid = app.author_guid
    print(text)

    if text.startswith("تگ"):
        guids = await all_user(target)
        temp_chunk = []

        for mem in guids:
            try:
                info = await bot.get_user_info(mem)
                if "first_name" in info["user"]:
                    name = info.user.first_name
                    if name == "" or name == " "or name == "‌":
                        name = "بدون‌نام"
                else:
                    name = "بدون‌نام"
            except Exception as e:
                name = "نامشخص"

            mention_text = name
            temp_chunk.append(mention_text)

            if len(temp_chunk) == 5:
                msg = "\n".join(temp_chunk)
                await app.reply(msg)
                temp_chunk = []

        if temp_chunk:
            msg = "\n".join(temp_chunk)
            await app.reply(msg)

bot.run()
