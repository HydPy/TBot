from telegram.ext import Updater,CommandHandler
from telegram import ChatAction
from datetime import datetime, timedelta
from pytz import timezone
from time import sleep
import logging,requests,pytz,re,ast

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater=Updater(token='Telegram-Bot-API-Token')
dispatcher=updater.dispatcher

meetupApi={'sign':'true','key':'Meetup-API-Token'}

utc = pytz.utc

volunteer={}

admins=['list-of-people-who-can-modify-teams']

with open('volunteer.json', 'r') as fp:
    volunteer = ast.literal_eval(fp.read())
    

print("I'm here..!!")

def start(bot, update, args):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text=''
Hi! I have been trained for serving the PyConf Hyderabad Community only!
Enter /help to get /help'')

def mailing_list(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://mail.python.org/mm3/mailman3/lists/hydpy.python.org')

def website(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://http://pyconf.hydpy.org/')

def twitter(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://twitter.com/hydPython')

def meetup(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://www.meetup.com/Hyderabad-Python-Meetup-Group/')

def nextmeetup(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        r=requests.get('http://api.meetup.com/Hyderabad-Python-Meetup-Group/events', params=meetupApi)
        event_link=r.json()[0]['link']
        date_time=r.json()[0]['time']//1000
        utc_dt = utc.localize(datetime.utcfromtimestamp(date_time))
        indian_tz = timezone('Asia/Kolkata')
        date_time=utc_dt.astimezone(indian_tz)
        date_time=date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        if 'venue' in r.json()[0]:
                venue=r.json()[0]['venue']['address_1']
                bot.sendLocation(chat_id=update.message.chat_id, latitude=r.json()[0]['venue']['lat'],longitude=r.json()[0]['venue']['lon'])
        else:
                venue='Help us to decide a venue!'
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup
Date/Time : %s
Venue : %s
Event Page : %s
'''%(date_time, venue, event_link))

def nextmeetups(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        r=requests.get('http://api.meetup.com/Hyderabad-Python-Meetup-Group/events', params=meetupApi)
        #print(re.sub('</a>','',re.sub('<a href="','',re.sub('<br/>',' ',re.sub('<p>',' ',re.sub('</p>','\n',r.json()[0]['description']))))))
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup Schedule
%s
'''%(re.sub('</a>','',re.sub('<a href="','',re.sub('<br/>',' ',re.sub('<p>',' ',re.sub('</p>','\n',r.json()[0]['description'])))))),parse_mode='HTML')

def facebook(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://goo.gl/AxoGMG')

def github(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://github.com/HydPy')

def invitelink(bot,update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://t.me/joinchat/DENc8kJQtctdg3H5JfTXvg')

def help(bot, update):
	bot.sendChatAction(chat_id = update.message.chat_id, action=ChatAction.TYPING)
	sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id, text='''

Use one of the following commands
/mailinglist - PyConf Hyderabad Mailing List link
/twitter - PyConf Hyderabad Twitter Link
/meetuppage - PyConf Hyderabad Meetup page link
/nextmeetup - to get info about next Meetup
/nextmeetupschedule - to get schedule of next Meetup
/facebook - to get a link to Facebook page
/github - to get a link to GitHub Profile
/invitelink - to get an invite link for our Group'''

dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
dispatcher.add_handler(CommandHandler('mailinglist', mailing_list))
dispatcher.add_handler(CommandHandler('website', website))
dispatcher.add_handler(CommandHandler('twitter', twitter))
dispatcher.add_handler(CommandHandler('meetuppage', meetup))
dispatcher.add_handler(CommandHandler('nextmeetup', nextmeetup))
dispatcher.add_handler(CommandHandler('nextmeetupschedule', nextmeetups))
dispatcher.add_handler(CommandHandler('facebook', facebook))
dispatcher.add_handler(CommandHandler('github', github))
dispatcher.add_handler(CommandHandler('invitelink', invitelink))
dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()

