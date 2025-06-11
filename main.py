from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def root(request: Request):
    data = await request.json()
    print("MENSAJE RECIBIDO:", data)   # Este print lo ves en los logs de Render
    return {"msg": "PG-One responde", "data": data}
