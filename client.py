import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
import sys
import random
import winsound
import datetime

HOST = '127.0.0.1'
PORT = 55555

root = tk.Tk()
root.withdraw() 

# --- GİRİŞ VE ADMİN KONTROLÜ ---
is_admin = False
secret_code = simpledialog.askstring("GÜVENLİK PROTOKOLÜ", "RECITE THE CODE:", parent=root)

if secret_code == "KRONOS":
    is_admin = True
    messagebox.showinfo("YETKİ ONAYI", "SİSTEM YÖNETİCİSİ OLARAK GİRİŞ YAPILDI. TAM ERİŞİM SAĞLANDI.")
elif secret_code != "Abyssus abyssum invocat":
    messagebox.showerror("ERİŞİM REDDEDİLDİ", "YANLIŞ KOD. THE RIVER SENİ KABUL ETMEDİ.")
    sys.exit()

nickname = simpledialog.askstring("KİMLİK", "Kod adınızı girin (Örn: Charon IV):", parent=root)
if not nickname:
    nickname = "Bilinmeyen"

if is_admin:
    nickname = f"★ {nickname}" 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except:
    messagebox.showerror("BAĞLANTI HATASI", "Sunucu kapalı veya ulaşılamıyor.")
    sys.exit()

message_count = 0
current_active_users = []

def play_sound(freq, duration):
    threading.Thread(target=winsound.Beep, args=(freq, duration), daemon=True).start()

root.deiconify() 
root.overrideredirect(True) 
root.geometry("800x500")
root.configure(bg="#0000AA") 
root.attributes("-topmost", True)

terminal_font = ("Courier", 12, "bold")

def start_move(event):
    root.x = event.x; root.y = event.y
def stop_move(event):
    root.x = None; root.y = None
def do_move(event):
    x = root.winfo_x() + (event.x - root.x)
    y = root.winfo_y() + (event.y - root.y)
    root.geometry(f"+{x}+{y}")
def close_app():
    try: client.close()
    except: pass
    root.destroy(); sys.exit()

title_bar = tk.Frame(root, bg="#0000AA", relief="raised", bd=2)
title_bar.pack(fill=tk.X, side=tk.TOP)
title_bar.bind("<ButtonPress-1>", start_move)
title_bar.bind("<ButtonRelease-1>", stop_move)
title_bar.bind("<B1-Motion>", do_move)

title_label = tk.Label(title_bar, text=f"X-~>< the river <3> - {nickname}", bg="#0000AA", fg="white", font=terminal_font)
title_label.pack(side=tk.LEFT, padx=5)

close_btn = tk.Button(title_bar, text="[X]", bg="#0000AA", fg="white", font=terminal_font, bd=0, command=close_app, activebackground="red")
close_btn.pack(side=tk.RIGHT, padx=5)

anim_frame = tk.Frame(root, bg="black")
anim_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

scary_label = tk.Label(anim_frame, text="", bg="black", fg="#8B0000", font=("Courier", 18, "bold"))
scary_label.pack(expand=True)

main_container = tk.Frame(root, bg="black")

anim_steps = ["AĞA BAĞLANILIYOR...", "KİMLİK DOĞRULANIYOR...", "R'LYEH DÜĞÜMLERİ YÖNLENDİRİLİYOR...", f"THE RIVER'A HOŞ GELDİN, {nickname.upper()}."]

def run_animation(step=0):
    if step < len(anim_steps):
        scary_label.config(text=anim_steps[step])
        scary_label.config(fg=random.choice(["#FF0000", "#8B0000", "#550000"]))
        play_sound(300, 150) 
        root.after(random.randint(800, 1200), run_animation, step + 1)
    else:
        anim_frame.destroy()
        main_container.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        play_sound(1000, 300)
run_animation()

users_frame = tk.Frame(main_container, bg="black", width=200, highlightbackground="blue", highlightthickness=2)
users_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

tk.Label(users_frame, text="Active Users", bg="blue", fg="white", font=terminal_font).pack(fill=tk.X)
users_list_frame = tk.Frame(users_frame, bg="black")
users_list_frame.pack(fill=tk.BOTH, expand=True)

