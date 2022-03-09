from mongodb_manager import DataBaseManagerUser
import telebot
import langid
from PIL import Image
import pytesseract
from googletrans import Translator
from telebot import types
from textblob import TextBlob
import os

TOKEN = "5269440758:AAGwPGbPL5qLbHz4bVDWxRRYHYqLswqurZ0"
bot = telebot.TeleBot(token=TOKEN)

print("started !")


@bot.message_handler(commands=["start"])
def service1_command(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}")


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
    user_id = message.from_user.id
    if DataBaseManagerUser.check_login(user_id):
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"{fileID}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        img = Image.open(f'{fileID}.jpg')
        try:
            result = pytesseract.image_to_string(img)
            if result is not None:
                translation = Translator().translate(result, dest="fa")
                os.system(f"rm -rf {fileID}.jpg")
                bot.send_message(message.chat.id, translation.text)
            else:
                bot.send_message(message.chat.id, "Could Not Find Any Text In This Image")
        except:
            bot.send_message(message.chat.id, "Could Not Find Any Text In This Image")
    else:
        bot.send_message(message.chat.id, 'Please Use /register for login in this bot')


@bot.message_handler()
def translate_texts(message):
    user_id = message.from_user.id
    if DataBaseManagerUser.check_login(user_id):
        lang = langid.classify(f"{message.text}")
        bot.send_message(message.chat.id, f"{lang[0]}")
    else:
        bot.send_message(message.chat.id, 'Please Use /register for login in this bot')


bot.polling()
