import subprocess
import re
import urllib3
import keyboard

"""
source code :x00bence
i just modified, prettified and made easier to use
"""

def getstuff():
    try:
        output = subprocess.Popen("WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline", stdout=subprocess.PIPE, shell=True).stdout.read().decode('utf-8')
        port = re.findall(r'"--app-port=(.*?)"', output)[0]
        password = re.findall(r'"--remoting-auth-token=(.*?)"', output)[0]
        return port, password
    except IndexError:
        print("League client isn't running")
        return None, None

def boost(port, password):
    urllib3.disable_warnings()
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    headers = urllib3.make_headers(basic_auth='riot:' + password)
    r = http.request('POST', f'https://127.0.0.1:{port}/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1",""]', headers=headers)
    if "flex.messaging.messages.AcknowledgeMessage" in r.data.decode():
        print('[+] Boosted')
    else:
        print("an error occured")

def main():
    p, passwd = getstuff()
    if p == None and passwd == None:
        exit()
    print(f'[i] Success Port :{p} Token :{passwd}')
    print("[i] Press \"CTRL+UP\" to boost lobby, Press CTRL+C or ENTER to exit")
    keyboard.add_hotkey("ctrl+up", boost, (p, passwd))
    input()

try:
    main()
except KeyboardInterrupt:
    exit()
