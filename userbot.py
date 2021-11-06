from pyrogram import Client, filters
from pyrogram.raw import types, functions

app = Client(
    "app",
    api_id=,
    api_hash="",
)

"""
CREDIT:

👇Telegram-Accountbin👇
https://t.me/joinchat/kPacx29bJZJiMjY0

👇Telegram-Methods & General IT 👇
https://t.me/methodsegeneral
    
"""


_silent = filters.user()


@app.on_message(_silent & filters.private & ~filters.me)
async def _del(_, message):
    await message.delete(revoke=True)


@app.on_message(filters.me & filters.regex(r"^\.(?:un)mute") & filters.private & filters.text)
async def mute(userbot, message):
    if "un" in message.text:
        await message.edit_text("Ora sei libero!")
        return _silent.discard(message.chat.id)
    await message.edit_text("Taci.")
    _silent.add(message.chat.id)


_autoread = filters.chat()


@app.on_message(_autoread)
async def _read(userbot, message):
    await userbot.read_history(chat_id=message.chat.id, max_id=message.id)


@app.on_message(filters.me & filters.regex(r"^\.(?:del)autoread") & filters.private & filters.text)
async def autoread(userbot, message):
    if "del" in message.text:
        await message.edit_text("Autoread attivato!")
        return _autoread.discard(message.chat.id)
    await message.edit_text("Autoread disattivato!")
    _autoread.add(message.chat.id)


@app.on_message(filters.me & filters.command("purge", ".") & ~filters.chat("me") & filters.text)
async def purge(userbot, message):
    await userbot.send(functions.messages.DeleteHistory(peer=app.resolve_peer(message.chat.id), max_id=0, revoke=True))


_replies = {}


@app.on_message(filters.me & filters.command("addreply", ".") & ~filters.chat("me") & filters.text)
async def autoreply(userbot, message):
    try:
        args = message.text.split(maxsplit=2)
        _replies[args[1]] = args[2]
        await message.edit_text("Fatto!")
    except Exception as e:
        await message.edit_text(f"Errore: {e}")


@app.on_message(filters.me & filters.command("delreply", ".") & ~filters.chat("me") & filters.text)
async def delreply(userbot, message):
    try:
        args = message.text.split(maxsplit=1)
        if args[1] in _replies:
            del _replies[args[1]]
        await message.edit_text("Fatto!")
    except Exception as e:
        await message.edit_text(f"Errore: {e}")


@app.on_message(filters.me & filters.command("listautoreply", ".") & ~filters.chat("me") & filters.text)
async def listautoreply(userbot, message):
    await message.edit_text("\n\n".join(f"{key}: {value}" for key, value in _replies.items()) or "Nessuna risposta impostata.")


@app.on_message(filters.me & filters.command("lol", ".") & filters.text)
async def lol(_, message):
    await message.edit_text(
        """
╱┏┓╱╱╱╭━━━╮┏┓╱╱╱╱
╱┃┃╱╱╱┃╭━╮┃┃┃╱╱╱╱
╱┃┗━━┓┃╰━╯┃┃┗━━┓╱
╱┗━━━┛╰━━━╯┗━━━┛╱
        """
    )


@app.on_message(filters.me & filters.command("lol", ".") & filters.text)
async def chatid(_, message):
    await message.edit_text(f"Chat id: {message.chat.id}")


#stampo informazioni dell'user a cui ho risposto al comando
@app.on_message(filters.me & filters.command('info', '.') & filters.reply)
def user_message(client, message):
    try:
        user = message.reply_to_message.from_user

        testo = leggi_json_user(user)

        if user.mention is not None:
            testo = testo + "\n• 🔗PermaLink » " + str(user.mention)

        try:
            if message.command[1] == 'p':
                app.delete_messages(message.chat.id, message.message_id, True)

                if user.photo is not None:
                    app.download_media(user.photo.big_file_id, "userbot_immagini/profile_photo.png")
                    app.send_photo(loggroup_id, "userbot_immagini/profile_photo.png", testo)
                else:
                    app.send_message(loggroup_id, testo)

        except:
            if user.photo is not None:
                app.edit_message_text(message.chat.id, message.message_id, 'Elaborazione...')
                app.download_media(user.photo.big_file_id, "userbot_immagini/profile_photo.png")
                app.send_photo(message.chat.id, "userbot_immagini/profile_photo.png", testo)
            else:
                app.send_message(message.chat.id, testo)
            app.delete_messages(message.chat.id, message.message_id, True)


    except:
        app.edit_message_text(message.chat.id, message.message_id, 'Errore Scannerizzazione')
        sleep(5)
        app.delete_messages(message.chat.id, message.message_id, True)

#recupera informazioni user dall'id
@app.on_message(filters.me & filters.command('idinfo', '.'))
def scan_message(client, message):
    try:
        id_sconosciuto = int(message.command[1])

        user = app.get_chat(id_sconosciuto)
        testo = leggi_json_user(user)

        try:
            if message.command[2] == 'p':
                app.delete_messages(message.chat.id, message.message_id, True)

                if user.photo is not None:
                    app.download_media(user.photo.big_file_id, "userbot_immagini/profile_photo.png")
                    app.send_photo(loggroup_id, "userbot_immagini/profile_photo.png", testo)
                else:
                    app.send_message(loggroup_id, testo)

        except:
            if user.photo is not None:
                app.edit_message_text(message.chat.id, message.message_id, 'Elaborazione...')
                app.download_media(user.photo.big_file_id, "userbot_immagini/profile_photo.png")
                app.send_photo(message.chat.id, "userbot_immagini/profile_photo.png", testo)
                app.delete_messages(message.chat.id, message.message_id, True)
            else:
                app.send_message(message.chat.id, testo)

    except:
        app.edit_message_text(message.chat.id, message.message_id, 'Utente non trovato')
        sleep(5)
        app.delete_messages(message.chat.id, message.message_id, True)

#formatta il json user
def leggi_json_user(user):
    testo = ""
    if user.first_name is not None:
        testo = "• 👤Nome » " + str(user.first_name)

    if user.last_name is not None:
        testo = testo + "\n• 👤Cognome » " + str(user.last_name)

    if user.username is not None:
        testo = testo + "\n• 🌐Username » @" + str(user.username)

    if user.id is not None:
        testo = testo + "\n• 🆔ID» " + str(user.id)

    if user.dc_id is not None:
        testo = testo + "\n• 🌍DC » " + str(user.dc_id)
    return testo


app.run()
