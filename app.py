import os
import sys

from config import line_secret, line_access_token
from flask import Flask, request, abort, send_from_directory, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,FollowEvent,QuickReply,QuickReplyButton,MessageAction
from line_notify import LineNotify

app = Flask(__name__)

channel_secret = line_secret
channel_access_token = line_access_token

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def linechat(text):
    
    ACCESS_TOKEN = "oK2sk4w1eidfRyOVfgIcln38TBS8JmL0PgfbbQ8t0Zv"

    notify = LineNotify(ACCESS_TOKEN)

    notify.send(text)

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

            from urllib.request import Request, urlopen
            from bs4 import BeautifulSoup as soup 

            def usdcheck():
                IQXUSTHB = '29.74'
                req = Request('https://th.investing.com/currencies/usd-thb', headers={'User-Agent': 'Chrome/78.0'})
                webopen = urlopen(req).read()

                data = soup(webopen, 'html.parser')

                usthbrate = data.findAll('div',{'class':'top bold inlineblock'})
                usthbrate = usthbrate[0].text
                usthbrate = usthbrate.replace('\n',' ')
                usthbrate = usthbrate.replace(',','')
                usthbrate = usthbrate[1:]
                usthbrate = usthbrate[0:6]

                xusthbrate = data.findAll('div',{'class':'top bold inlineblock'})
                xusthbrate = xusthbrate[0].text
                xusthbrate = xusthbrate.replace('\n',' ')
                xusthbrate = xusthbrate.replace(',','')
                xusthbrate = xusthbrate[1:]
                xusthbrate = xusthbrate[7:13]

                usthbspot = float(usthbrate)
                usthbspot = '%.2f'%usthbspot

                buy = float(usthbspot) + 0.02 #dif rate buy
                buy = '%.2f'%buy
                sale = float(usthbspot) - 0.06 #dif rate sale
                sale = '%.2f'%sale

                text1 = 'IQXUSTB >> ' 
                text2 = '\n' + IQXUSTHB +' >> ' + usthbrate + ' (' + xusthbrate + ')' + '\n' + 'ซื้อ ' + sale + ' / ขาย '+ buy

                if float(usthbspot) >= float(IQXUSTHB):
                    word_to_reply2 = text1 + 'ค่าเงินอ่อน' + text2
                else:
                    word_to_reply2 = text1 + 'ค่าเงินแข็ง' + text2
                
                print(word_to_reply2)
                word_to_reply1 = '{} '.format(disname) + 'ค้นข้อมูล ' + text_from_user

                text_to_reply1 = TextSendMessage(text = word_to_reply1)
                text_to_reply2 = TextSendMessage(text = word_to_reply2)

                line_bot_api.reply_message(
                        event.reply_token,
                        messages=[text_to_reply2]
                    )

            usdcheck()

        elif 'IQXWTI' in text_from_user:
            from urllib.request import Request, urlopen
            from bs4 import BeautifulSoup as soup 

            def wticheck():
                IQXWTI = '61.35'
                req = Request('https://th.investing.com/commodities/crude-oil', headers={'User-Agent': 'Chrome/78.0'})
                webopen = urlopen(req).read()

                data = soup(webopen, 'html.parser')

                wtirate = data.findAll('div',{'class':'top bold inlineblock'})
                wtirate = wtirate[0].text
                wtirate = wtirate.replace('\n',' ')
                wtirate = wtirate.replace(',','')
                wtirate = wtirate[1:]
                wtirate = wtirate[0:6]

                xwtirate = data.findAll('div',{'class':'top bold inlineblock'})
                xwtirate = xwtirate[0].text
                xwtirate = xwtirate.replace('\n',' ')
                xwtirate = xwtirate.replace(',','')
                xwtirate = xwtirate[1:]
                xwtirate = xwtirate[6:11]

                wtispot = float(wtirate)
                wtispot = '%.2f'%wtispot

                text1 = 'IQXWTI >> ' 
                text2 = '\n' + IQXWTI +' >> ' + wtispot + ' (' + xwtirate + ')'

                if float(wtispot) >= float(IQXWTI):
                    word_to_reply2 = text1 + 'Long' + text2
                else:
                    word_to_reply2 = text1 + 'Short' + text2
                
                print(word_to_reply2)
                word_to_reply1 = '{} '.format(disname) + 'ค้นข้อมูล ' + text_from_user

                text_to_reply1 = TextSendMessage(text = word_to_reply1)
                text_to_reply2 = TextSendMessage(text = word_to_reply2)

                line_bot_api.reply_message(
                        event.reply_token,
                        messages=[text_to_reply2]
                    )
            wticheck()

        elif 'IQXGL' in text_from_user:
            from urllib.request import Request, urlopen
            from bs4 import BeautifulSoup as soup 
            def goldcheck():
                IQXGL = '1517.2'

                req = Request('https://th.investing.com/currencies/xau-usd', headers={'User-Agent': 'Chrome/78.0'})
                webopen = urlopen(req).read()

                data = soup(webopen, 'html.parser')

                goldrate = data.findAll('div',{'class':'top bold inlineblock'})
                goldrate = goldrate[0].text
                goldrate = goldrate.replace('\n',' ')
                goldrate = goldrate.replace(',','')
                goldrate = goldrate[1:]
                goldrate = goldrate[0:8]

                xgoldrate = data.findAll('div',{'class':'top bold inlineblock'})
                xgoldrate = xgoldrate[0].text
                xgoldrate = xgoldrate.replace('\n',' ')
                xgoldrate = xgoldrate.replace(',','')
                xgoldrate = xgoldrate[9:]
                xgoldrate = xgoldrate[0:5]

                gspot = float(goldrate)
                gspot = '%.2f'%gspot

                text1 = 'IQXGL >> ' 
                text2 = '\n' + IQXGL +' >> ' + gspot + ' (' + xgoldrate + ')'

                if float(gspot) >= float(IQXGL):
                    word_to_reply2 = text1 + 'Long' + text2
                
                else:
                    word_to_reply2 = text1 + 'Short' + text2

                print(word_to_reply2)
                word_to_reply1 = '{} '.format(disname) + 'ค้นข้อมูล ' + text_from_user

                text_to_reply1 = TextSendMessage(text = word_to_reply1)
                text_to_reply2 = TextSendMessage(text = word_to_reply2)

                line_bot_api.reply_message(
                        event.reply_token,
                        messages=[text_to_reply2]
                    )
            goldcheck()

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
                    start = datetime(end.year -1,end.month,end.day)
                    list = self.stock

                    dfY = data.DataReader(f'{list}', data_source="yahoo", start='2020-01-01', end=end)
                    dfM = data.DataReader(f'{list}', data_source="yahoo", start='2020-01-01', end=end)
                    #2020-01-01 = Y M D

                    list = list.replace('.bk','')
                                
                    OpenY = dfY['Open'].iloc[0]
                    OpenY  = '%.2f'%OpenY
                    OpenY = str(OpenY)

                    OpenM = dfM['Open'].iloc[0]
                    OpenM  = '%.2f'%OpenM
                    OpenM = str(OpenM)

                    Close = float(f'{r[1]}')
                    Close  = '%.2f'%Close
                    Close = str(Close)

                    endday = float(f'{r[2]}')
                    endday = '%.2f'%endday
                    endday = str(endday)

                    barY = ((float(Close) - float(OpenY)) / float(OpenY) )*100
                    barY = float(barY)

                    barM = ((float(Close) - float(OpenM)) / float(OpenM) )*100
                    barM = '%.2f'%barM
                    barM = float(barM)

                    chg = barY
                    chg  = '%.2f'%chg
                    chg = str(chg)

                    exit1 = float(OpenY) * 1.06
                    exit1 = '%.2f'%exit1
                    exit1 = str(exit1)

                    exit2 = float(OpenY) * 1.16
                    exit2 = '%.2f'%exit2
                    exit2 = str(exit2)

                    buy1 = float(OpenM) * 1.01
                    buy1 = '%.2f'%buy1
                    buy1 = str(buy1) 

                    stop = float(OpenY) * 0.985
                    stop = '%.2f'%stop
                    stop = str(stop) 

                    text = text_request +'\n' + 'B ' + stop + ' ~ '+ buy1 +'\n' + 'X ' + exit1 + ' | ' + exit2 
                    text2 = 'มีแรงขาย' + '\n' + text_request +'\n' + 'B ' + stop + ' ~ '+ buy1
                    alert = '\n' + 'เลย {} ทยอยขาย'.format(exit1)

                    if barY >= 0:
                        if barM > 6.00:
                            word_to_reply2 = str(text + alert)
                        elif barM >= 0.00:
                            word_to_reply2 = str(text)
                        else:
                            word_to_reply2 = str(text2)
                    elif barM >= 0:
                        if barM > 6.00:
                            word_to_reply2 = str(text + alert)
                        elif barM >= 0.00:
                            word_to_reply2 = str(text)
                        else:
                            word_to_reply2 = str(text2) 
                    else:
                        word_to_reply2 = str(text2)
                    
                    print(word_to_reply2)
                    word_to_reply1 = '{} '.format(disname) + 'ค้นข้อมูล ' + text_from_user

                    text_to_reply1 = TextSendMessage(text = word_to_reply1)
                    text_to_reply2 = TextSendMessage(text = word_to_reply2)
                    line_bot_api.reply_message(
                            event.reply_token,
                            messages=[text_to_reply2]
                        )
                    
            for symbol in symbols:
                stock(symbol).ticket()
    except:
        text_list = [
            '{} ไม่มีในฐานข้อมูล {} ลองใหม่อีกครั้ง'.format(text_from_user,disname),
            '{} พิมพ์หุ้น {} ไม่ถูกต้อง กรุณาตรวจสอบใหม่'.format(disname, text_from_user),

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
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)