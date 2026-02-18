from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    print("=== WEBHOOK RECEIVED ===")
    print(json.dumps(body, indent=2, ensure_ascii=False))
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
