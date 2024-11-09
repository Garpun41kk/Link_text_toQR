import telebot
from PIL import Image
import qrcode
import io

BOT_TOKEN = '7433011948:AAHKonD2aVgjxPe_R2xmR0FtIaeqOMwjThM'  
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Ссылка')
    btn2 = telebot.types.KeyboardButton('Текст')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привет! Выберите, что вы хотите преобразовать в QR-код:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Ссылка', 'Текст'])
def handle_choice(message):
    if message.text == 'Ссылка':
        bot.send_message(message.chat.id, "Введите ссылку:")
        bot.register_next_step_handler(message, generateqrformlink)
    elif message.text == 'Текст':
        bot.send_message(message.chat.id, "Введите текст:")
        bot.register_next_step_handler(message, generateqrfromtext)

def generateqrformlink(message):
    try:
        url = message.text
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        bot.send_photo(message.chat.id, img_buffer, caption="Отсканируйте QR-код, чтобы открыть ссылку в браузере.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

def generateqrfromtext(message):
    try:
        text = message.text
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        bot.send_photo(message.chat.id, img_buffer, caption="Отсканируйте QR-код, чтобы увидеть текст.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка: {e}")
time.sleep(5)