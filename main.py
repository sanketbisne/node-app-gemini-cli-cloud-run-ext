from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/mcp")
async def mcp_endpoint(data: dict):
    # This is where you would implement your Model Context Protocol logic
    # For now, it just echoes the received data
    return {"received_data": data, "status": "processed"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)