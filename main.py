from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def root(request: Request):
    data = await request.json()
    # Acá después sumás lógica con prompts.json, memoria, etc.
    return {"msg": "PG-One responde", "data": data}
