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

## Real-time Chat Application with Firestore and SSE

This repository now contains a FastAPI application that demonstrates a real-time chat application using Google Cloud Firestore and Server-Sent Events (SSE).

### How it works:
-   The root endpoint (`/`) serves an HTML page with a simple chat interface.
-   The `/send_message` endpoint accepts POST requests with chat messages and stores them in a Firestore collection named `chat_messages`.
-   The `/stream` (SSE) endpoint streams existing chat messages from Firestore and then listens for new messages in real-time, pushing them to connected clients.

### Google Cloud Firestore Setup:

To make this application work, you need to enable the Firestore API and grant appropriate permissions to your Cloud Run service account:

1.  **Enable Firestore API:**
    Visit the Google Cloud Console and enable the Firestore API for your project:
    `https://console.cloud.google.com/apis/library/firestore.googleapis.com?project=mcp-gcp-project`

2.  **Grant IAM Permissions:**
    Your Cloud Run service account (typically `PROJECT_NUMBER-compute@developer.gserviceaccount.com`) needs the "Cloud Datastore User" role (which includes Firestore permissions) or a custom role with specific Firestore permissions.
    You can grant this role via the IAM & Admin section in the Google Cloud Console:
    `https://console.cloud.google.com/iam-admin/iam?project=mcp-gcp-project`

### How to use the Chat Application:

1.  **Deploy the application:** Once the Firestore API is enabled and permissions are set, deploy the application to Cloud Run.
2.  **Open in browser:** Access the deployed service URL (e.g., `https://sanket-mcp-cloud-run-jeqyasc2za-ew.a.run.app`).
3.  **Send messages:** Type a message in the input field and click "Send". Messages will appear in real-time for all connected clients.
