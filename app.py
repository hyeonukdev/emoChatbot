from flask import Flask, render_template, request
import json, requests

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


def request_dialogflow_api(userText):
    MY_AUTH_TOKEN = "Bearer ya29.a0ARrdaM9SjP3ygOmXYBwxOGV9DiyzkzX61lDupARro59HoqEKXL5JIvkHv1lO4IVTC5TYAu8q4QRwM5n5SS-WLANX9z7CiLk8DbcDdFMWcSJt7zz8RcJggHi5gNWcBfjCIsBrtAsUoXNO3ELg1anMGvRRhktuIpo1G1zGonaMYBKmGX1jq1Kao_YKfHrrpPFAjsmlFx5tFTfHReuHceXu5kToAHJMgLUy6N0IbDdEI0whAjI"

    data_header = {
        'Authorization': MY_AUTH_TOKEN,
        'Content-Type': 'application/json; charset=utf-8'
    }

    data = {
        "queryInput": {
            "text": {
                "text": userText,
                "languageCode": "ko"
            }
        }
    }

    dialogflow_url = 'https://dialogflow.clients6.google.com/v2beta1/projects/emochatbot-aupx/locations/global/agent/sessions/704c9faa-a2ba-4f3b-e9c6-a394311753f2:detectIntent'
    res = requests.post(dialogflow_url, data=json.dumps(data), headers=data_header)

    print(f"res : {res}")
    if res.status_code != requests.codes.ok:
        return '오류가 발생했습니다.'
    else:
        data_receive = res.json()
        print(f"data_receive : {data_receive}")

        if data_receive['queryResult']['fulfillmentText'] != '':
            response = data_receive['queryResult']['fulfillmentText']
            print(f"response : {response}")
            return response
        else:
            print(f"data_receive : {data_receive}")
            return data_receive



@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(request_dialogflow_api(userText))
    # return 'test'


if __name__ == "__main__":
    app.run(debug=True)