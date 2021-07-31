from flask import Flask, render_template, request
import json, requests

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


def request_dialogflow_api(userText):
    MY_AUTH_TOKEN = "Bearer ya29.a0ARrdaM94yZLF8yYVTkJ9yyuCjPT3F9E_iESNujfv2CFnpBuWj2ZV4LLqEcQFg_aK_gSxQ6oznp3boTpLFsMGfaMdNqSEhGVwCxARACoMJ4JWhxY9tbppkcNhgsNOxylzLC4DxHR6ZMniKTzewMqEx5W4_1O1rs1glIhhzPspUc1cd9JxoIW6gZmjKWcQ9-QCnq9Bf6gjKwR_JH6BBEeZ4BI3fa3JdWWTFGe3BfzPSkcJYks"

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

    if res.status_code != requests.codes.ok:
        return '오류가 발생했습니다.'
    else:
        data_receive = res.json()
        print(f"data_receive : {data_receive}")
        queryResult = data_receive['queryResult']
        fulfillmentText = queryResult.get('fulfillmentText')

        if fulfillmentText:
            # 인텐트에 데한 리스폰스
            response = fulfillmentText
        else:
            # '그래' 답을 했을 경우
            fulfillmentMessages = queryResult.get('fulfillmentMessages')
            # print(f"fulfillmentMessages: {fulfillmentMessages}")
            richContent = fulfillmentMessages[0]['payload']['richContent'][0][0]
            # print(f"richContent: {richContent}")
            text = richContent.get('text')
            link = richContent.get('link')
            msg = text + '\n' + link
            response = msg

        # print(f"response : {response}")
        return response


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(request_dialogflow_api(userText))


if __name__ == "__main__":
    app.run(debug=True)