from fastapi import FastAPI, Body
import httpx

app = FastAPI()

@app.post("/webhook")
async def webhook(alert: dict = Body(...)):
    """
    Process alert JSON and forward it to /responses/add
    """
    print(alert)

    # --- Forward alert to another endpoint ---
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://127.0.0.1:8000/responses/add",
                json=alert,
                timeout=10.0
            )
            if response.status_code == 200:
                print("✅ Alert forwarded successfully")
            else:
                print(f"⚠ Failed to forward alert: {response.status_code} {response.text}")
        except Exception as e:
            print(f"❌ Error forwarding alert: {e}")

    return {"status": "received"}
