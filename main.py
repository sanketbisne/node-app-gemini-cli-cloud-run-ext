from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse, HTMLResponse
import os
import asyncio
import json
from datetime import datetime

app = FastAPI()

# In-memory list to store messages
messages = []
message_queue = asyncio.Queue()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat App</title>
            <style>
                body { font-family: sans-serif; margin: 20px; }
                #messages { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: scroll; margin-bottom: 10px; }\n                .message { margin-bottom: 5px; }\n                .timestamp { font-size: 0.8em; color: #888; margin-left: 10px; }\n            </style>\n        </head>\n        <body>\n            <h1>Real-time Chat (In-memory)</h1>\n            <div id="messages"></div>\n            <input type="text" id="messageInput" placeholder="Type your message...">\n            <button onclick="sendMessage()">Send</button>\n
            <script>\n                const messageInput = document.getElementById('messageInput');\n                const messagesDiv = document.getElementById('messages');\n
                // SSE connection\n                const eventSource = new EventSource('/stream');\n                eventSource.onmessage = function(event) {\n                    const data = JSON.parse(event.data);\n                    const messageElement = document.createElement('div');\n                    messageElement.className = 'message';\n                    messageElement.innerHTML = `<strong>${data.user || 'Anonymous'}:</strong> ${data.text} <span class=\"timestamp\">${new Date(data.timestamp).toLocaleTimeString()}</span>`;\n                    messagesDiv.appendChild(messageElement);\n                    messagesDiv.scrollTop = messagesDiv.scrollHeight;\n                };\n
                async function sendMessage() {\n                    const text = messageInput.value;\n                    if (text.trim() === '') return;\n
                    await fetch('/send_message', {\n                        method: 'POST',
                        headers: {\n                            'Content-Type': 'application/json'\n                        },\n                        body: JSON.stringify({ user: 'Anonymous', text: text, timestamp: new Date().toISOString() }) // You can add user authentication here\n                    });\n                    messageInput.value = '';\n                }\n            </script>\n        </body>\n    </html>\n    """

@app.post("/send_message")\nasync def send_message(message: dict):\n    messages.append(message)\n    await message_queue.put(message)\n    return {"status": "Message sent"}\n
@app.get("/stream")\nasync def sse_stream(request: Request):\n    async def event_generator():\n        # Send existing messages first\n        for msg in messages:\n            yield f"data: {json.dumps(msg)}\n\n"\n            await asyncio.sleep(0.01) # Small delay to allow client to process\n
        # Listen for new messages\n        while True:\n            if await request.is_disconnected():\n                break\n            message = await message_queue.get()\n            yield f"data: {json.dumps(message)}\n\n"\n
    return StreamingResponse(event_generator(), media_type="text/event-stream")\n
if __name__ == "__main__":\n    import uvicorn\n    port = int(os.environ.get("PORT", 8080))\n    uvicorn.run(app, host="0.0.0.0", port=port)