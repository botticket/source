import os
import sys

from flask import Flask, request, abort, send_from_directory, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,FollowEvent,QuickReply,QuickReplyButton,MessageAction
from line_notify import LineNotify
from reply import reply_msg , SetMessage_Object
from flex_crypto import *
from dialogflow_uncle import detect_intent_texts
from datetime import datetime,date

app = Flask(__name__)

line_secret = "11116494ef78727c367cab0cd4584b9c"
line_access_token = "dOt/F1F30Np2lf95rvGpYlj7w6WVVWKfK66IKtwL1jbD/sMCYcqOeRUiUuO/P6zWGvCr+v3Nf6mfYihfARJyUKvA32Jt/LCL7Im373bQABD0PttiBLkUnVYMp1SVKrYe7FoKEcvsjhkJD/j4hMXZ6wdB04t89/1O/w1cDnyilFU="

channel_secret = line_secret
channel_access_token = line_access_token
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

today = date.today()

start_year = today.year - 1
start_year = '{}-{}-01'.format(start_year,today.month)

yearly = '{}-01-01'.format(today.year)
monthly = '{}-{}-01'.format(today.year,today.month)

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
    request_text= ('ticket02' + '\n' + '>> {} : {}').format(disname,text_from_user)
    
    print(request_text)
    linechat(request_text)

    try:    
        if 'สวัสดี' in text_from_user:    
            text_list = ['สวัสดีจ้า คุณ {} '.format(disname),
                        'สวัสดีจ้า คุณ {} วันนี้จะเล่นตัวไหนดี'.format(disname)]
            from random import choice
            word_to_reply = choice(text_list)
            text_to_reply = TextSendMessage(text = word_to_reply)
            line_bot_api.reply_message(event.reply_token,messages=[text_to_reply])
            return 'OK'

        else:
            from bs4 import BeautifulSoup as soup
            from urllib.request import urlopen as req
            from pandas_datareader import data
            from datetime import datetime, date
            from scipy.stats import linregress
            import math
            import numpy as np
            import pandas as pd  

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
                comvlue = data.findAll('div',{'class':'col-xs-4'})
                comvlue = comvlue[6].text
                comvlue = comvlue.replace(',','')
                comvlue = format(float(comvlue),'')
                comvluee = format(float(comvlue),',')
                return [title,stockprice,change,comvlue,comvluee]

            st = checkmarket(code)
            text_request = '{} {} ({})'.format(st[0], st[1], st[2])

            class stock:
                def __init__(self,stock):
                    self.stock = stock

                def ticket(self):
                    end = datetime.now()
                    start = datetime(end.year,end.month,end.day)
                    list = self.stock
                    
                    dfall = data.DataReader(f'{list}', data_source="yahoo",start=start_year, end=end)
                    
                    try:
                        dfY = data.DataReader(f'{list}', data_source="yahoo", start=yearly, end=end)
                    except ValueError:
                        dfY = data.DataReader(f'{list}', data_source="yahoo", start=start_year, end=end)

                    try:
                        dfM = data.DataReader(f'{list}', data_source="yahoo", start=monthly, end=end)
                    except ValueError:
                        dfM = data.DataReader(f'{list}', data_source="yahoo", start=start_year, end=end)

                    list = list.replace('.bk','') 

                    stock = f'{list}'
                    dfall.dropna(inplace=True)

                    try:
                        Close = float(st[1])
                    except ValueError:
                        Close = dfall['Close'].iloc[-1]

                    Close  = '%.2f'%Close
                    Close = str(Close) 

                    Open_all = dfall['Open'].iloc[0]
                    Open_all  = '%.2f'%Open_all
                    Open_all = str(Open_all)

                    Chg_all = ((float(Close) - float(Open_all))/ float(Open_all))*100
                    Chg_all = '%.2f'%Chg_all
                    Chg_all = str(Chg_all)

                    OpenY = dfY['Open'].iloc[0]
                    OpenY  = '%.2f'%OpenY
                    OpenY = str(OpenY)

                    ChgY = ((float(Close) - float(OpenY)) / float(OpenY) )*100
                    ChgY = '%.2f'%ChgY
                    ChgY = str(ChgY)

                    OpenM = dfM['Open'].iloc[0]
                    OpenM  = '%.2f'%OpenM
                    OpenM = str(OpenM)

                    ChgM = ((float(Close) - float(OpenM)) / float(OpenM) )*100
                    ChgM = '%.2f'%ChgM
                    ChgM = str(ChgM)

                    try:
                        today_chg = float(st[2])
                    except ValueError:
                        today_chg = float(dfall['Close'].iloc[-1]) - float(dfall['Close'].iloc[-2])

                    today_chg  = '%.2f'%today_chg
                    today_chg = str(today_chg)

                    def computeRSI (data, time_window):
                        diff = data.diff(1).dropna()
                        up_chg = 0 * diff
                        down_chg = 0 * diff
                        up_chg[diff > 0] = diff[ diff>0 ]    
                        down_chg[diff < 0] = diff[ diff < 0 ]
                        up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
                        down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
                        rs = abs(up_chg_avg/down_chg_avg)
                        rsi = 100 - 100/(1+rs)
                        return rsi

                    dfall['RSI'] = computeRSI(dfall['Close'], 35)
                    m_RSI = dfall['RSI'].iloc[-1]
                    m_RSI = '%.2f'%m_RSI
                    m_RSI = str(m_RSI)

                    #copy dataframeY
                    dfall = dfall.copy()
                    dfall['date_id'] = ((dfall.index.date - dfall.index.date.min())).astype('timedelta64[D]')
                    dfall['date_id'] = dfall['date_id'].dt.days + 1

                    # high trend lineY
                    dfall_mod = dfall.copy()
                    while len(dfall_mod)>3:
                        reg = linregress(x=dfall_mod['date_id'],y=dfall_mod['Close'],)
                        dfall_mod = dfall_mod.loc[dfall_mod['Close'] > reg[0] * dfall_mod['date_id'] + reg[1]]
                    reg = linregress(x=dfall_mod['date_id'],y=dfall_mod['Close'],)
                    dfall['high_trend'] = reg[0] * dfall['date_id'] + reg[1]

                    # low trend lineY
                    dfall_mod = dfall.copy()
                    while len(dfall_mod)>3:
                        reg = linregress(x=dfall_mod['date_id'],y=dfall_mod['Close'],)
                        dfall_mod = dfall_mod.loc[dfall_mod['Close'] < reg[0] * dfall_mod['date_id'] + reg[1]]
                    reg = linregress(x=dfall_mod['date_id'],y=dfall_mod['Close'],)
                    dfall['low_trend'] = reg[0] * dfall['date_id'] + reg[1]

                    min_Y = dfall.nsmallest(1, columns='Low')
                    min_Y = min_Y['Low'].iloc[-1]
                    min_Y = '%.2f'%min_Y
                    min_Y = str(min_Y)

                    max_Y = dfall.nlargest(1, columns='High')
                    max_Y = max_Y['High'].iloc[-1]
                    max_Y = '%.2f'%max_Y
                    max_Y = str(max_Y)

                    dfall['min_Y'] = float(min_Y)
                    dfall['max_Y'] = float(max_Y)

                    dfall['Open_all'] = dfall['Open'].iloc[0]
                    dfall['ema'] = dfall['Close'].rolling(35).mean()
                    dfY['OpenY'] = dfY['Open'].iloc[0]

                    ema = dfall['ema'].iloc[-1]
                    ema = '%.2f'%ema
                    ema = str(ema)

                    pema = ((float(Close) - float(ema)) / float(ema))*100
                    pema = '%.2f'%pema
                    pema = str(pema)

                    high_trend = dfall['high_trend'].iloc[-1]
                    high_trend = '%.2f'%high_trend
                    high_trend = str(high_trend)

                    if float(ChgM) >= 0.0 :
                        trendM = ' '
                    else:
                        trendM = 'X'

                    if float(ChgY) >= 0 :
                        trendAll = '▲'
                        if float(Close) >= float(OpenM) :
                            if float(Close) >= float(ema):
                                trendY = '©'
                            else:
                                trendY = ' '
                        else:
                            trendY = ' '
                    else:
                        trendAll = '▼'
                        if float(Close) >= float(OpenM) :
                            if float(Close) >= float(ema):
                                trendY = '℗'
                            else:
                                trendY = ' '
                        else:
                            trendY = ' '

                    if float(today_chg) >= 0:
                        if float(Close) > float(OpenY):
                            if float(Close) >= float(OpenM) :
                                if float(Close) >= float(ema):
                                    notice = f'หุ้นเก็บของ {OpenM}'
                                else:
                                    notice = f'หุ้นราคาหลุด {ema}'
                            else:
                                notice = f'หุ้นมีเท {OpenM}'
                        elif float(Close) >= float(OpenM) :
                            if float(Close) >= float(ema):
                                notice = f'หุ้นมีแรงซื้อ {OpenM}'
                            else:
                                notice = f'หุ้นราคาหลุด {ema}'
                        elif float(Close) >= float(ema):
                            notice = f'หุ้นกลับตัวเมื่อเลยราคา {ema}'
                        else:
                            notice = f'หุ้นโดนเท {ema}'
                    else:
                        notice = f'กำลังย่อ/ปรับฐาน \nไม่หลุด {ema} ห่อกลับ'
                        
                    stocknrequest = st[0]
                    text_return = f'ตอนนี้ {stocknrequest} \nราคา {Close} ({today_chg}) \n{notice} \n>> แนวต้าน {max_Y}'
                    word_to_reply = str(text_return)
                    text_to_reply = TextSendMessage(text = word_to_reply)
                    line_bot_api.reply_message(event.reply_token,messages=[text_to_reply])
                    linechat(word_to_reply)

            for symbol in symbols:
                stock(symbol).ticket()
    except:
        text_list = ['{} ไม่มีในฐานข้อมูล {} ลองใหม่อีกครั้ง'.format(text_from_user,disname),
            '{} ค้นหาหุ้น {} ไม่ถูกต้อง ลองใหม่อีกครั้ง'.format(disname, text_from_user)]

        from random import choice
        word_to_reply = choice(text_list)
        text_to_reply = TextSendMessage(text = word_to_reply)
        line_bot_api.reply_message(event.reply_token,messages=[text_to_reply])

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