import os
import sys

from config import line_secret, line_access_token
from flask import Flask, request, abort, send_from_directory, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,FollowEvent,QuickReply,QuickReplyButton,MessageAction
from line_notify import LineNotify
from datetime import datetime,date

app = Flask(__name__)

line_secret = "11116494ef78727c367cab0cd4584b9c"
line_access_token = "dOt/F1F30Np2lf95rvGpYlj7w6WVVWKfK66IKtwL1jbD/sMCYcqOeRUiUuO/P6zWGvCr+v3Nf6mfYihfARJyUKvA32Jt/LCL7Im373bQABD0PttiBLkUnVYMp1SVKrYe7FoKEcvsjhkJD/j4hMXZ6wdB04t89/1O/w1cDnyilFU="

channel_secret = line_secret
channel_access_token = line_access_token
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

IQXGL = '1780.50'
IQXBRT = '41.61'
IQUSTB = '30.89'
tfex_value = '880.00'
set_value = '1345.60'
#Quarter

today = date.today()
yearly = '{}-01-01'.format(today.year)
monthly = '{}-{}-01'.format(today.year,today.month)

if today.month >= 10 :
    quarter = '{}-10-01'.format(today.year)
    tfex_code = 'S50Z20'
elif today.month >= 7:
    quarter = '{}-07-01'.format(today.year)
    tfex_code = 'S50U20'
elif today.month >= 4 :
    quarter = '{}-04-01'.format(today.year)
    tfex_code = 'S50M20'
else:
    quarter = '{}-01-01'.format(today.year)
    tfex_code = 'S50H20'

def linechat(text):
    
    ACCESS_TOKEN = "oK2sk4w1eidfRyOVfgIcln38TBS8JmL0PgfbbQ8t0Zv"
    notify = LineNotify(ACCESS_TOKEN)
    notify.send(text)

def sendimage(filename):
	file = {'imageFile':open(filename,'rb')}
	payload = {'message': 'update'}
	return _lineNotify(payload,file)

def _lineNotify(payload,file=None):
	import requests
	url = 'https://notify-api.line.me/api/notify'
	token = 'fzU5NggivM0rgd8sDfJjdAP3kMCzU0JzmvbPJGLxZMZ'	#EDIT
	headers = {'Authorization':'Bearer '+token}
	return requests.post(url, headers=headers , data = payload, files=file)

