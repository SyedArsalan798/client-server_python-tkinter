import tkinter as tk
import tkinter.font as tkFont
import socket
import threading
class App:

    ip_port_input = None
    isConnected = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, root):
        root.title("Instant LAN Messenger Client")
        width=482
        height=365
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)


        ip_port_label=tk.Label(root)
        ft = tkFont.Font(family='serif',size=10)
        ip_port_label["font"] = ft
        ip_port_label["fg"] = "#333333"
        ip_port_label["justify"] = "center"
        ip_port_label["text"] = "Enter IP and Port: "
        ip_port_label.place(x=10,y=10,width=124,height=30)

        connect_btn=tk.Button(root)
        connect_btn["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='serif',size=10)
        connect_btn["font"] = ft
        connect_btn["fg"] = "#000000"
        connect_btn["justify"] = "center"
        connect_btn["text"] = "Connect"
        connect_btn.place(x=250,y=40,width=95,height=30)
        connect_btn["command"] = self.connect_btn_command

        ip_port_input=tk.Entry(root)
        ip_port_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='serif',size=10)
        ip_port_input["font"] = ft
        ip_port_input["fg"] = "#333333"
        ip_port_input["justify"] = "left"
        ip_port_input["text"] = ""
        ip_port_input.place(x=20,y=40,width=220,height=30)
        self.ip_port_input = ip_port_input

        send_btn=tk.Button(root)
        send_btn["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='serif',size=10)
        send_btn["font"] = ft
        send_btn["fg"] = "#000000"
        send_btn["justify"] = "center"
        send_btn["text"] = "Send"
        send_btn.place(x=390,y=320,width=72,height=30)
        send_btn["command"] = self.send_btn_command

        msg_input=tk.Entry(root)
        msg_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='serif',size=10)
        msg_input["font"] = ft
        msg_input["fg"] = "#333333"
        msg_input["justify"] = "left"
        msg_input["text"] = ""
        msg_input.place(x=20,y=320,width=359,height=30)
        self.msg_input = msg_input

        isConnected=tk.Label(root)
        ft = tkFont.Font(family='serif',size=10)
        isConnected["font"] = ft
        isConnected["fg"] = "#333333"
        isConnected["justify"] = "center"
        isConnected["text"] = "Not Connected"
        isConnected.place(x=80,y=70,width=101,height=30)
        self.isConnected = isConnected


        msg_frame = tk.Frame(root)
        msg_frame.place(x=20,y=100,width=450,height=200)

        msg_box_scrollbar = tk.Scrollbar(msg_frame)
        msg_box_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        msg_box = tk.Text(msg_frame, wrap=tk.WORD, yscrollcommand=msg_box_scrollbar.set, state="normal")
        msg_box.pack(expand=True, fill=tk.BOTH)

        msg_box_scrollbar.config(command=msg_box.yview)
        self.msg_box = msg_box

    def connect_btn_command(self):
        with open('server_config.txt', 'r') as f:
            File_accessed_port = int(f.readline().strip())
            ip_and_port_Combined = self.ip_port_input.get()
            ip_and_port_Combined = ip_and_port_Combined.split(':') #[ip, port]
            ip = ip_and_port_Combined[0]
            cPort = int(ip_and_port_Combined[1])
            if (File_accessed_port != cPort):
                print("Failed")
            else:
                try:
                    if ip == '127.0.0.1' or ip == 'localhost':
                        self.s.connect((ip, cPort))
                        
                        self.receive_thread = threading.Thread(target=self.receive)
                        self.receive_thread.start()

                        self.isConnected["text"] = "Connected"
                        self.isConnected["fg"] = "green"
                    else:
                        self.isConnected["text"] = "Not Connected"
                        self.s.close()
                except:
                    print("Connection Refused.")
    
    def receive(self):
        while True:
            msg = self.s.recv(1024).decode('utf-8')
            self.msg_box.insert('1.0', f'Server: {msg}\n\n')
            print(msg)


    def send_btn_command(self):
        msgInput = self.msg_input.get()
        self.msg_box.insert('1.0', f'You: {msgInput}\n\n')
        self.s.send(bytes(msgInput, 'utf-8'))
        print(msgInput)
        self.msg_input.delete(0, len(msgInput))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
