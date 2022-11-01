import logging
import random
import playsound
import os
import sqlite3
import wikipedia
from sqlite3 import Error, sqlite_version_info
from gtts import gTTS
from translate import Translator
from camera_config import androidCamera
from dictionaries import bot_greetings_reply, user_greetings_dictionary, bot_greetings_dictionary, translate_dictionary
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{random.choice(bot_greetings_dictionary)}, my name is Athenamylla. {random.choice(bot_greetings_reply)}")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_help = """\n
    Athenamylla can assist you with the following.\n
    /translate (/tr; /trans) + message will return translated version of your message in English;\n
    /sherlock (/sh) + message will return a list(+ text file and no list message if the text file contains 4000+ words) of social media where there is an account with the provided username;\n
    - once you receive the text file, the file is deleted from the server.\n
    /tts + message will convert your message into a voice and send it back to you. The message can be heard on the host;\n
    - once you receive the mp3 file, the file is deleted from the server.\n
    /user - provides the current user username, first name, last name & the chat id;\n
    - this information is being saved in internal database on the server.\n
    /wiki + message will provide a paragraph of information regarding the input message.\n
    /cam + integer will start recording for a while depending on the integer and send you as mp4. (still some issues but working).
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(bot_help))

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translator = Translator(from_lang='autodetect',to_lang='bg')
    text = update.message.text.split(' ', 1)[1]
    translated_reply = translator.translate(text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(translated_reply))
    
async def sherlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='This may take some time, hold on. I will notify you when the investigation is done.')
    sherlock_hook = update.message.text.split(' ', 1)[1]
    os.system(f'python3 /home/icek/Desktop/athenamylla_project/sherlock/sherlock/sherlock/sherlock.py --timeout 3 {sherlock_hook}')
    await context.bot.send_message(chat_id=update.effective_chat.id, text='The investigation is successful. I am sending the report.')
    text_file = open(f'/home/icek/Desktop/athenamylla_project/{sherlock_hook}.txt')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(text_file.read()))
    text_file_large = (f'/home/icek/Desktop/athenamylla_project/{sherlock_hook}.txt')
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(text_file_large, 'rb'))
    print(text_file.read())
    text_file.close()
    os.remove((f'/home/icek/Desktop/athenamylla_project/{sherlock_hook}.txt'))
    
async def tts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.split(' ', 1)[1]
    language = 'en'
    audio = gTTS(text=text, lang=language, slow=False)
    audio_file = (f'{text}.mp3').replace(' ', '_')
    audio.save(audio_file)
    print(audio_file)
    playsound.playsound(f'/home/icek/Desktop/athenamylla_project/{audio_file}')
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(audio_file, 'rb'))
    os.remove((f'/home/icek/Desktop/athenamylla_project/{audio_file}'))

async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = str(update.message.chat.username)
    user_firstname = str(update.message.chat.first_name)
    user_lastname = str(update.message.chat.last_name)
    chat_id = str(update.message.chat_id)
    try:
        sqliteConnection = sqlite3.connect('users.db')
        cursor = sqliteConnection.cursor()
        print('Successful connection!')
        cursor.execute("INSERT INTO USERS VALUES (?, ?, ?, ?)", (username, user_firstname, user_lastname, chat_id))
        sqliteConnection.commit()
        print('Information successfully saved.')
        cursor.close()
        
    except sqlite3.Error as error:
        print('Failed to insert data into sqlite table.', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('The SQLite connection is closed.')
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'username - {username}, first name - {user_firstname}, last name - {user_lastname}, chat ID - {chat_id}')

async def android_cam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_duration = float(update.message.text.split(' ', 1)[1])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Started recording footage at duration argument {video_duration}.\n ')
    video = androidCamera(video_duration)
    video.start_video()
    video_file = open('/home/icek/Desktop/athenamylla_project/outpy.avi')
    await context.bot.send_video(chat_id=update.message.chat_id, video=open('outpy.mp4', 'rb'), supports_streaming=True)


async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_input = str(update.message.text.split(' ', 1)[1])
    wiki_text = wikipedia.page(f'{text_input}')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(wiki_text.summary))

if __name__ == '__main__':
    application = ApplicationBuilder().token('telegram_bot_token').build()
    
    # create_connection('/home/icek/Desktop/athenamylla_project/users.db')
    
    start_handler = CommandHandler(user_greetings_dictionary, start)
    help_handler = CommandHandler('help', help)
    translate_handler = CommandHandler(translate_dictionary, translate)
    sherlock_handler = CommandHandler('sherlock', sherlock)
    tts_handler = CommandHandler('tts', tts)
    user_information_handler = CommandHandler('user', user_info)
    android_camera_handler = CommandHandler('cam', android_cam)
    wiki_handler = CommandHandler('wiki', wiki)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(translate_handler)
    application.add_handler(sherlock_handler)
    application.add_handler(tts_handler)
    application.add_handler(user_information_handler)
    application.add_handler(android_camera_handler)
    application.add_handler(wiki_handler)
    application.run_polling()
