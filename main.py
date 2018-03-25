import json
from subprocess import Popen, PIPE

import requests
from prettytable import PrettyTable

p = Popen(['tracert', "-d", "www.tni.mil.id"], stdout=PIPE)

t = PrettyTable(['NO', 'IP', 'AS', 'COMAPNY', 'COUNTRY'])
counter = 0
while True:
    line = p.stdout.readline().decode('cp1251')
    if ("ms" in line):
        print('\n' * 40)
        counter = counter + 1
        ip = line.split(' ')[-2]
        dic = json.loads(requests.get(f"http://ip-api.com/json/{ip}").text)
        if dic['status'] == 'success':
            AS, company = dic['as'].split(' ', 1) if dic['as'] != '' else ['', '']
            t.add_row([counter, ip, AS, company, dic['country']])
        else:
            t.add_row([counter, ip, 'private', '-', '-'])
        print(t)
    if not line:
        break