chat_frame = tk.Frame(main_container, bg="black")
chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

input_frame = tk.Frame(chat_frame, bg="black")
input_frame.pack(side=tk.BOTTOM, fill=tk.X)

tk.Label(input_frame, text=f"{nickname}-->", bg="black", fg="#FF00FF", font=terminal_font).pack(side=tk.LEFT)
entry_field = tk.Entry(input_frame, bg="black", fg="#FF00FF", font=terminal_font, insertbackground="#FF00FF", borderwidth=0)
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True)

tk.Label(chat_frame, text="THE CIRCLE", bg="blue", fg="white", font=terminal_font).pack(side=tk.TOP, fill=tk.X)

chat_box = tk.Text(chat_frame, bg="black", fg="#00FF00", font=terminal_font, state=tk.DISABLED, wrap=tk.WORD, borderwidth=0)
chat_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)

chat_box.tag_config("me", foreground="#FF00FF") 
chat_box.tag_config("other", foreground="#00FF00") 
chat_box.tag_config("system", foreground="red") 
chat_box.tag_config("whisper", foreground="#FFFF00") 
chat_box.tag_config("whisper_echo", foreground="#808000") 
chat_box.tag_config("watcher", foreground="#FF0000") 

# YUKARI KAYMA (AUTO-SCROLL) ÇÖZÜMÜ
def scroll_to_bottom():
    chat_box.see(tk.END)

def decode_text(tag_name, real_text):
    chat_box.tag_unbind(tag_name, "<Button-1>") 
    chat_box.tag_config(tag_name, underline=False, foreground="#00FA9A") 
    
    def anim_step(current_len):
        if current_len <= len(real_text):
            chat_box.config(state=tk.NORMAL)
            ranges = chat_box.tag_ranges(tag_name)
            if ranges:
                start, end = ranges[0], ranges[1]
                gibberish = "".join(random.choice("!@#$%^&*<>X?") for _ in range(len(real_text) - current_len))
                display = real_text[:current_len] + gibberish
                
                chat_box.delete(start, end)
                chat_box.insert(start, display, tag_name)
                
            chat_box.config(state=tk.DISABLED)
            play_sound(800 + current_len*5, 10) 
            root.after(30, anim_step, current_len + 1)
            
    anim_step(0)

def prepare_whisper(target_user):
    if target_user != nickname:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, f">whisper {target_user}: ")
        entry_field.focus()

def trigger_glitch():
    try: orig_x = root.winfo_x(); orig_y = root.winfo_y()
    except: return 
    def shake(count):
        if count > 0:
            dx = random.randint(-15, 15); dy = random.randint(-15, 15)
            root.geometry(f"+{orig_x + dx}+{orig_y + dy}")
            chat_box.config(bg=random.choice(["black", "red", "darkgreen"]), fg=random.choice(["black", "red", "#00FF00"]))
            root.after(40, lambda: shake(count - 1))
        else:
            root.geometry(f"+{orig_x}+{orig_y}")
            chat_box.config(bg="black", fg="#00FF00")
    shake(10)

def update_user_list(users_array):
    global current_active_users
    current_active_users = users_array
    for widget in users_list_frame.winfo_children(): widget.destroy()
    for user in users_array:
        color = "#FF00FF" if user == nickname else ("red" if "★" in user else "#00FF00")
        lbl = tk.Label(users_list_frame, text=user, bg="black", fg=color, font=terminal_font, anchor="w", cursor="hand2")
        lbl.pack(fill=tk.X, padx=5)
        lbl.bind("<Button-1>", lambda event, u=user: prepare_whisper(u))

