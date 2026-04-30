from rubpy import Client, filters
from rubpy.types import Updates
import audioop
from pydub import AudioSegment
import math, requests

# pip install rubpy requests pydub audioop-lts

bot = Client("session")

Admins = ["u0JdmEn0d729f3d3c1c44dccf92411de"]
Maker = "u0JdmEn0d729f3d3c1c44dccf92411de"
Volom = 100

def reduce_volume_by_percent(input_path, output_path, percent):

    if percent > 100:
        raise ValueError("درصد نمی‌تواند بیشتر از 100 باشد. حداکثر 100 مجاز است.")
    if percent < 0:
        raise ValueError("درصد نمی‌تواند منفی باشد.")
    
    factor = percent / 100.0
    
    if factor == 0:
        db_change = -float('inf')
    else:
        db_change = 20 * math.log10(factor)
    
    audio = AudioSegment.from_file(input_path)
    
    if db_change == -float('inf'):
        new_audio = AudioSegment.silent(duration=len(audio))
    else:
        new_audio = audio + db_change
    
    ext = input_path.split('.')[-1]
    new_audio.export(output_path, format=ext)
    
    print(f"ولوم فایل به {percent}% کاهش یافت (ضریب {factor})")
    print(f"فایل ذخیره شد: {output_path}")

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded += len(chunk)
                percent = (downloaded / total_size) * 100 if total_size > 0 else 0
                a = f"\rstatus: {percent:.1f}%"
    print()

@bot.on_message_updates()
async def main(app: Updates):
    try:
        global Volom
        text = app.text
        guid = app.author_guid
        target = app.object_guid

        if text == "ارتقا":
            if app.reply_message_id:
                reply_id = app.reply_message_id
                get_info = await bot.get_messages_by_id(target, [reply_id])
                guid_user = get_info.messages[0].author_object_guid
                Admins.append(guid_user)
                await app.reply("Set Admin.")
        
        if text == "تنزیل":
            if app.reply_message_id:
                reply_id = app.reply_message_id
                get_info = await bot.get_messages_by_id(target, [reply_id])
                guid_user = get_info.messages[0].author_object_guid
                Admins.remove(guid_user)
                await app.reply("UnSet Admin.")

        if guid not in Admins:
            return

        elif text.startswith("پخش"):
            if app.reply_message_id:
                reply_id = app.reply_message_id
                get_file = await bot.get_messages_by_id(target, [reply_id])
                get_file = get_file.messages[0].file_inline
                file_id = get_file.file_id
                mime = get_file.mime
                await app.reply("Downloading...\nPlease Wait...")
                await bot.download(get_file, "Music")
                await app.reply("Playing...")
                reduce_volume_by_percent(f"Music.{mime}", f"Music.{mime}", Volom)
                await bot.voice_chat_player(target, f"Music.{mime}")
                await app.reply("End Play.")
            else:
                url = text.split()[1]
                if url.startswith("http") and url.endswith(".mp3"):
                    a = await app.reply("Downloading...\nPlease Wait...")
                    download_file(url, "Music.mp3")
                    reduce_volume_by_percent(f"Music.mp3", f"Music.mp3", Volom)
                    await app.reply("Playing...")
                    await bot.voice_chat_player(target, url)
                    await app.reply("End Play.")

        elif text.startswith("تنظیم ولوم"):
            if len(text.split()) == 3:
                Volom = int(text.split()[2])
                await app.reply(f"Set Volum : {Volom}")

    except Exception as e:
        print(e)

bot.run()
