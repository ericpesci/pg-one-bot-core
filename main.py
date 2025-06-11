from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def root(request: Request):
    data = await request.json()
    print("MENSAJE RECIBIDO:", data)

    # Extracción del texto del mensaje (adapta si la estructura cambia)
    try:
        # SendPulse a veces lo manda como lista, tomamos el primer elemento
        evento = data[0] if isinstance(data, list) else data
        texto = evento['message']['channel_data']['message']['text']
        # Usuario: si lo tenés como variable o lo querés armar de Telegram
        usuario = evento['contact'].get('username') or evento['contact'].get('name') or 'Usuario'
    except Exception as e:
        texto = None
        usuario = None
        print(f"Error parseando mensaje: {e}")

    print(f"Mensaje de {usuario}: {texto}")

    return {"msg": f"PG-One recibió tu mensaje, {usuario}!", "texto": texto}
