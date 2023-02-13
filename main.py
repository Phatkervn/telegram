

import asyncio
from threading import Thread


from _functions import *
from _var import *
from _telegram import *

totalERROR = 0

def main(session):
    proxy = listProxy.pop(0)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    proxyLive = loop.run_until_complete(runCheckProxy(proxy))
    loop.close()
    if proxyLive == True:
        tele = Telegram(session,proxy=proxy)
        async def run():
            is_connect = await tele.connect()
            print(session,proxy["ip"],"live" if is_connect else "chết")
            if is_connect :
                global totalERROR
                while totalERROR < 20:
                    try:
                        phone = listPhone.pop(0)
                        is_phone = await tele.addMemberContact(phone)
                        if is_phone == 200:
                            writeResultPhone(PATHPHONERESULT,phone)
                        if is_phone == 400:
                            print("dính flood!: ",session)
                            writeFloodSession(session)
                            break
                        if is_phone == 404:
                            totalERROR += 1
                    except IndexError:
                        print("hết phone")
                        break
                    #await asyncio.sleep(1)
                else :
                    print("lỗi quá 20 => Dừng , các phone chưa sài lưu vào file out.txt")
        asyncio.run(run())
        

listProxy = getProxy(PATHPROXY)

listSessions = findSession(PATHSESSION)

listTheads = []

listPhone = getListPhone(PATHPHONE)

for session in listSessions:
    #print(session)
    t = Thread(target=main , args=(session,))
    listTheads.append(t)

# start
[th.start() for th in listTheads]

# join
[th.join() for th in listTheads]
if len(listPhone) > 0:
    with open(PATHOUTPHONE,"a+") as f:
        f.write("\n".join(listPhone)) 

