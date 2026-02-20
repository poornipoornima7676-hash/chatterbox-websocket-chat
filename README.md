
# Chatterbox – Real-time WebSocket Chat Application

Chatterbox is a full-stack real-time chat application built using FastAPI and WebSockets.
It enables instant communication between multiple users with persistent message storage, real-time presence tracking, and interactive UI features similar to modern messaging platforms.

The system demonstrates asynchronous communication, WebSocket-based broadcasting, token-based authentication, and database persistence.


## Project Overview

Chatterbox is designed to simulate a real-time collaborative chat environment where multiple authenticated users can communicate instantly.

Unlike traditional HTTP request-response systems, this application uses persistent WebSocket connections to enable low-latency, full-duplex communication between clients and the server.

The project focuses on:

* Real-time multi-user communication
* Online presence tracking
* Persistent chat history
* Interactive message management
* Delivery and read receipts


## Features

### Real-time Messaging

Messages are delivered instantly to all connected users using a WebSocket broadcast mechanism.

### Online Users Tracking

Active users are dynamically tracked using a connection manager and displayed in a live “Online” panel.

### Chat History Persistence

Messages are stored in SQLite and automatically loaded when a user joins the chat.

### Message Editing

Users can edit previously sent messages. Updated messages are reflected in real time for all participants.

### Message Deletion

Deleted messages are replaced with a placeholder (“This message was deleted”) to maintain conversation flow.

### Typing Indicators

Users can see when another participant is typing in real time.

### Read Receipts

Message status indicators show:

* ○ Delivered
* ● Seen

### Date-Based Message Grouping

Messages are automatically grouped under “Today” and “Yesterday” separators.

### Emoji Support

Built-in emoji picker for enhanced user interaction.

## Technical Stack

Backend

* FastAPI (asynchronous Python framework)
* WebSockets for real-time communication
* SQLite for relational database storage
* JWT / Token-based authentication

Frontend

* HTML5
* CSS3 (Flexbox layout, dark UI theme)
* Vanilla JavaScript (WebSocket API integration)

Communication Protocol

* WebSocket (ws://) for persistent full-duplex communication

## System Architecture

1. User logs in with a username.
2. Server generates an authentication token.
3. WebSocket connection is established using the token.
4. ConnectionManager stores active connections.
5. Messages are saved in SQLite.
6. Server broadcasts updates to all connected users.
7. Frontend dynamically renders updates without refresh.

## Project Structure

```
chatterbox/
│
├── server/
│   ├── main.py                 # WebSocket endpoint and routing logic
│   ├── database.py             # Database operations
│   ├── connection_manager.py   # Manages active WebSocket connections
│   ├── auth.py                 # Token generation and verification
│
├── static/
│   ├── index.html              # Frontend UI
│
├── requirements.txt
├── README.md
└── chat.db
```

## Database Schema

The application uses a SQLite database with a messages table containing:

* id (Primary Key)
* username
* message
* timestamp
* date
* edited flag

This ensures persistence and message continuity across sessions.

## How to Run the Project

### 1. Clone the Repository

```
git clone https://github.com/yourusername/chatterbox-websocket-chat.git
cd chatterbox-websocket-chat
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Run the Server

```
python -m uvicorn server.main:app --reload
```

### 4. Open in Browser

```
http://127.0.0.1:8000
```

## Challenges Solved

* Managing multiple concurrent WebSocket connections
* Synchronizing chat history for newly connected users
* Handling unexpected disconnections
* Preventing incorrect read receipt updates
* Ensuring database persistence without blocking real-time flow

## Future Enhancements

* Private one-to-one chat rooms
* File and image sharing
* PostgreSQL or Redis for high concurrency
* User accounts with password hashing
* Deployment on cloud platforms


## License

This project is licensed under the MIT License.
