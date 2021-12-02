#OSlab_Noe1_bot
import telebot
import random
import persiantools
from telebot import types
from persiantools.jdatetime import JalaliDateTime
import datetime
import qrcode
from PIL import Image
from gtts import gTTS
import os


#you have the token, you are the boss in here
bot = telebot.TeleBot("2144775312:AAGrhjF2FaqI0xFVhHlGLaSDQAX-_9e07A0")
n_r=0
now = JalaliDateTime.now()
#cm = current month....
cm = int(now.month)
cd = int(now.day)
cy = int(now.year)
ar_num=[]
maxe=0
result=0
@bot.message_handler(commands=['start'])
def start(message):
  bot.reply_to(message, "Hello %s welcome to Noe bot-1"%message.from_user.username)


@bot.message_handler(commands=['game'])
def game(message):
  global n_r
  markup = types.ReplyKeyboardMarkup()
  b_new = types.KeyboardButton('new game')
  b_end = types.KeyboardButton('end game')
  markup.row(b_end,b_new)
  bot.reply_to(message, "game started! guess a number (1-51)", reply_markup=markup)
  n_r=random.randint(1,51)
  bot.register_next_step_handler(message,checking)

def checking(message):
    global n_r
    try:
        if message.text == 'new game':
          game(message)
        elif message.text == 'end game':
          help_me(message)
        else :
          u_n = int(message.text)
          if u_n > n_r:
              bot.send_message(message.chat.id,"guess lowere.")
              bot.register_next_step_handler(message,checking)
          elif u_n < n_r:
              bot.send_message(message.chat.id,"guess higher.")
              bot.register_next_step_handler(message,checking)
          else:
              bot.send_message(message.chat.id, "congratulations.")
              bot.register_next_step_handler(message,checking)
    except ValueError:
        bot.send_message(message.chat.id, "try integer")
        bot.register_next_step_handler(message,checking)
@bot.message_handler(commands=['age'])
def age(message):

  bot.reply_to(message, "enter your birth day in jalali like xxxx/... .")
  bot.register_next_step_handler(message,date)

def date(message):
  global cy
  global cm
  global cd
  try:
      birth=message.text.split('/')
      if len (birth) ==3:
        y=int(birth[0])
        m=int(birth[1])
        d=int(birth[2])
        if (cy < y):
          bot.reply_to(message, "you are not born yet. wronge date I guess.")
          bot.register_next_step_handler(message,date)
        elif m>12:
          bot.send_message(message, "invalid month.try again.")
          bot.register_next_step_handler(message,date)
        elif d>365 :
          bot.send_message(message, "invalid day.try again.")
          bot.register_next_step_handler(message,date)
        else:
          if (d > cd):        
              if cm in range (1,7):
                cd = cd + 31
              elif cm==12:
                cd +=29
              else:
                cd+=30
                cm = cm - 1
          if (m > cm):        
            cy = cy - 1
            cm = cm + 12  
          cal_d = cd - d
          cal_m = cm - m
          cal_y = cy - y
          cal_d=str(cal_d) 
          cal_m = str(cal_m)
          cal_y = str(cal_y)
          bot.send_message(message.chat.id,"your age: ")
          bot.send_message(message.chat.id,"year: "+ cal_y+'  months: '+cal_m+'  days: '+cal_d)
      else:
        bot.register_next_step_handler(message,date)
  except ValueError as e:
        masy=bot.reply_to(message, "invalid try again.")
        bot.register_next_step_handler(masy,date) 

@bot.message_handler(commands=['max'])
def max_a(message):
  global ar_num
  global maxe
  global result
  try:
      bot.reply_to(message,"send some numbers az x,y,... .")
      bot.register_next_step_handler(message,max_arn)
  except ValueError as e:
      masy=bot.reply_to(message, "invalid1 try again.")
      bot.register_next_step_handler(masy,max_a)

