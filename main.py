from mongodb_manager import DataBaseManagerUser
import telebot
from PIL import Image
import pytesseract
from googletrans import Translator
from telebot import types

TOKEN = "5272226190:AAHvQaAECllfCEFQqpodfspZo1GCi5dw8YE"
bot = telebot.TeleBot(token=TOKEN)

print("started !")


@bot.message_handler(commands=["start"])
def service1_command(message):
    bot.send_message(message.chat.id, f"Hello {bot.user.first_name}")


@bot.message_handler(commands=["register"])
def service2_command(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Send phone",
                                        request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, 'Send Your Phone Number :', reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        if message.from_user.id == message.contact.user_id:
            DataBaseManagerUser.insert_user_data(user_id=message.from_user.id, phone=message.contact.phone_number)
            bot.send_message(message.chat.id, f'Successful | {message.contact.phone_number} Registered')
        else:
            bot.send_message(message.chat.id, 'Failed ! Please Send Your Own Number !')


@bot.message_handler(commands=['check'])
def check_login(message):
    user_id = message.from_user.id
    if DataBaseManagerUser.check_login(user_id):
        bot.send_message(message.chat.id, 'You Are Registered')
    else:
        bot.send_message(message.chat.id, 'Please Use /register for login in this bot')


@bot.message_handler(content_types=['photo'])
def contact(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"{fileID}.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    img = Image.open(f'{fileID}.jpg')
    result = pytesseract.image_to_string(img)
    print(result)
    translation = Translator().translate("hello", dest="fa")
    print(translation.text)
    bot.send_message(message.chat.id, translation.text)


bot.polling()
