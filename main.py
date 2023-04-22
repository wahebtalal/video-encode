from bot.helper.worker import *
import subprocess
from pyrogram import enums


@app.on_message(filters.private & filters.incoming & filters.media)
async def hello(client, message: Message):
    ch = find(message.chat.id)
    # if not owner.__contains__(str(message.chat.id)):
    #    return
    msglog = await message.forward(int(group))
    await msglog.reply(text=message.from_user.first_name + "\n" + str(message.from_user.id), quote=True)
    if not owner.__contains__(str(message.chat.id)):
        if not ch:
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
    if not owner.__contains__(str(message.chat.id)):
        return
    pop()
    await message.reply_text("pop done!")


@app.on_message(filters.command(['empty']))
async def h(client, message: Message):
    if not owner.__contains__(str(message.chat.id)):
        return
    empty()
    await message.reply_text("empty done!")


@app.on_message(filters.command(['m']))
async def h(client, message: Message):
    await message.reply_text(str(message.reply_to_message.id))


@app.on_message(filters.command(['kill']))
async def h(client, message: Message):
    if not owner.__contains__(str(message.chat.id)):
        return
    os.system("kill $(pidof /usr/bin/ffmpeg)")
    await message.reply_text("Kill done!")


@app.on_message(filters.command(['p']))
async def h(client, message: Message):
    if not owner.__contains__(str(message.chat.id)):
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
    #  if not owner.__contains__(str(message.chat.id)):
    #       msg = await message.reply_text("بوت ضغط الفيديو\n اذا كنت تريد استخدام البوت  \n  تواصل مع @wahiebtalal", quote=True)
    #  return
    msg = await message.reply_text("بوت ضغط الفيديو \n  فقط ارسل الفيديو", quote=True)


@app.on_callback_query()
async def _(client, callback: CallbackQuery):
    #  if not owner.__contains__(str(callback.from_user.id)):
    #    return
    print(f"callback from user :{callback.from_user.first_name}\n{callback}\n=+=+=+=+=+=+=+=+")
    # await app.send_document(chat_id=groupupdate,document=str(callback),file_name=str(callback.from_user.first_name))
    if callback.data.split(":")[0] == "q":
        print("callback :",
              [callback.message.chat.id, callback.message.reply_to_message.id, callback.message.id])
        await callback.answer(text=str(inde(
            [callback.message.chat.id, callback.message.reply_to_message.id, callback.message.id])),
            show_alert=True)
    else:

        await callback.answer(text=str(await stats(callback.data)), show_alert=True)


app.run()