def max_arn(message):
  global ar_num
  global maxe
  global result
  ar_num = message.text.split(',')
  for i in range((len(ar_num))):
    ar_num[i]=int(ar_num[i])
  maxe = max(ar_num)
  result =  ar_num.index(maxe)
  markup = types.ReplyKeyboardMarkup()
  b_argmax = types.KeyboardButton('index of max num')
  b_max = types.KeyboardButton('value of max num')
  b_end = types.KeyboardButton('end')
  markup.row(b_end,b_argmax,b_max)
  try:
      bot.reply_to(message,"your choice: ",reply_markup=markup)
      bot.register_next_step_handler(message,max_w)
  except ValueError as e:
      masy=bot.reply_to(message, "invalid2 try again.")
      bot.register_next_step_handler(masy,max_arn)
def max_w(message):
  global ar_num
  global maxe
  global result
  try:
      if message.text == 'value of max num':
        maxe=str(maxe)
        bot.send_message(message.chat.id,"maximum value: "+maxe)
        bot.register_next_step_handler(message,max_w)
      elif message.text == 'index of max num':
        result =  ar_num.index(maxe)
        r=str(result)
        bot.send_message(message.chat.id,"index of max num: "+r)
        bot.register_next_step_handler(message,max_w)
      elif message.text == 'end':
        help_me(message)
      else:
        help_me(message)
  except ValueError as e:
      masy=bot.reply_to(message, "invalid3 try again.")
      bot.register_next_step_handler(masy,max_w)

@bot.message_handler(commands=['QR code'])
def qr_code(message):
  try:
      bot.reply_to(message, "enter a string.")
      bot.register_next_step_handler(message,qr_make)
  except:
      bot.send_message(message.chat.id,"try again. ")
      bot.register_next_step_handler(message,qr_code)

def qr_make(message):
  try:
      qrcode_img = qrcode.make(message.text)
      qrcode_img.save("qrcode.png")
      photo = open('qrcode.png', 'rb')
      bot.send_photo(message.chat.id,photo)
  except Exception as e:
    print(e)
    #bot.send_message(message.chat.id,"try again. ")
    #bot.register_next_step_handler(message,qr_code)

@bot.message_handler(commands=['text-speech'])
def text_speech(message):
  try:
      bot.reply_to(message,"enter a sentence in english.")
      bot.register_next_step_handler(message,generate_speech)
  except:
      bot.send_message(message.chat.id,"try again. ")
      bot.register_next_step_handler(message,text_speech)
def generate_speech(message):
  try:
      mytext = message.text
      language = 'en'
      myobj = gTTS(text=mytext, lang=language, slow=False)
      myobj.save("tetosp.mp3")
      audio = open('tetosp.mp3', 'rb')
      bot.send_audio(message.chat.id, audio)
  except:
      bot.send_message(message.chat.id,"try again. ")
      bot.register_next_step_handler(message,generate_speech)

@bot.message_handler(commands=['help'])
def help_me(message):
  bot.reply_to(message, "Menu")
  markup = types.ReplyKeyboardMarkup()
  b_start = types.KeyboardButton('start')
  b_help = types.KeyboardButton('help')
  b_game = types.KeyboardButton('game')
  b_age = types.KeyboardButton('age cal')
  b_max = types.KeyboardButton('max')
  b_qr = types.KeyboardButton('QR')
  b_ts = types.KeyboardButton('text-speech')
  markup.row(b_help,b_qr,b_start)
  markup.row(b_max,b_age,b_game,b_ts)
  bot.reply_to(message, "choose something new.",reply_markup=markup)
@bot.message_handler(func=lambda message: True)
def answer(message):
  if message.text=='start':
    start(message)
  elif message.text=='game':
    game(message)
  elif message.text=='age cal':
    age(message)
  elif message.text=='help':
    help_me(message)
  elif message.text=='max':
    max_a(message)
  elif message.text=='QR':
    qr_code(message)
  elif message.text=='text-speech':
    text_speech(message)
  else:
    help_me(message)

bot.infinity_polling()
