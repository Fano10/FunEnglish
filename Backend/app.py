import yaml
from flask import Flask, jsonify, request
import json
import re
import requests

app = Flask(__name__)

with open("keys.yaml" , "r") as file:
    keys = yaml.safe_load(file)

api_key = keys["api_key"]
theme = "job"
wordType = "verb"

@app.route('/vocabulary', methods=['POST'])
def get_newVocabulary():

    if (request.headers.get('Content-Type') == 'application/json'):
        data = request.get_json()
        theme = data["theme"]
        nature = data["nature"]
    
    content = str("Theme: " +theme+ ", nature: " + nature+ ", word already know: promotion")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type" : "application/json",
        "Authorization": "Bearer " + api_key
    }
    body = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "system",
            "content": "You are an excellent English teacher. The person attending your class is an A2 level student and wants to reach B2 level. Your goal is to provide him with only a new word, its definition and an example based on the theme chosen by the student and the nature of the word. But be careful, the student will also provide you with words that he already knows, so it is important not to return these words. The return response must be strictly in JSON format no comment with the keys: word, definition and example"
        },
        {
            "role": "user",
            "content": content
        }
    ],
}


    response = requests.post(url, headers= headers, json= body)

    print (response)
    if response.status_code == 200:
        body = response.json()
        body_value = body["choices"][0]["message"]["content"]

        body_value = re.sub('^(```json)?','',body_value)
        body_value = re.sub('`+','',body_value)
        body_value_json = json.loads(body_value)
        print(body_value_json)
        return body_value_json
    else:
        return "Not okay"
    
if __name__ == '__main__':
    app.run(debug=True)