import json
import requests

def ReplyMessage(Reply_token, TextMessage, Line_Access_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Access_Token) 
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        },{
            "type":"text",
            "text":'ท่านสามารถใช้งานโดยการพิมพ์ประโยคที่ต้องการค้นหาค่ะ'
        }]
    }
    
    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 'OK'

def PushMessage(userid, TextMessage, Line_Access_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/push'

    Authorization = 'Bearer {}'.format(Line_Access_Token) 
    print(Authorization)
    
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "to": userid,
        "messages":[
            {
                "type":"text",
                "text":TextMessage
            },
            {
                "type":"text",
                "text":"Hello"
            }
        ]
    }

    data = json.dumps(data) ## dump dict >> Json Object

    r = requests.post(LINE_API, headers=headers, data=data)
    print(r) 
    return 'OK'

def SetMessage_Object(Message_data,Quick_Reply = None):
    file_data = {"replyToken":'', "messages": []}

    if type(Message_data) is list:
        for message in Message_data:
            file_data['messages'].append(message)
    else :
        file_data['messages'].append(Message_data)
        
    return file_data

def reply_msg(reply_token,data,bot_access_key):
    
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(bot_access_key)

    headers = {'Content-Type': 'application/json; charset=UTF-8',
  'Authorization': Authorization}

    data['replyToken'] = reply_token
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data) 
    print(r.content)
    return r

    

