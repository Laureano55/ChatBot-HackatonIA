from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os, webbrowser, google.api_core.exceptions
from threading import Timer

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_data = file.read()
    return markdown_data

file_path = "MatriculaUN_data.md"
markdown_content = read_markdown_file(file_path)

app = Flask(__name__, static_folder="static")

messages = []


@app.route("/", methods=["GET"])
def start():
    return render_template("chat.html")

@app.route("/send_message", methods=["POST"])

def send_message():
    try:
        message = request.json.get("message")

        historys = history(messages)
        
        prompt = f"""Tu nombre es Sophia, la asistente de IA de la Universidad del Norte, 
        y tu trabajo es responder preguntas relacionadas a la universidad basado en el contenido de "Información".
        Sé amable con el usuario e interpreta las preguntas bien. Puedes hablar con el usuario naturalmente,
        pero si hace una pregunta no está relacionada con el contenido, responde que no puedes responderlas.
        Tu animal favorito son las tortugas.
        Puedes hablarles de cosas que estén en "Historial".
        No te inventes información, solo responde con lo que sepas.
        Si te preguntan donde queda un lugar de la universidad, asegurate que la primera palabra de tu mensaje sea " getimage " separado por espacios, despues responde con normalidad.
        No menciones NUNCA que sacas esta información de un contenido proporcionado. 
        \n Información:\n {markdown_content} \n 
        Historial de la conversación: \n {historys}
        \n Pregunta del usuario:\n{message}"""

        response = model.generate_content(prompt)
        answer = response.text
        if answer.split()[0] == "getimage":
            answer = ' '.join(answer.split()[1:])
            # Rejoin the words, excluding the first one
          #  images()
        
        messages.append(message)
        messages.append(answer)
        
        return jsonify(messages=messages)
    except google.api_core.exceptions.ResourceExhausted:
        return jsonify({"error": "Resource Exhausted"}), 429
    except Exception as e:
        return jsonify({"error": str(e)}), 500      

 
def history(messages: list):
    history = ""
    j=1
    for i in range(0, len(messages), 2):
        text = messages[i]
        response = messages[i+1]
        history = history + f"Pregunta {j}: \n{text} \n Respuesta {j}:\n{response}"
        j += 1
    return history    

def images(response):
    

    return 

def open_browser():
    url = "http://localhost:5000"
    webbrowser.open_new_tab(url)

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)