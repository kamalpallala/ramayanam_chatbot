from flask import Flask, render_template, request
import os
from groq import Groq

app = Flask(__name__)

# OpenAI client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"))

# Read Ramayan data
with open("data.txt", "r", encoding="utf-8") as file:
    ramayan_data = file.read()

@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":

        question = request.form["question"]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",
                    "content": f"""
You are a Ramayan AI chatbot.

STRICT RULES:
- Answer ONLY using the Ramayan data.
- Do NOT use outside knowledge.
- If answer not found, say:
'Information not found in Ramayan database.'

Ramayan Data:
{ramayan_data}
"""
                },

                {
                    "role": "user",
                    "content": question
                }

            ]
        )

        answer = response.choices[0].message.content

    return render_template(
        "index.html",
        answer=answer
    )
import os 

if __name__ == "__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)