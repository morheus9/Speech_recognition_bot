import datetime
import subprocess
import requests
import telebot
import os
import speech_recognition as sr


logfile = str(datetime.date.today()) + '.log'
token = 'ADD HERE YOUR TOKEN'
bot = telebot.TeleBot(token)


# Function for translating audio, in the format ".wav" to text
def audio_to_text(dest_name: str):
    r = sr.Recognizer()
    # Reading .wav file
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language="ru_RU")
    return result


@bot.message_handler(content_types=['voice'])
def get_audio_messages(message):
    # Accepts the voice from the user
    try:
        file_info = bot.get_file(message.voice.file_id)
        # Path to file (for example: voice/file_2.oga)
        path = file_info.file_path
        # Path to filename (for example: file_2.oga)
        fname = os.path.basename(path)
        # We receive and save the sent voice message
        doc = requests.get(
            'https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        with open(fname+'.oga', 'wb') as f:
            # Saving
            f.write(doc.content)
        # Convertation .oga в .wav with ffmpeg
        process = subprocess.run(['ffmpeg', '-i', fname+'.oga', fname+'.wav'])
        # Calling a function to translate audio into text, and at the same time passing the file names for their subsequent deletion
        result = audio_to_text(fname+'.wav')
        bot.send_message(message.from_user.id, format(result))
    except sr.UnknownValueError as e:
        bot.send_message(message.from_user.id,
                         "Sorry i don't understand your record...")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' +
                    str(message.from_user.last_name) + ':' + str(message.from_user.username) + ':' + ':Message is empty.\n')
    except Exception as e:
        bot.send_message(message.from_user.id,
                         "Something went through the ass, but our brave engineers are already working on a solution... \n or it will just get lost in the logs.")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' +
                    str(message.from_user.last_name) + ':' + str(message.from_user.username) + ':' + ':' + str(e) + '\n')
    finally:
        os.remove(fname+'.wav')
        os.remove(fname+'.oga')


# Check new messages
bot.polling(none_stop=True, interval=0)
