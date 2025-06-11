@app.post("/")
async def root(request: Request):
    data = await request.json()
    print("MENSAJE RECIBIDO:", data)

    # Intenta obtener el texto del mensaje de distintas formas
    texto = None
    usuario = None
    try:
        evento = data[0] if isinstance(data, list) else data
        # Casos posibles: Telegram a veces envía varias formas
        if 'message' in evento and 'channel_data' in evento['message'] and 'message' in evento['message']['channel_data']:
            texto = evento['message']['channel_data']['message'].get('text')
        elif 'message' in evento and 'text' in evento['message']:
            texto = evento['message']['text']
        elif 'text' in evento:
            texto = evento.get('text')
        else:
            print('No se encontró texto en el mensaje.')
        
        # Usuario (de la forma que venga)
        if 'contact' in evento:
            usuario = evento['contact'].get('username') or evento['contact'].get('name') or 'Usuario'
        else:
            usuario = 'Usuario'
    except Exception as e:
        print(f"Error parseando mensaje: {e}")

    print(f"Texto detectado: {texto}, usuario: {usuario}")

    prompt = f"Sos PG-One, un bot de cocina argentino. Respondéle a {usuario} de manera cálida, breve y con humor:\n\nUsuario: {texto}\nPG-One:"

    respuesta = "Ups, no pude generar respuesta..."
    if texto:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
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
