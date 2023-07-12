import tkinter as tk
import tkinter.font as tkFont
import socket
import threading
class App:
    client_connection = None
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg_box = None
    msg_input = None
    port_input = None
    connected_label = None
    def __init__(self, root):
        #setting title
        root.title("Instant LAN Messenger Server")
        #setting window size
        width=482
        height=365
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        port_label=tk.Label(root)
        ft = tkFont.Font(family='serif',size=10)
        port_label["font"] = ft
        port_label["fg"] = "#333333"
        port_label["justify"] = "center"
        port_label["text"] = "Port Number: "
        port_label.place(x=20,y=23,width=91,height=30)

        connected_label=tk.Label(root)
        ft = tkFont.Font(family='serif',size=10)
        connected_label["font"] = ft
        connected_label["fg"] = "#333333"
        connected_label["justify"] = "center"
        connected_label["text"] = "Not connected"
        connected_label.place(x=140,y=60,width=70,height=25)
        connected_label.pack()
        self.connected_label = connected_label


        listen_btn=tk.Button(root)
        listen_btn["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='serif',size=10)
        listen_btn["font"] = ft
        listen_btn["fg"] = "#000000"
        listen_btn["justify"] = "center"
        listen_btn["text"] = "Start Listening"
        listen_btn.place(x=280,y=20,width=100,height=35)
        listen_btn["command"] = self.listen_btn_command


        port_input=tk.Entry(root)
        port_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='serif',size=10)
        port_input["font"] = ft
        port_input["fg"] = "#333333"
        port_input["justify"] = "left"
        port_input["text"] = ""
        port_input.place(x=120,y=20,width=150,height=35)
        self.port_input = port_input

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

        msg_frame = tk.Frame(root)
        msg_frame.place(x=20,y=70,width=450,height=230)

        msg_box_scrollbar = tk.Scrollbar(msg_frame)
        msg_box_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        msg_box = tk.Text(msg_frame, wrap=tk.WORD, yscrollcommand=msg_box_scrollbar.set, state="normal")
        msg_box.pack(expand=True, fill=tk.BOTH)

        msg_box_scrollbar.config(command=msg_box.yview)
        self.msg_box = msg_box



    def listen_btn_command(self):
        port_inputt = int(self.port_input.get())
        with open('server_config.txt', 'w') as f:
            f.write(f"{port_inputt}")
        self.soc.bind(('localhost',port_inputt))
        self.soc.listen()
        print("Waiting for Client...")

        while True:
            con, address = self.soc.accept()
            self.connected_label["text"] = f"Connected to Client: {address}"
            self.connected_label["fg"] = "green"
            print('Connected to Client: ', address)
            self.client_connection = con
            break
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        

    def send_btn_command(self):
        msgInput = self.msg_input.get()
        self.msg_box.insert('1.0', f'You: {msgInput}\n\n')
        self.client_connection.send(bytes(msgInput, 'utf-8'))
        print(msgInput)
        self.msg_input.delete(0, len(msgInput))

    def receive(self):
        while True:
            msg = self.client_connection.recv(1024).decode('utf-8')
            self.msg_box.insert('1.0', f'Client: {msg}\n\n')
            print(msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
