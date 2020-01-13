richdata = {
  "size": {
    "width": 2500,
    "height": 843
  },
  "selected": True,
  "name": "Rich Menu 1",
  "chatBarText": "Menu",
  "areas": [
    {
      "bounds": {
        "x": 13,
        "y": 17,
        "width": 805,
        "height": 805
      },
      "action": {
        "type": "message",
        "text": "IQXUSTB"
      }
    },
    {
      "bounds": {
        "x": 847,
        "y": 8,
        "width": 801,
        "height": 818
      },
      "action": {
        "type": "message",
        "text": "IQXGL"
      }
    },
    {
      "bounds": {
        "x": 1674,
        "y": 13,
        "width": 813,
        "height": 818
      },
      "action": {
        "type": "message",
        "text": "IQXWTI"
      }
    }
  ]
}

from config import line_secret, line_access_token

import json

import requests



def RegisRich(Rich_json,channel_access_token):

    url = 'https://api.line.me/v2/bot/richmenu'

    Rich_json = json.dumps(Rich_json)

    Authorization = 'Bearer {}'.format(line_access_token)


    headers = {'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': Authorization}

    response = requests.post(url,headers = headers , data = Rich_json)

    print(str(response.json()['richMenuId']))

    return str(response.json()['richMenuId'])

def CreateRichMenu(ImageFilePath,Rich_json,channel_access_token):


    richId = RegisRich(Rich_json = Rich_json,channel_access_token = line_access_token)

    url = ' https://api.line.me/v2/bot/richmenu/{}/content'.format(richId)

    Authorization = 'Bearer {}'.format(line_access_token)

    headers = {'Content-Type': 'image/jpeg',
    'Authorization': Authorization}

    img = open(ImageFilePath,'rb').read()

    response = requests.post(url,headers = headers , data = img)

    print(response.json())



CreateRichMenu(ImageFilePath='Resource/richmenu.jpg',Rich_json=richdata,channel_access_token=line_access_token)