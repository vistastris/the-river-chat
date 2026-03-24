# the-river-chat
a minimalist, retro-terminal chat room application built with Python and Tkinter. designed with a dark-web aesthetic, it features local socket connections, terminal-based commands, and an autonomous system bot. inspired by the film "unfriended".

<img width="798" height="498" alt="login" src="https://github.com/user-attachments/assets/ef1a832d-6294-4e8c-84a2-303ce38f2ef2" />
<img width="798" height="501" alt="test" src="https://github.com/user-attachments/assets/5705e606-74b6-4963-94d6-748431af48e0" />

## Features

- **Custom Interface:** Borderless, draggable retro terminal UI.
- **The Watcher:** An autonomous background bot that occasionally connects to the network, drops cryptic messages, and disconnects.
- **Visual Decryption:** Send encrypted messages (`>crypt`) that decode visually with an animation upon clicking.
- **Admin Mode:** System administrator access to kick nodes or wipe the network (Password: `KRONOS`).
- **Terminal Commands:** Local chat logging, private whispering, and live network statistics.
- **Glitch Effects:** Screen shakes and UI color glitches triggered by system events.

## Installation & Usage

1. Clone the repository and navigate to the project directory.
2. Start the server script first:
    python server.py
3. Run the client script (you can run multiple instances to test):
    python client.py
4. Enter the security code when prompted:
    Abyssus abyssum invocat

Available Commands
>help : Display all available commands.

>clear : Clear your local chat screen.

>stats : View active nodes and total network traffic.

>log : Export the current chat history as a .md (Markdown) file.

>whisper [Name]: [Message] : Send a private message to a specific node.

>crypt [Message] : Broadcast a visually encrypted message to the network.

Admin Only:
>kick [Name] : Disconnect a user from the server.

>clearall : Force-clear the screens of all connected clients.
