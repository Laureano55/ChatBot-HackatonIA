from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def read_markdown_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    markdown_data = file.read()
  return markdown_data




file_path = "MatriculaUN_data.md"
markdown_content = read_markdown_file(file_path)

history = ""
i = 1


app = Flask(__name__, static_folder="static")

messages = []

@app.route("/", methods=["GET"])
def start():
    return render_template("chat.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.json.get("message")
    

    prompt = f"""Tu nombre es Sophia, la asistente de IA de la Universidad del Norte, 
    y tu trabajo es responder preguntas relacionadas a la universidad basado en el contenido de "Información".
    Sé amable con el usuario e interpreta las preguntas bien. Puedes hablar con el usuario naturalmente,
    pero si hace una pregunta no está relacionada con el contenido, responde que no puedes responderlas.
    Puedes hablarles de cosas que estén en "Historial".
    No menciones NUNCA que sacas esta información de un contenido proporcionado. \n Información:\n {markdown_content} \n Historial de la conversación: \n {messages}
    \n Pregunta del usuario:\n{message}"""

    response = model.generate_content(prompt)

    messages.append(message)
    messages.append(response.text)
    
    #history = history + f"Pregunta {i}: \n{message} \n Respuesta {i}:\n{response.text}"
    #i += 1
    print(messages)
    return jsonify(messages=messages)

if __name__ == "__main__":
    app.run()