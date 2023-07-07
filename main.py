import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import telebot

TOKEN='6179282994:AAGK7c2yGeuLWkHIpspVzqpxj8mSp_GTZzU'
bot=telebot.TeleBot(TOKEN)

time=datetime.now().date()

# получаем хтмл код страницы
def get_html(url):
    response=requests.get(url)
    return response.text

# главная функция
@bot.message_handler(func=lambda message:True)
def send_message(message):
    i=1
    num=get_data(html)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    buttons = [telebot.types.KeyboardButton(str(i)) for i in range(1,len(num)+1)]
    markup.add(*buttons)
    if message.text=='/start':
        for title in num.values():
            result=title['title']
            bot.send_message(message.chat.id,f'{i}. {result}',reply_markup=markup)
            i+=1
    bot.register_next_step_handler(message,get_message)
  

url="https://kaktus.media/?lable=8&date="+str(time)+"&order=time"
html=get_html(url)

def get_message(message):
    global telurl
    telurl=bot.send_message(message.chat.id,get_data(get_html(url))[int(message.text)]['url'])
    keyboard = telebot.types.ReplyKeyboardMarkup()
    button1 = telebot.types.KeyboardButton('Description')
    button2 = telebot.types.KeyboardButton('Photo')
    button3 = telebot.types.KeyboardButton('Quit')
    keyboard.row(button1, button2,button3)
    bot.send_message(message.chat.id,'some title news you can see Description of this news and Photo',reply_markup=keyboard)
    bot.register_next_step_handler(message,get_desc)


def get_desc(message):
    global telurl
    if message.text=='Description':
        bot.send_message(message.chat.id,get_data(get_html(url))[int(step)]['title'])
    if message.text=='Quit':
        bot.send_message(message.chat.id,'Good bye!')
        bot.stop_bot()
    
    
# получаем нужные нам данный с сайта 
def get_data(html):
    news_dict={}
    soup=bs(html,'lxml')
    news_list=soup.find('div',class_='Tag--articles').find_all('a',class_='ArticleItem--name')
    count=1
    for article in news_list[:20]:
        title_news=article.text.strip()
        news_url=article.get('href')
        news_dict[count]={
                       'title':title_news,
                       'url':news_url
                         }
        count+=1
    return news_dict

# запускает весь код
bot.polling()