from fastapi import FastAPI, Request
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # No pongas la key acá, solo el nombre de la variable

app = FastAPI()

@app.post("/")
async def root(request: Request):
    data = await request.json()
    print("MENSAJE RECIBIDO:", data)  # Esto lo vas a ver en los logs de Render

    try:
        evento = data[0] if isinstance(data, list) else data
        texto = evento['message']['channel_data']['message']['text']
        usuario = evento['contact'].get('username') or evento['contact'].get('name') or 'Usuario'
    except Exception as e:
        texto = None
        usuario = None
        print(f"Error parseando mensaje: {e}")

    prompt = f"Sos PG-One, un bot de cocina argentino. Respondéle a {usuario} de manera cálida, breve y con humor:\n\nUsuario: {texto}\nPG-One:"

    respuesta = "Ups, no pude generar respuesta..."
    if texto:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Si tenés GPT-4 lo podés cambiar
                messages=[{"role": "system", "content": prompt}]
            )
            respuesta = completion.choices[0].message.content.strip()
        except Exception as e:
            print("Error con OpenAI:", e)
    
    print(f"Respuesta IA: {respuesta}")

    return {
        "messages": [
            {
                "text": respuesta
            }
        ]
    }
