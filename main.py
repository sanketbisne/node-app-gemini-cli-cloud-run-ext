from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse, HTMLResponse
from google.cloud import firestore
import os
import asyncio
import json
from datetime import datetime

app = FastAPI()
db = firestore.Client()
messages_ref = db.collection('chat_messages')

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat App</title>
            <style>
                body { font-family: sans-serif; margin: 20px; }
                #messages { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: scroll; margin-bottom: 10px; }
                .message { margin-bottom: 5px; }
                .timestamp { font-size: 0.8em; color: #888; margin-left: 10px; }
            </style>
        </head>
        <body>
            <h1>Real-time Chat</h1>
            <div id="messages"></div>
            <input type="text" id="messageInput" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>

            <script>
                const messageInput = document.getElementById('messageInput');
                const messagesDiv = document.getElementById('messages');

                // SSE connection
                const eventSource = new EventSource('/stream');
                eventSource.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    const messageElement = document.createElement('div');
                    messageElement.className = 'message';
                    messageElement.innerHTML = `<strong>${data.user || 'Anonymous'}:</strong> ${data.text} <span class="timestamp">${new Date(data.timestamp._seconds * 1000).toLocaleTimeString()}</span>`;
                    messagesDiv.appendChild(messageElement);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                };

                async function sendMessage() {
                    const text = messageInput.value;
                    if (text.trim() === '') return;

                    await fetch('/send_message', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ user: 'Anonymous', text: text }) // You can add user authentication here
                    });
                    messageInput.value = '';
                }
            </script>
        </body>
    </html>
    """

@app.post("/send_message")
async def send_message(message: dict):
    message['timestamp'] = datetime.now()
    await messages_ref.add(message)
    return {"status": "Message sent"}

@app.get("/stream")
async def sse_stream(request: Request):
    async def event_generator():
        # Send existing messages first
        for doc in messages_ref.order_by('timestamp').stream():
            yield f"data: {json.dumps(doc.to_dict())}\n\n"
            await asyncio.sleep(0.01) # Small delay to allow client to process

        # Listen for new messages
        messages_queue = asyncio.Queue()

        # Firestore on_snapshot callback
        def on_snapshot(col_snapshot, changes, read_time):
            for change in changes:
                if change.type.name == 'ADDED':
                    messages_queue.put_nowait(change.document.to_dict())

        # Start listening for changes
        col_watch = messages_ref.order_by('timestamp').on_snapshot(on_snapshot)

        try:
            while True:
                if await request.is_disconnected():
                    break
                message = await messages_queue.get()
                yield f"data: {json.dumps(message)}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            col_watch.unsubscribe() # Clean up the listener

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)