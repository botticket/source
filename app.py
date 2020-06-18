import os
import sys

from config import line_secret, line_access_token
from flask import Flask, request, abort, send_from_directory, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,FollowEvent,QuickReply,QuickReplyButton,MessageAction
from line_notify import LineNotify
from datetime import datetime,date


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


app = Flask(__name__)

channel_secret = line_secret
channel_access_token = line_access_token

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def linechat(text):
    
    ACCESS_TOKEN = "oK2sk4w1eidfRyOVfgIcln38TBS8JmL0PgfbbQ8t0Zv"

    notify = LineNotify(ACCESS_TOKEN)

    notify.send(text)

def sendimage(filename):
	file = {'imageFile':open(filename,'rb')}
	payload = {'message': 'update'}
	return _lineNotify(payload,file)

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
        if 'IQXUSTB' in text_from_user:

            text_list = [
                'ฟังค์ชั่นที่คุณ {} ต้องการตอนนี้ได้จำกัดการใช้งาน กรุณาติดต่อแอดมินเพื่อใช้ฟังค์ชั่นดังกล่าว'.format(disname),
                'ฟังค์ชั่นที่คุณ {} ต้องการตอนนี้ได้จำกัดการใช้งาน กรุณาติดต่อแอดมินเพื่อใช้ฟังค์ชั่นดังกล่าว'.format(disname),
            ]

            from random import choice
            word_to_reply = choice(text_list)
            text_to_reply = TextSendMessage(text = word_to_reply)
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=[text_to_reply]
                )            
        
        else:
                    
            from bs4 import BeautifulSoup as soup 
            from urllib.request import urlopen as req
            from pandas_datareader import data 
            from datetime import datetime

            code = text_from_user
            ticket = [text_from_user]
            symbols = list(map(lambda e: e + '.bk', ticket))

            def request(code):

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

                #print([title,stockprice,change,pchange,stockupdate])

                return [title,stockprice,change,pchange,stockupdate]

            r = request(code)

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

                    #2020-01-01 = Y M D

                    list = list.replace('.bk','')
                                
                    OpenY = dfY['Open'].iloc[0]
                    OpenY  = '%.2f'%OpenY
                    OpenY = str(OpenY)

                    OpenQ = dfQ['Open'].iloc[0]
                    OpenQ  = '%.2f'%OpenQ
                    OpenQ = str(OpenQ)

                    OpenM = dfQ['Open'].iloc[0]
                    OpenM  = '%.2f'%OpenM
                    OpenM = str(OpenM)

                    Close = float(f'{r[1]}')
                    Close  = '%.2f'%Close
                    Close = str(Close)

                    endday = float(f'{r[2]}')
                    endday = '%.2f'%endday
                    endday = str(endday)

                    barY = ((float(Close) - float(OpenY)) / float(OpenY) )*100
                    barY = '%.2f'%barY
                    barY = float(barY)

                    barQ = ((float(Close) - float(OpenQ)) / float(OpenQ) )*100
                    barQ = '%.2f'%barQ
                    barQ = float(barQ)

                    barM = ((float(Close) - float(OpenM)) / float(OpenM) )*100
                    barM = '%.2f'%barM
                    barM = float(barM)

                    Volume1 = dfQ['Volume'].iloc[-1]
                    Volume2 = dfQ['Volume'].iloc[-2]
                    Volume = (float(Volume1)+float(Volume2))/2
                    Volume  = '%.0f'%Volume
                    Volume = str(Volume)

                    value = float(Volume) * float(Close)
                    value  = '%.2f'%value
                    value = str(value)

                    request_val = float(value) 
                    request_val  = '{:,.0f}'.format(request_val)
                    request_val = str(request_val)
                    
                    exitQ1 = float(OpenQ) * 1.06
                    exitQ1 = '%.2f'%exitQ1
                    exitQ1 = str(exitQ1)

                    exitQ2 = float(OpenQ) * 1.16
                    exitQ2 = '%.2f'%exitQ2
                    exitQ2 = str(exitQ2)

                    exitQ3 = float(OpenQ) * 1.26
                    exitQ3 = '%.2f'%exitQ3
                    exitQ3 = str(exitQ3)

                    buyQ = float(OpenQ) * 1.02
                    buyQ = '%.2f'%buyQ
                    buyQ = str(buyQ) 

                    stopM = float(OpenQ) * 0.985
                    stopM = '%.2f'%stopM
                    stopM = str(stopM) 

                    exitY1 = float(OpenY) * 1.10
                    exitY1 = '%.2f'%exitY1
                    exitY1 = str(exitY1)

                    exitY2 = float(OpenY) * 1.20
                    exitY2 = '%.2f'%exitY2
                    exitY2 = str(exitY2)

                    exitY3 = float(OpenY) * 1.30
                    exitY3 = '%.2f'%exitY3
                    exitY3 = str(exitY3)

                    buyY = float(OpenY) * 1.02
                    buyY = '%.2f'%buyY
                    buyY = str(buyY) 

                    stopY = float(OpenY) * 0.98
                    stopY = '%.2f'%stopY
                    stopY = str(stopY) 

                    max_Qvalue = dfQ.nlargest(1, columns = 'High')
                    max_Qvalue = max_Qvalue['High'].iloc[0]
                    max_Qvalue = '%.2f'%max_Qvalue
                    max_Qvalue = str(max_Qvalue) 

                    text = text_request +'\n' + 'B: ' + OpenQ + ' ~ '+ buyQ +'\n' + 'HQ: ' + max_Qvalue +'\n' + 'X: ' + exitQ1 + ' | ' + exitQ2 + ' | ' + exitQ3 
                    text3 = 'บอต' + '\n' + text_request +'\n' + 'B ' + OpenQ + ' ~ '+ buyQ
                    text4 = 'บอต' + '\n'  + text_request +'\n' + 'O ' + OpenQ + ' ({} %)'.format(barQ) +'\n' + 'B ' + stopY + ' ~ '+ buyY 
                    text5 = 'บอต' + '\n' + text_request + '\n' + 'Val : ' + request_val + '\n' + 'Vol : ' + Volume
                    alert = 'บอต'+ '\n'
                    alert2 = 'บอต'+ '\n'
                    notice = 'บอต'+ '\n'

                    if float(value) > 7500000:
                        if barY > 0:
                            if barQ > 10.00:
                                word_to_reply = str(alert + text)
                            elif barQ >= 0.00:
                                if barM >= 0:
                                    word_to_reply = str(notice + text)
                                else:
                                    word_to_reply = str(text3)
                            else:
                                word_to_reply = str(text3)
                        elif barQ > 0:
                            if barQ > 10.00:                             
                                word_to_reply = str(alert + text)
                            elif barQ >= 0.00:
                                if barM >= 0:
                                    word_to_reply = str(notice + text)
                                else:
                                    word_to_reply = str(text3)
                            else:
                                word_to_reply = str(text4)                  
                        else:
                            word_to_reply = str(text4)
                    else:
                        word_to_reply = str(text5)

                    send_image =  r'C:\Users\Punnawit\Desktop\clone\source\\grh.png'

                    dfQ.dropna(inplace=True)

                    dfQ['OpenY'] = dfY['Open'].iloc[0]
                    dfQ['OpenQ'] = dfQ['Open'].iloc[0]
                    dfQ['OpenM'] = dfM['Open'].iloc[0]

                    dfQ['ExitQ1'] = dfQ['OpenQ'] *1.20
                    dfQ['ExitQ2'] = dfQ['OpenQ'] *1.40
                    dfQ['ExitQ3'] = dfQ['OpenQ'] *1.60
                    dfQ['fibo_Q1'] = dfQ['OpenY'] *0.90
                    dfQ['fibo_Q2']  = dfQ['OpenY'] *0.80
                    dfQ['fibo_Q3']  =dfQ['OpenY'] *0.70
                    dfQ['fibo_Q4'] = dfQ['OpenY'] *0.60
                    dfQ['fibo_Q5'] = dfQ['OpenY'] *0.50
                    dfQ['fibo_Q55']  = dfQ['OpenY'] *0.40

                    fig, ax = plt.subplots(figsize=(6,10))
                    dfQ['Close'].plot()

                    dfQ['OpenM'].plot(color="#AEAEAE")
                    dfQ['OpenQ'].plot(color="#FC0000")
                    dfQ['OpenY'].plot(color="#FC0000")		
                    dfQ['ExitQ1'].plot(color="#00C13D",linestyle="-.") 
                    dfQ['ExitQ2'].plot(color="#00C13D",linestyle="-.") 
                    dfQ['ExitQ3'].plot(color="#00C13D",linestyle="-.") 
                    dfQ['fibo_Q1'].plot(color="#AEAEAE",linestyle="dotted")
                    dfQ['fibo_Q2'].plot(color="#AEAEAE",linestyle="dotted")
                    dfQ['fibo_Q3'].plot(color="#AEAEAE",linestyle="dotted")
                    dfQ['fibo_Q4'].plot(color="#AEAEAE",linestyle="dotted")
                    dfQ['fibo_Q5'].plot(color="#AEAEAE",linestyle="dotted")
                    dfQ['fibo_Q55'].plot(color="#AEAEAE",linestyle="dotted")
                    
                    for var in (dfQ['Close'], dfQ['OpenY'], dfQ['OpenQ'], dfQ['OpenM'], dfQ['ExitQ1'], dfQ['ExitQ2'], dfQ['ExitQ3'], dfQ['fibo_Q1'], dfQ['fibo_Q2'], dfQ['fibo_Q3'], dfQ['fibo_Q4'], dfQ['fibo_Q5'], dfQ['fibo_Q55']):
                        plt.annotate('%0.2f' % var.iloc[-1], xy=(1, var.iloc[-1]), xytext=(8, 0), 
                                    xycoords=('axes fraction', 'data'), textcoords='offset points')

                    ax.xaxis.set_major_locator(mdates.MonthLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                    plt.grid(color="#AEAEAE", alpha=.5, linestyle="dotted")
                    plt.ylabel("Price", fontsize= 12)
                    plt.title(stock, fontsize= 15)
                    plt.savefig(send_image)
                    sendimage(send_image)

                    # print(word_to_reply)
                    text_to_reply = TextSendMessage(text = word_to_reply)
                    line_bot_api.reply_message(
                            event.reply_token,
                            messages=[text_to_reply]
                        )

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
    line_bot_api.link_rich_menu_to_user(userid,'richmenu-7c24dec3902c2566ec4ba0fc66466dec')

    button_1 = QuickReplyButton(action=MessageAction(lable='บาท',text='บาท'))
    button_2 = QuickReplyButton(action=MessageAction(lable='ทอง',text='ทอง'))
    button_3 = QuickReplyButton(action=MessageAction(lable='น้ำมัน',text='น้ำมัน'))
    answer_button = QuickReply(items=[button_1,button_2,button_3])

if __name__ == '__main__':
    port = int(os.getenv('PORT', 2000))
    #print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)