@app.route("/webhook", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text_from_user = event.message.text
    Reply_token = event.reply_token

    userid = event.source.user_id
    disname = line_bot_api.get_profile(user_id=userid).display_name
    request_text= (' bullbot' + '\n' + '>> {} : {}').format(disname,text_from_user)
    
    print(request_text)
    linechat(request_text)

    try:    
        if 'สวัสดี' in text_from_user:    
            text_list = [
                'สวัสดีจ้า คุณ {} '.format(disname),
                'สวัสดีจ้า คุณ {} วันนี้จะเล่นตัวไหนดี'.format(disname),
            ]

            from random import choice
            word_to_reply = choice(text_list)
            text_to_reply = TextSendMessage(text = word_to_reply)
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=[text_to_reply]
                )
            return 'OK'
        elif 'hi' in text_from_user:    
            text_list = [
                'Hello {} '.format(disname),
                'Good day {} '.format(disname),
            ]

            from random import choice
            word_to_reply = choice(text_list)
            text_to_reply = TextSendMessage(text = word_to_reply)
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=[text_to_reply]
                )
            return 'OK'
        else:
                            
            from pandas_datareader import data 
            from datetime import datetime,date
            from bs4 import BeautifulSoup as soup 
            from urllib.request import urlopen as req
            import pandas as pd 
            import numpy as np
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates

            code = text_from_user
            ticket = [text_from_user]
            symbols = list(map(lambda e: e + '.bk', ticket))

            def checkstock(code):

                url = 'https://www.settrade.com/C04_02_stock_historical_p1.jsp?txtSymbol={}&ssoPageId=10&selectPage=2'.format(code)
                webopen = req(url)
                page_html = webopen.read()
                webopen.close()

                data = soup(page_html, 'html.parser')
                price = data.findAll('div',{'class':'col-xs-6'})

                title = price[0].text
                stockprice = price[2].text

                change = price[3].text
                change = change.replace('\n','')
                change = change.replace('\r','')
                change = change.replace('\t','')
                change = change.replace(' ','')
                change = change[11:]

                pchange = price[4].text
                pchange = pchange.replace('\n','')
                pchange = pchange.replace('\r','')
                pchange = pchange.replace(' ','')
                pchange = pchange[12:]

                update = data.findAll('span',{'class':'stt-remark'})
                stockupdate = update[0].text
                stockupdate = stockupdate[13:]
                return [title,stockprice,change,pchange,stockupdate]

            r = checkstock(code)
            text_request = '{} {} ({})'.format(r[0], r[1], r[2])

            class stock:
                def __init__(self,stock):
                    self.stock = stock

                def ticket(self):
                    end = datetime.now()
                    start = datetime(end.year,end.month,end.day)
                    list = self.stock

                    dfY = data.DataReader(f'{list}', data_source="yahoo", start=yearly, end=end)
                    dfQ = data.DataReader(f'{list}', data_source="yahoo", start=quarter, end=end)
                    dfM = data.DataReader(f'{list}', data_source="yahoo", start=monthly, end=end)
                    list = list.replace('.bk','')
                                
                    OpenY = dfY['Open'].iloc[0]
                    OpenY  = '%.2f'%OpenY
                    OpenY = str(OpenY)

                    OpenQ = dfQ['Open'].iloc[0]
                    OpenQ  = '%.2f'%OpenQ
                    OpenQ = str(OpenQ)

                    p_openQ = ((float(OpenQ) - float(OpenY)) / float(OpenY))*100
                    p_openQ  = '%.2f'%p_openQ
                    p_openQ = str(p_openQ)

                    OpenM = dfM['Open'].iloc[0]
                    OpenM  = '%.2f'%OpenM
                    OpenM = str(OpenM)

                    Close = float(f'{r[1]}')
                    Close  = '%.2f'%Close
                    Close = str(Close)

                    barY = ((float(Close) - float(OpenY)) / float(OpenY) )*100
                    barY = '%.2f'%barY
                    barY = float(barY)

                    barQ = ((float(Close) - float(OpenQ)) / float(OpenQ) )*100
                    barQ = '%.2f'%barQ
                    barQ = float(barQ)

                    barM = ((float(Close) - float(OpenM)) / float(OpenM) )*100
                    barM = '%.2f'%barM
                    barM = float(barM)

                    Volume1 = dfY['Volume'].iloc[-1]
                    Volume2 = dfY['Volume'].iloc[-2]

                    Volume = (float(Volume1)+float(Volume2))/2
                    Volume  = '%.0f'%Volume
                    Volume = str(Volume)

                    value = float(Volume) * float(Close)
                    value  = '%.2f'%value
                    value = str(value)

                    request_val = float(value) 
                    request_val  = '{:,.0f}'.format(request_val)
                    request_val = str(request_val)
                    
                    dfQ['mValue'] = (dfQ['Close'] - dfQ['Open']) * dfQ['Volume']
                    mValue = dfQ['mValue'].iloc[-1]
                    mValue = int(mValue)
                    mValue = "{:,}".format(mValue)

                    exit1 = float(OpenQ) * 1.20
                    exit1 = '%.2f'%exit1
                    exit1 = str(exit1)

                    exit2 = float(OpenQ) * 1.40
                    exit2 = '%.2f'%exit2
                    exit2 = str(exit2)

                    exit3 = float(OpenQ) * 1.60
                    exit3 = '%.2f'%exit3
                    exit3 = str(exit3)

                    buyQ = float(OpenQ) * 1.02
                    buyQ = '%.2f'%buyQ
                    buyQ = str(buyQ) 

                    stopQ = float(OpenQ) * 0.98
                    stopQ = '%.2f'%stopQ
                    stopQ = str(stopQ) 

                    buyY = float(OpenY) * 1.02
                    buyY = '%.2f'%buyY
                    buyY = str(buyY) 

                    stopY = float(OpenY) * 0.98
                    stopY = '%.2f'%stopY
                    stopY = str(stopY) 

                    max_value = dfY.nlargest(1, columns = 'High')
                    max_value = max_value['High'].iloc[0]
                    max_value = '%.2f'%max_value
                    max_value = str(max_value) 

                    max_valueQ = dfQ.nlargest(1, columns = 'High')
                    max_valueQ = max_valueQ['High'].iloc[0]
                    max_valueQ = '%.2f'%max_valueQ
                    max_valueQ = str(max_valueQ) 

                    pmax_valueQ = ((float(max_valueQ) - float(OpenQ)) / float(OpenQ)) * 100
                    pmax_valueQ = '%.2f'%pmax_valueQ
                    pmax_valueQ = str(pmax_valueQ)  

                    min_value = dfY.nsmallest(1, columns = 'Low')
                    min_value = min_value['Low'].iloc[0]
                    min_value = '%.2f'%min_value
                    min_value = str(min_value) 

                    pmin_value = ((float(min_value) - float(OpenY)) / float(OpenY)) * 100
                    pmin_value = '%.2f'%pmin_value
                    pmin_value = str(pmin_value)

                    support1 = float(OpenY) * 0.80
                    support1 = '%.2f'%support1
                    support1 = str(support1)

                    support2 = float(OpenY) * 0.70
                    support2 = '%.2f'%support2
                    support2 = str(support2)

                    support3 = float(OpenY) * 0.60
                    support3 = '%.2f'%support3
                    support3 = str(support3)

                    from pyrebase import pyrebase

                    config_firebase = {
                        "apiKey": "AIzaSyC8D2tlkS-qvH27Ivi9W3eKSYC4vzAzwC4",
                        "authDomain": "worldstock-iardyn.firebaseapp.com",
                        "databaseURL": "https://worldstock-iardyn.firebaseio.com",
                        "projectId": "worldstock-iardyn",
                        "storageBucket": "worldstock-iardyn.appspot.com",
                        "messagingSenderId": "80320331665",
                        "appId": "1:80320331665:web:53171e563ead132a03e430"
                    }		

                    firebase = pyrebase.initialize_app(config_firebase)
                    storage = firebase.storage()
                    upload_jpg_firebase = "image/fig.png"	

                    dfQ.dropna(inplace=True)

                    min_value = dfY.nsmallest(1, columns = 'Low')
                    min_value = min_value['Low'].iloc[0]
                    min_value = '%.2f'%min_value
                    min_value = str(min_value) 
                    
                    dfY['OpenY'] = dfY['Open'].iloc[0]
                    dfY['OpenQ'] = dfQ['Open'].iloc[0]
                    dfY['OpenM'] = dfM['Open'].iloc[0]
                    dfY['limitC'] = dfY['OpenY'] *1.02

                    dfY['ExitQ1'] = dfY['OpenQ'] *1.20
                    dfY['ExitQ2'] = dfY['OpenQ'] *1.40
                    dfY['ExitQ3'] = dfY['OpenQ'] *1.60

                    dfY['fibo_Q1'] = dfY['OpenY'] *0.90
                    dfY['fibo_Q2']  = dfY['OpenY'] *0.80
                    dfY['fibo_Q3']  =dfY['OpenY'] *0.70
                    dfY['fibo_Q4'] = dfY['OpenY'] *0.60
                    dfY['fibo_Q5'] = dfY['OpenY'] *0.50
                    dfY['fibo_Q6']  = dfY['OpenY'] *0.40
                    dfY['min_value'] = float(min_value)

                    fig, ax = plt.subplots(figsize=(14,7))

                    dfY['Close'].plot()
                    dfY['OpenQ'].plot(color="#FF0000")
                    dfY['OpenY'].plot(color="#16CE00")

                    dfY['limitC'].plot(color="#00A6FF",linestyle="-.")
                    dfY['min_value'].plot(color="#FFC800",linestyle="-.")		

                    dfY['ExitQ1'].plot(color="#553E3E",linestyle="-.") 
                    dfY['ExitQ2'].plot(color="#553E3E",linestyle="-.") 
                    dfY['ExitQ3'].plot(color="#553E3E",linestyle="-.") 

                    dfY['fibo_Q1'].plot(color="#AEAEAE",linestyle="dotted")
                    dfY['fibo_Q2'].plot(color="#AEAEAE",linestyle="dotted")
                    dfY['fibo_Q3'].plot(color="#AEAEAE",linestyle="dotted")
                    dfY['fibo_Q4'].plot(color="#AEAEAE",linestyle="dotted")
                    dfY['fibo_Q5'].plot(color="#AEAEAE",linestyle="dotted")
                    dfY['fibo_Q6'].plot(color="#AEAEAE",linestyle="dotted")
                    
                    for var in (dfY['Close'],dfY['min_value'], dfY['OpenY'], dfY['OpenQ'],dfY['limitC'], dfY['ExitQ1'], dfY['ExitQ2'], dfY['ExitQ3'], dfY['fibo_Q2'], dfY['fibo_Q4'], dfY['fibo_Q6']):
                        plt.annotate('%0.2f' % var.iloc[-1], xy=(1, var.iloc[-1]), xytext=(6, 0), 
                                    xycoords=('axes fraction', 'data'), textcoords='offset points')

                    ax.xaxis.set_major_locator(mdates.MonthLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                    plt.grid(color="#AEAEAE", alpha=.5, linestyle="dotted")
                    plt.ylabel("Price", fontsize= 12)
                    plt.title(text_request, fontsize= 15)

                    path_png_local = r'C:\Users\Punnawit\Desktop\clone\source\\fig.png'
                    plt.savefig(path_png_local)
                    upload = storage.child(upload_jpg_firebase).put(path_png_local)
                    send_url = 'https://firebasestorage.googleapis.com/v0/b/worldstock-iardyn.appspot.com/o/image%2Ffig.png?alt=media&token=e794bf2f-9208-4656-b15b-36095ff0877c'

                    alert1 = 'Alert : ซื้อ'
                    alert2 = 'Alert : ไปต่อ'
                    alert3 = 'Alert : ขายนั่งรอ'
                    alert4 = 'Alert : อย่าเพิ่งเข้า'
                    alert5 = 'Alert : Vol น้อย'
                    
                    text = '\n' + text_request + '\n' + '{} > {} ({}%)'.format(OpenY,Close,barY) +'\n' + 'B: {} + 2 ช่อง'.format(OpenQ)  + '\n' + 'H: {} | L: {}'.format(max_valueQ,min_value) + '\n' + 'margin {}'.format(mValue) 

                    if float(value) > 7500000:
                        if  barY >= 0.00:
                            if barQ >= 0.00:
                                if 0.00 < barY < 3.00:
                                    word_to_reply = str(alert1 + text)
                                else:
                                    word_to_reply = str(alert2 + text)
                            else:
                                word_to_reply = str(alert4 + text)
                        else:
                            if barQ >= 0.00:
                                if 0.00 < barQ < 3.00:
                                    word_to_reply = str(alert1 + text)
                                else:
                                    word_to_reply = str(alert2 + text)
                            else:
                                word_to_reply = str(alert4 + text)
                    else:
                        word_to_reply = str(alert5 + text)
                    
                    text_to_reply = TextSendMessage(text = word_to_reply)
                    line_bot_api.reply_message(
                            event.reply_token,
                            messages=[text_to_reply]
                        )

                    linechat(send_url)
                    
            for symbol in symbols:
                stock(symbol).ticket()
    except:
        text_list = [
            '{} ไม่มีในฐานข้อมูล {} ลองใหม่อีกครั้ง'.format(text_from_user,disname),
            '{} ค้นหาหุ้น {} ไม่ถูกต้อง ลองใหม่อีกครั้ง'.format(disname, text_from_user),
        ]

        from random import choice
        word_to_reply = choice(text_list)
        
        text_to_reply = TextSendMessage(text = word_to_reply)

        line_bot_api.reply_message(
                event.reply_token,
                messages=[text_to_reply]
            )

@handler.add(FollowEvent)
def RegisRichmenu(event):
    userid = event.source.user_id
    disname = line_bot_api.get_profile(user_id=userid).display_name
    line_bot_api.link_rich_menu_to_user(userid,'richmenu-073dc85eff8bb8351e8d53769c025029')

    button_1 = QuickReplyButton(action=MessageAction(lable='สวัสดี',text='สวัสดี'))
    answer_button = QuickReply(items=[button_1])

if __name__ == '__main__':
    port = int(os.getenv('PORT', 2000))
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)