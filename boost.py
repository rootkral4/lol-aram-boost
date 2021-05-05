import subprocess
import re
import urllib3
from tkinter import *

tk = Tk()

tk.geometry("600x200")
tk.title("LoL Aram Boost")
tk['background']="#313131"
tk.resizable(False,False)

def getstuff():
    try:
        output = subprocess.Popen("WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline", stdout=subprocess.PIPE, shell=True).stdout.read().decode('utf-8')
        port = re.findall(r'"--app-port=(.*?)"', output)[0]
        password = re.findall(r'"--remoting-auth-token=(.*?)"', output)[0]
        return port, password
    except IndexError:
        return None, None

def boost(port, password):
    try:
        urllib3.disable_warnings()
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        headers = urllib3.make_headers(basic_auth='riot:' + password)
        r = http.request('POST', f'https://127.0.0.1:{port}/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1",""]', headers=headers)
        if "flex.messaging.messages.AcknowledgeMessage" in r.data.decode():
            myText.config(text="Boosted!")
        else:
            myText.config(text="An error occured")
    except:
        myText.config(text="An error occured")
        pass

def main():
    p, passwd = getstuff()
    if p == None and passwd == None:
        myText.config(text="League client isn't running")
    else:
        boost(p,passwd)

myText = Label(tk,text="Boost!",font="Arial 15",bg="#313131",fg="white")
myInfoText = Label(tk,text="Press 'Boost!' to boost lobby or Press 'Exit' to exit",font="Arial 10",bg="#313131",fg="white")
button = Button(tk, text="Boost!", font="Arial", command=main, bg="red",fg="white",height=1,width=13)
exitButton = Button(tk, text="Exit", font="Arial", command=tk.destroy, bg="red",fg="white",height=1,width=13)

myText.place(x=60, y=55)
myInfoText.place(x=30,y=110)
button.place(x =400, y=40)
exitButton.place(x =400, y=100)

tk.mainloop()