def receive():
    global message_count
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            elif message.startswith("USERLIST:"):
                users_string = message.replace("USERLIST:", "")
                active_users = users_string.split(",")
                root.after(0, update_user_list, active_users)
            
            elif message == "KICKED_BY_ADMIN":
                messagebox.showerror("BAĞLANTI KESİLDİ", "BİR SİSTEM YÖNETİCİSİ TARAFINDAN AĞDAN ATILDINIZ.")
                client.close()
                root.destroy()
                sys.exit()
                
            elif message == "CLEARALL_CMD":
                chat_box.config(state=tk.NORMAL)
                chat_box.delete('1.0', tk.END)
                chat_box.insert(tk.END, "<SİSTEM> AĞ ÜZERİNDEKİ TÜM VERİLER YÖNETİCİ TARAFINDAN İMHA EDİLDİ.\n", "system")
                chat_box.config(state=tk.DISABLED)
                play_sound(800, 50)
                root.after(0, trigger_glitch)
                root.after(10, scroll_to_bottom)
                
            elif message.startswith("CRYPT|"):
                parts = message.split("|", 2)
                sender = parts[1]; content = parts[2]
                
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, f"[ŞİFRELİ VERİ] <{sender}> : ", "other")
                
                tag_name = f"crypt_{random.randint(10000, 99999)}"
                gibberish = "".join(random.choice("!@#$%^&*()_+X?><") for _ in range(len(content)))
                
                chat_box.insert(tk.END, gibberish + "\n", tag_name)
                
                chat_box.tag_config(tag_name, foreground="yellow", underline=True)
                chat_box.tag_bind(tag_name, "<Button-1>", lambda e, t=tag_name, c=content: decode_text(t, c))
                chat_box.tag_bind(tag_name, "<Enter>", lambda e, t=tag_name: chat_box.config(cursor="hand2"))
                chat_box.tag_bind(tag_name, "<Leave>", lambda e, t=tag_name: chat_box.config(cursor="arrow"))
                
                chat_box.config(state=tk.DISABLED)
                play_sound(700, 150)
                message_count += 1
                root.after(10, scroll_to_bottom)
                
            elif message.startswith("WHISPER_RECV|"):
                parts = message.split("|", 2)
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, f"[FISILTI] <{parts[1]}>  {parts[2]}\n", "whisper")
                chat_box.config(state=tk.DISABLED)
                play_sound(500, 150); message_count += 1
                root.after(10, scroll_to_bottom)
                
            elif message.startswith("WHISPER_ECHO|"):
                parts = message.split("|", 2)
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, f"[FISILTI -> {parts[1]}]  {parts[2]}\n", "whisper_echo")
                chat_box.config(state=tk.DISABLED)
                message_count += 1
                root.after(10, scroll_to_bottom)
                
            else:
                chat_box.config(state=tk.NORMAL)
                if message.startswith(f"<{nickname}>"): chat_box.insert(tk.END, message + "\n", "me")
                elif message.startswith("<SİSTEM>"): 
                    chat_box.insert(tk.END, message + "\n", "system"); play_sound(400, 300); root.after(0, trigger_glitch)
                elif message.startswith("<THE WATCHER>") or message.startswith("<UNKNOWN_NODE>") or message.startswith("<SYS_ADMIN>"):
                    chat_box.insert(tk.END, message + "\n", "watcher"); play_sound(250, 600); root.after(0, trigger_glitch) 
                else: chat_box.insert(tk.END, message + "\n", "other"); play_sound(800, 100) 
                chat_box.config(state=tk.DISABLED)
                message_count += 1
                root.after(10, scroll_to_bottom)
        except Exception as e:
            client.close()
            break

