from bot.helper.worker import *
import subprocess
from pyrogram import enums
from bot.helper.db import *


@app.on_message(filters.private & filters.incoming & filters.media)
async def hello(client, message: Message):
    if search(message.chat.id) is None:
        insert(message.chat.id, message.from_user.username, message.from_user.first_name)
    if is_ban(message.chat.id):
        await message.reply_text("تم حظرك ♤\n@wahiebtalal")
        return
    ch = find(message.chat.id)
    # if not owner.__contains__(str(message.chat.id)):
    #    return
    msglog = await message.forward(int(group))
    await msglog.reply(text=message.from_user.first_name + "\n" + str(message.from_user.id), quote=True)
    if not is_admin(message.chat.id):
        if not ch:
            if usage(message.chat.id) < message.video.duration:
                await message.reply_text("ليس لديك الرصيد الكافي \n"
                                         "/limit")
                return
            msg = await message.reply_text("تم الاضافة الى الطابور", quote=True, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="موقعك بالطابور", callback_data="q:" + str(message.id))]]))
            await add_queue([message.chat.id, message.id, msg.id])
        else:
            await app.send_message(chat_id=ch[0], text="لديك عملية بالانتظار", reply_to_message_id=ch[1])

    else:
        msg = await message.reply_text("تم الاضافة الى الطابور", quote=True, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="موقعك بالطابور", callback_data="q:" + str(message.id))]]))
        await add_queue([message.chat.id, message.id, msg.id])


@app.on_message(filters.command(['pop']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    pop()
    await message.reply_text("pop done!")


@app.on_message(filters.command(['empty']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    empty()
    await message.reply_text("empty done!")


@app.on_message(filters.command(['m']))
async def h(client, message: Message):
    await message.reply_text(str(message.reply_to_message.id))


@app.on_message(filters.command(['kill']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    os.system("kill $(pidof /usr/bin/ffmpeg)")
    await message.reply_text("Kill done!")


@app.on_message(filters.command(['admin']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    if len(message.command) < 2:
        await message.reply_text("خطا!")
        return
    admin(message.command[1])
    await app.send_message(message.command[1], "لقد تم ترقيتك الى مشرف ♤")
    await message.reply_text(" done!")


@app.on_message(filters.command(['unadmin']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    if len(message.command) < 2:
        await message.reply_text("خطا!")
        return
    unadmin(message.command[1])
    await app.send_message(message.command[1], "لم تعد مشرفاً بعد الآن ♤")
    await message.reply_text(" done!")


@app.on_message(filters.command(['ban']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    if len(message.command) < 2:
        await message.reply_text("خطا!")
        return
    ban(message.command[1])
    await message.reply_text(" done!")


@app.on_message(filters.command(['unban']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    if len(message.command) < 2:
        await message.reply_text("خطا!")
        return
    unban(message.command[1])
    await app.send_message(message.command[1], "تم إلغاء الحظر ♤")
    await message.reply_text(" done!")


@app.on_message(filters.command(['slimit']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    if len(message.command) < 3:
        await message.reply_text("خطا!")
        return
    print(message.command)
    set_limit(message.command[1], message.command[2])
    await message.reply_text(" done!")


@app.on_message(filters.command(['sl']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    if len(message.command) < 2:
        await message.reply_text("الامر المدخل غير صحيح !")
        return
    set_limit_all(message.command[1])
    await message.reply_text(" done!")


@app.on_message(filters.command(['limit']))
async def lim(client, message: Message):
    if is_ban(message.chat.id):
        await message.reply_text("تم حظرك ♤\n@wahiebtalal")
        return

    limit = usage(message.chat.id).__int__()
    minutes = (limit / 60).__int__()
    sec = (limit % 60).__int__()
    mess = minutes.__str__() + " دقيقة "
    if sec > 0:
        mess += " و "
        mess += sec.__str__()
        mess += " ثانية "
    mess += "لهذا اليوم ♤"

    await message.reply_text(mess)


@app.on_message(filters.command(['p']))
async def h(client, message: Message):
    if not is_admin(message.chat.id):
        return
    proc = subprocess.Popen(message.text.replace('/p', ''), stdout=subprocess.PIPE, shell=True)
    (ou, err) = proc.communicate()
    out = ou if ou is not None else err
    outlist = [out[i:i + 4000] for i in range(0, len(out), 4000)]
    for i in outlist:
        await message.reply_text(["Output: ", i], parse_mode=enums.ParseMode.MARKDOWN)
    print("program output:", out)


@app.on_message(filters.private & filters.incoming)
async def hello(client, message: Message):
    if search(message.chat.id) is None:
        insert(message.chat.id, message.from_user.username, message.from_user.first_name)
    if is_ban(message.chat.id):
        await message.reply_text("تم حظرك ♤\n@wahiebtalal")
        return
    msg = await message.reply_text("بوت ضغط الفيديو \n  فقط ارسل الفيديو", quote=True)


@app.on_callback_query()
async def _(client, callback: CallbackQuery):
    if callback.data.split(":")[0] == "q":
        await callback.answer(text=str(inde(
            [callback.message.chat.id, callback.message.reply_to_message.id, callback.message.id])),
            show_alert=True)
    else:

        await callback.answer(text=str(await stats(callback.data)), show_alert=True)


app.run()
