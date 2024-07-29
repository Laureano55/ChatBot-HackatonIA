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

college_places = {
    "Biblioteca Karl C. Parrish": 1,
    "Bloque A": 2,
    "Bloque Administrativo I": 3,
    "Bloque Administrativo II": 4,
    "Bloque B": 5,
    "Bloque C": 6,
    "Bloque D": 7,
    "Bloque E": 8,
    "Bloque F": 9,
    "Bloque G. Edificio Postgrados": 10,
    "Bloque I. Instituto de Idiomas": 11,
    "Bloque J": 12,
    "Bloque K. Edificio de Ingenierías": 13,
    "Bloque L. Edificio Julio Muvdi": 14,
    "Bloque M": 15,
    "Laboratorio de Arquitectura Tropical": 16,
    "Laboratorio de Energías Renovables": 17,
    "Bloque de Salud": 18,
    "Canchas Múltiples": 19,
    "Coliseo Cultural y Deportivo Los Fundadores": 20,
    "Parqueadero administrativo principal": 21,
    "Parqueadero Bloque C": 22,
    "Parqueadero Bloque J": 23,
    "Parqueadero canchas de futbol": 24,
    "Parqueadero Coliseo": 25,
    "Parqueadero Edificio Postgrados": 26,
    "Parqueadero 10": 27,
    "DuNord Café": 28,
    "DuNord Express": 29,
    "DuNord Graphique": 30,
    "DuNord Plaza": 31,
    "DuNord Terrasse": 32,
    "Iwanna Store": 33,
    "Km5": 34,
    "Le Salon": 35,
    "Restaurante 1966": 36
}

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

        if response.text.split()[0] == "getimage":

            images()

        messages.append(message)
        messages.append(response.text)
        
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