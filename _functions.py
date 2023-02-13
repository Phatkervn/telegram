import glob

import aiohttp
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from aiosocksy import Socks5Auth

import re
def checkVietnamese(self, text):
    check = re.findall(
        r'(?i)[áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]', text)
    if len(check) > 1:
        return True
    else:
        return False
    
def getProxy(filename):
    listProxys = []
    with open(filename) as f:
        lines = [i.strip() for i in f.readlines()]
    for line in lines:
        row = line.split(":")
        data = {
                    'ip': row[0],
                    'port': int(row[1]),
                    'user': row[2],
                    'password': row[3],
                }
        listProxys.append(data)
    return listProxys
    
async def runCheckProxy(proxies):
    proxy = f'socks5://{proxies["ip"]}:{proxies["port"]}'
    if 'user' in proxies:
        proxy_auth = Socks5Auth(proxies["user"], password=proxies["password"])
    else:
        proxy_auth = None
    connector = ProxyConnector()
    url = 'https://api.telegram.org/'
    head = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }
    try:
        async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
            async with session.get(url, headers=head, proxy=proxy, proxy_auth=proxy_auth) as response:
                return True
    except aiohttp.client_exceptions.ClientConnectorCertificateError:
        print('dont SSL')
        return False
    except aiohttp.client_exceptions.ClientProxyConnectionError:
        print('proxy dont connect')
        return False
    except Exception as e:
        print('ERROR', e)
        return False
    

def findSession(path):
    path = path + r"/*.session"
    files = glob.glob(path)
    return files

def getListPhone(path):
    with open(path,"r") as f:
        data = [i.strip() for i in f.readlines()]
        return data
def writeResultPhone(path,phone):
    with open(path,'a+') as f:
        f.write("{}\n".format(phone))
# from _var import *
# findSession(PATHSESSION)
def writeFloodSession(session):
    with open("floodsession.txt","a+") as f:
        f.write(session+"\n")