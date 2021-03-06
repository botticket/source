import os
import sys

from config import line_secret, line_access_token
from flask import Flask, request, abort, send_from_directory, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,FollowEvent,QuickReply,QuickReplyButton,MessageAction
from line_notify import LineNotify
from datetime import datetime,date
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

line_secret = "11116494ef78727c367cab0cd4584b9c"
line_access_token = "dOt/F1F30Np2lf95rvGpYlj7w6WVVWKfK66IKtwL1jbD/sMCYcqOeRUiUuO/P6zWGvCr+v3Nf6mfYihfARJyUKvA32Jt/LCL7Im373bQABD0PttiBLkUnVYMp1SVKrYe7FoKEcvsjhkJD/j4hMXZ6wdB04t89/1O/w1cDnyilFU="

channel_secret = line_secret
channel_access_token = line_access_token
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

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
    
    ACCESS_TOKEN = "12CiN1mDzj3q93N5aTYvtWX63XlQOqDs6FWizTRUx1y"
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
                            
            import math
            import warnings
            import numpy as np
            import pandas as pd 
            import matplotlib.pyplot as plt
            warnings.filterwarnings("ignore")
            from pandas_datareader import data 
            from datetime import datetime,date
            from bs4 import BeautifulSoup as soup 
            from urllib.request import urlopen as req
            from urllib.request import Request,urlopen
            from openpyxl import Workbook, load_workbook
            from line_notify import LineNotify
            from scipy.stats import linregress
            import matplotlib.dates as mdates

            code = text_from_user
            ticket = [text_from_user]
            symbols = list(map(lambda e: e + '.bk', ticket))

            def checkmarket(code):
                url = 'https://www.settrade.com/C04_01_stock_quote_p1.jsp?txtSymbol={}&ssoPageId=9&selectPage=1'.format(code)
                webopen = req(url)
                page_html = webopen.read()
                webopen.close()

                data = soup(page_html, 'html.parser')
                price = data.findAll('div',{'class':'col-xs-6'})
                title = price[0].text
                stockprice = price[2].text
                stockprice = stockprice.replace('\n','')
                change = price[3].text
                change = change.replace('\n','')
                change = change.replace('\r','')
                change = change[87:]	
                pbv = data.findAll('div',{'class':'text-right col-xs-4'})
                pbv_rate = pbv[4].text
                pbv_rate = pbv_rate.replace('\n','')
                pbv_rate = pbv_rate.replace(' ','')
                return [title,stockprice,change,pbv_rate]

            st = checkmarket(code)
            text_request = 'ตอนนี้ {} : {} ({})'.format(st[0], st[1], st[2])

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

                    OpenM = dfM['Open'].iloc[0]
                    OpenM  = '%.2f'%OpenM
                    OpenM = str(OpenM)

                    try:
                        Close = float(st[1])
                    except ValueError:
                        Close = dfY['Close'].iloc[-1]

                    Close  = '%.2f'%Close
                    Close = str(Close) 

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

                    exit1 = float(OpenM) * 1.15
                    exit1 = '%.2f'%exit1
                    exit1 = str(exit1)

                    exit2 = float(OpenM) * 1.30
                    exit2 = '%.2f'%exit2
                    exit2 = str(exit2)

                    exit3 = float(OpenM) * 1.45
                    exit3 = '%.2f'%exit3
                    exit3 = str(exit3)

                    buyQ = float(OpenM) * 1.02
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

                    max_valueQ = dfQ.nlargest(1, columns = 'High')
                    max_valueQ = max_valueQ['High'].iloc[0]
                    max_valueQ = '%.2f'%max_valueQ
                    max_valueQ = str(max_valueQ) 

                    min_value = dfQ.nsmallest(1, columns = 'Low')
                    min_value = min_value['Low'].iloc[0]
                    min_value = '%.2f'%min_value
                    min_value = str(min_value) 

                    alert1 = '>> เลย {} ซื้อติดมือ'.format(OpenM)
                    alert2 = '>> กำลังย่อ / ไม่หลุด {} ห่อกลับ'.format(OpenM)
                    alert3 = '>> หลุด {} ลงต่อ'.format(OpenM)
                    
                    
                    text = text_request + '\n' + 'แนวต้าน {} | แนวรับ {}'.format(max_valueQ,min_value) + '\n' 

                    if float(mValue) > 0.00:
                        if  barM > 0:
                            word_to_reply = str( text + alert1 )
                        else:
                            word_to_reply = str( text + alert3 )
                    else:
                        word_to_reply = str( text + alert2 )

                    text_to_reply = TextSendMessage(text = word_to_reply)
                    line_bot_api.reply_message(
                            event.reply_token,
                            messages=[text_to_reply])
                    linechat(word_to_reply)
                    
            for symbol in symbols:
                stock(symbol).ticket()
    except:
        text_list = [
            '{} ไม่มีในฐานข้อมูล {} ลองใหม่อีกครั้ง'.format(text_from_user,disname),
            '{} พิมพ์ชื่อหุ้น {} ไม่ถูกต้อง ลองใหม่อีกครั้ง'.format(disname, text_from_user)]

        from random import choice
        word_to_reply = choice(text_list)        
        text_to_reply = TextSendMessage(text = word_to_reply)

        line_bot_api.reply_message(
                event.reply_token,
                messages=[text_to_reply])

@handler.add(FollowEvent)
def RegisRichmenu(event):
    userid = event.source.user_id
    disname = line_bot_api.get_profile(user_id=userid).display_name
    line_bot_api.link_rich_menu_to_user(userid,'richmenu-073dc85eff8bb8351e8d53769c025029')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 2000))
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)