def send_message(event=None):
    global message_count
    msg = entry_field.get()
    if msg.strip() != "":
        cmd = msg.strip()
        
        # --- TERMİNAL KOMUTLARI ---
        if cmd.lower() == ">clear":
            chat_box.config(state=tk.NORMAL)
            chat_box.delete('1.0', tk.END)
            chat_box.config(state=tk.DISABLED)
            play_sound(800, 50)
            
        elif cmd.lower() == ">help":
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, "-"*50 + "\n", "system")
            chat_box.insert(tk.END, "[SİSTEM KOMUTLARI]\n", "system")
            chat_box.insert(tk.END, ">help    : Bu ekranı gösterir.\n", "other")
            chat_box.insert(tk.END, ">clear   : Ekrandaki tüm yazıları siler.\n", "other")
            chat_box.insert(tk.END, ">stats   : Ağdaki anlık istatistikleri gösterir.\n", "other")
            chat_box.insert(tk.END, ">log     : Sohbet geçmişini .md (Markdown) olarak kaydeder.\n", "other")
            chat_box.insert(tk.END, ">crypt [Mesaj] : Mesajı şifreli olarak ağa gönderir.\n", "other")
            chat_box.insert(tk.END, ">whisper [İsim]: [Mesaj] : Hedefe fısıldar.\n", "other")
            if is_admin:
                chat_box.insert(tk.END, "[ADMİN KOMUTLARI]\n", "watcher")
                chat_box.insert(tk.END, ">kick [İsim]  : Kullanıcıyı sistemden zorla atar.\n", "watcher")
                chat_box.insert(tk.END, ">clearall     : Ağdaki herkesin ekranını zorla siler.\n", "watcher")
            chat_box.insert(tk.END, "-"*50 + "\n", "system")
            chat_box.config(state=tk.DISABLED)
            play_sound(800, 50)
            root.after(10, scroll_to_bottom)
            
        # ESKİ KOMUTLAR GERİ DÖNDÜ: >stats ve >log
        elif cmd.lower() == ">stats":
            user_count = len(current_active_users)
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, "-"*50 + "\n", "system")
            chat_box.insert(tk.END, f"[AĞ DURUMU - Düğüm: {nickname.upper()}]\n", "system")
            chat_box.insert(tk.END, f"Aktif Kullanıcı/Bot Sayısı: {user_count}\n", "other")
            chat_box.insert(tk.END, f"İşlenen Toplam Veri Paketi : {message_count}\n", "other")
            chat_box.insert(tk.END, "-"*50 + "\n", "system")
            chat_box.config(state=tk.DISABLED)
            play_sound(800, 50)
            root.after(10, scroll_to_bottom)
            
        elif cmd.lower() == ">log":
            history = chat_box.get('1.0', tk.END)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"theriver_log_{timestamp}.md"
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("---\n")
                    f.write(f"title: The River Archive - {nickname}\n")
                    f.write(f"date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("tags: [theriver, archive, darkweb]\n")
                    f.write("---\n\n")
                    f.write(f"# THE CIRCLE LOG - Düğüm: {nickname}\n\n")
                    f.write("```text\n") 
                    f.write(history)
                    f.write("```\n")
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, f"<SİSTEM> Kayıtlar mühürlendi. Dosya: {filename}\n", "system")
                chat_box.config(state=tk.DISABLED)
            except Exception as e:
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, f"<SİSTEM> Kritik Arşiv Hatası: {str(e)}\n", "system")
                chat_box.config(state=tk.DISABLED)
            play_sound(400, 200)
            root.after(10, scroll_to_bottom)

        elif cmd.lower().startswith(">crypt "):
            msg_content = cmd[7:].strip()
            client.send(f"CRYPT|{nickname}|{msg_content}".encode('utf-8'))
            
        elif cmd.lower().startswith(">kick "):
            if is_admin:
                target = cmd[6:].strip()
                client.send(f"KICK|{target}".encode('utf-8'))
            else:
                messagebox.showerror("HATA", "Bu komutu kullanmak için YÖNETİCİ yetkiniz yok.")
                
        elif cmd.lower() == ">clearall":
            if is_admin:
                client.send("CLEARALL".encode('utf-8'))
            else:
                messagebox.showerror("HATA", "Bu komutu kullanmak için YÖNETİCİ yetkiniz yok.")
                
        elif cmd.lower().startswith(">whisper "):
            try:
                target_name, msg_content = cmd[9:].split(":", 1)
                whisper_packet = f"WHISPER|{target_name.strip()}|{nickname}|{msg_content.strip()}"
                client.send(whisper_packet.encode('utf-8'))
            except ValueError:
                chat_box.config(state=tk.NORMAL); chat_box.insert(tk.END, "<SİSTEM> Hatalı format. Kullanım: >whisper İsim: mesaj\n", "system"); chat_box.config(state=tk.DISABLED)

        else:
            client.send(f"<{nickname}>  {msg}".encode('utf-8'))
            
        entry_field.delete(0, tk.END)

entry_field.bind("<Return>", send_message)
entry_field.focus()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()