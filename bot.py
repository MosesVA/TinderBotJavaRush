from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *


async def start(update, context):
    dialog.mode = 'main'
    text = load_message('main')
    await send_photo(update, context, 'main')
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        'start': 'главное меню бота',
        'profile': 'генерация Tinder - профля 😎',
        'opener': 'сообщение для знакомства 🥰',
        'message': 'переписка от вашего имени 😈',
        'date': 'переписка со звездами 🔥',
        'gpt': 'задать вопрос чату GPT 🧠'
    })

async def gpt(update, context):
    dialog.mode = 'gpt'
    text = load_message('gpt')
    await send_photo(update, context, 'gpt')
    await send_text(update, context, text)

async def gpt_dialog(update, context):
    text = update.message.text
    promt = load_prompt('gpt')
    answer = await chatgpt.send_question(promt, text)
    await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, '*Привет!*')
        await send_text(update, context, '_Как дела!_')
        await send_text(update, context, 'Вы написали ' + update.message.text)

        await send_photo(update, context, 'avatar_main')
        await send_text_buttons(update, context, 'Запустить процесс?', {
            'start': 'Запустить',
            'stop': 'Остановить',
        })

async def hello_button(update, context):
    query = update.callback_query.data
    if query == 'start':
        await send_text(update, context, 'Процесс запущен!')
    else:
        await send_text(update, context, 'Процесс остановлен!')

dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(
    token='gpt:A02TVYVCwCQQ_OH2tdCyUd2HKqN4GP0xaMtAUWF72T9BdIro0-uIwKS8orBFCeYf_aOW-SBy7xJFkblB3Tz3TILu-3bNVFZqtDZtL5dguxjkKTQ1UO3rumIlFjgYt00HL4xUpvo1IqH_9HI69tGsbgnevKkS')

app = ApplicationBuilder().token("7675209029:AAH_zwrNV_GdRG1makmf5ilubMA5zP9bc_o").build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
