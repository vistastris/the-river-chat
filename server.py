import socket
import threading
import time
import random

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            if isinstance(message, str):
                client.send(message.encode('utf-8'))
            else:
                client.send(message)
        except:
            pass

def broadcast_user_list():
    users_str = "USERLIST:" + ",".join(nicknames)
    broadcast(users_str.encode('utf-8'))

# --- THE WATCHER (HAYALET İSTEMCİ BOTU) ---
def watcher_bot():
    time.sleep(10) 
    bot_names = ["THE WATCHER", "UNKNOWN_NODE", "SYS_ADMIN"]
    creepy_messages = [
        "01010111 01000001 01001011 01000101",
        "I CAN SEE YOU...",
        "THE RIVER IS OVERFLOWING.",
        "COORDINATES LOCKED: 37°14'06\"N 115°48'40\"W",
        "WHO IS KNOCKING?",
        "NULL_POINTER_EXCEPTION: SOUL NOT FOUND."
    ]
    
    while True:
        time.sleep(random.randint(300, 600)) 
        bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            bot.connect((HOST, PORT))
            bot.recv(1024) 
            bot_name = random.choice(bot_names)
            bot.send(bot_name.encode('utf-8'))
            time.sleep(random.randint(5, 12))
            msg = random.choice(creepy_messages)
            bot.send(f"<{bot_name}>  {msg}".encode('utf-8'))
            time.sleep(random.randint(3, 6))
            bot.close() 
        except:
            pass

def handle(client):
    while True:
        try:
            raw_message = client.recv(1024)
            if not raw_message:
                raise Exception("Bağlantı koptu!") 
                
            message = raw_message.decode('utf-8')
            
            # --- ÖZEL PROTOKOLLER ---
            if message.startswith("WHISPER|"):
                parts = message.split("|", 3)
                if len(parts) == 4:
                    target_name = parts[1]
                    sender_name = parts[2]
                    msg_content = parts[3]
                    if target_name in nicknames:
                        target_index = nicknames.index(target_name)
                        clients[target_index].send(f"WHISPER_RECV|{sender_name}|{msg_content}".encode('utf-8'))
                        client.send(f"WHISPER_ECHO|{target_name}|{msg_content}".encode('utf-8'))
                    else:
                        client.send(f"<SİSTEM> HATA: {target_name} isimli düğüm bulunamadı.\n".encode('utf-8'))
            
            # ŞİFRELİ MESAJ AĞI
            elif message.startswith("CRYPT|"):
                broadcast(message.encode('utf-8'))
            
            # ADMİN: KULLANICIYI AT
            elif message.startswith("KICK|"):
                target = message.split("|")[1]
                if target in nicknames:
                    idx = nicknames.index(target)
                    target_client = clients[idx]
                    target_client.send("KICKED_BY_ADMIN".encode('utf-8'))
                    target_client.close() # Bağlantıyı kopar
                    clients.remove(target_client)
                    nicknames.remove(target)
                    broadcast(f"<SİSTEM> {target} SİSTEMDEN SİLİNDİ (ADMİN MÜDAHALESİ).\n".encode('utf-8'))
                    broadcast_user_list()
            
            # ADMİN: HERKESİN EKRANINI TEMİZLE
            elif message == "CLEARALL":
                broadcast("CLEARALL_CMD".encode('utf-8'))
                
            else:
                broadcast(raw_message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'<SİSTEM> {nickname} the river\'dan ayrıldı.\n'.encode('utf-8'))
                nicknames.remove(nickname)
                broadcast_user_list()
            break

def receive():
    print("[-] Sunucu dinlemede... The River akıyor.")
    watcher_thread = threading.Thread(target=watcher_bot, daemon=True)
    watcher_thread.start()
    
    while True:
        client, address = server.accept()
        try:
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            if nickname:
                nicknames.append(nickname)
                clients.append(client)
                broadcast(f"<SİSTEM> {nickname} the circle'a katıldı.\n".encode('utf-8'))
                broadcast_user_list() 
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
        except:
            print(f"[-] {str(address)} giriş yapamadan ayrıldı.")
            client.close()

receive()