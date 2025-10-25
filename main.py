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
    return """<!DOCTYPE html>
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
        <h1>Real-time Chat (In-memory)</h1>
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
                messageElement.innerHTML = `<strong>${data.user || 'Anonymous'}:</strong> ${data.text} <span class="timestamp">${new Date(data.timestamp).toLocaleTimeString()}</span>`;
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
                    body: JSON.stringify({ user: 'Anonymous', text: text, timestamp: new Date().toISOString() }) // You can add user authentication here
                });
                messageInput.value = '';
            }
        </script>
    </body>
</html>
"