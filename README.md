# Cloud Run MCP Server

## Code that can be deployed

Only web servers can be deployed using this MCP server.
The code needs to listen for HTTP reqeusts on the port defined by the $PORT environment variable or 8080.

### Supported languages

- If the code is in Node.js, Python, Go, Java, .NET, PHP, Ruby, a Dockerfile is not needed.
- If the code is in another language, or has any custom dependency needs, a Dockerfile is needed.

### Static-only apps

To deploy static-only applications, create a Dockerfile that serves these static files. For example using `nginx`:

`Dockerfile`

```
FROM nginx:stable

COPY ./static /var/www
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
```

`nginx.conf`:

```
server {
    listen 8080;
    server_name _;

    root /var/www/;
    index index.html;

    # Force all paths to load either itself (js files) or go through index.html.
    location / {
        try_files $uri /index.html;
    }
}
```

## Google Cloud pre-requisites

The user must have an existing Google Cloud account with billing set up, and ideally an existing Google Cloud project.

If deployment fails because of an access or IAM error, it is likely that the user doesn't have Google Cloud credentials on the local machine.
The user must follow these steps:

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) and authenticate with their Google account.

2. Set up application credentials using the command:
   ```bash
   gcloud auth application-default login
   ```

## How to use the Gemini CLI Cloud Run MCP Extension

The Gemini CLI Cloud Run MCP Extension allows you to deploy applications to Google Cloud Run by interacting with the Gemini CLI agent. Here are some examples of how you can instruct the agent:

- **Deploying a local folder:** "Deploy the folder at `/path/to/my/app` to Cloud Run."
- **Deploying file contents:** "Deploy the Node.js application in the current directory to Cloud Run."
- **Deploying a container image:** "Deploy the container image `gcr.io/cloudrun/hello` to Cloud Run."
- **Listing services:** "List all Cloud Run services in project `my-project`."
- **Getting service details:** "Get details for the `my-service` service in project `my-project`."
- **Getting service logs:** "Get logs for the `my-service` service in project `my-project`."

## Simple Real-time Chat Application (In-memory)

This repository now contains a FastAPI application that demonstrates a simple real-time chat application using an in-memory message list and Server-Sent Events (SSE).

### How it works:
-   The root endpoint (`/`) serves an HTML page with a simple chat interface.
-   The `/send_message` endpoint accepts POST requests with chat messages and stores them in an in-memory list.
-   The `/stream` (SSE) endpoint streams existing chat messages from the in-memory list and then listens for new messages in real-time, pushing them to connected clients.
-   **Note:** Messages are stored only in memory and will be lost if the server restarts.

### How to use the Chat Application:

1.  **Deploy the application:** Deploy the application to Cloud Run.
2.  **Open in browser:** Access the deployed service URL (e.g., `https://sanket-mcp-cloud-run-jeqyasc2za-ew.a.run.app`).
3.  **Send messages:** Type a message in the input field and click "Send". Messages will appear in real-time for all connected clients.

### Deployment with Procfile

For Python applications, Cloud Run can use a `Procfile` to specify the command to run your application. This ensures that the web server (Uvicorn in this case) starts correctly and listens on the port expected by Cloud Run.

The `Procfile` in this repository contains:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```
This command tells Cloud Run to run the `app` object from `main.py` using Uvicorn, binding it to all network interfaces (`0.0.0.0`) and using the port specified by the `$PORT` environment variable.
