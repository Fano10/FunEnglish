import yaml
from flask import Flask, jsonify
import requests

app = Flask(__name__)

with open("keys.yaml" , "r") as file:
    keys = yaml.safe_load(file)

api_key = keys["api_key"]
theme = "job"
wordType = "verb"

@app.route('/vocabulary', methods=['POST'])
def get_newVocabulary():
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
            "content": "You are a great English teacher. The person attending your class is an A2 level student and wants to reach B2 level. Your goal is to provide him with a new word and its definition according to the theme chosen by the student and the nature of the word."
        },
        {
            "role": "user",
            "content": "Theme: job, nature: word"
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_new_word",
                "description": "Provides a new English word and its definition based on a theme and word nature",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "word": {
                            "type": "string",
                            "description": "The new English word"
                        },
                        "definition": {
                            "type": "string",
                            "description": "The definition of the word"
                        }
                    },
                    "required": ["word", "definition"]
                }
            }
        }
    ]
}


    response = requests.post(url, headers= headers, json= body)

    print (response)
    if response.status_code == 200:
        return response.json()
    else:
        return "Not okay"
    
if __name__ == '__main__':
    app.run()