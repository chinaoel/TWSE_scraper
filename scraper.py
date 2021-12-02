import requests
import sys
import time
from datetime import datetime, timedelta
import random
from common import dateformat, toSQL


pattern = '%Y%m%d'
DOMAIN = 'https://www.twse.com.tw'
# T86 : 三大法人買賣超日報
proxy_list = []
proxies = ''
API_URL = 'https://www.twse.com.tw/fund/T86?response=json&date={}&selectType=ALL&_={}'
Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
if len(sys.argv) != 3:
    print('Please input the start date and end date in this format : yyyymmdd')
    sys.exit()

start = sys.argv[1]
end = sys.argv[2]
try:
    interval = datetime(year=int(end[:4]),month=int(end[4:6]),day=int(end[6:8])) - datetime(year=int(start[:4]),month=int(start[4:6]),day=int(start[6:8])) 
    end_date = datetime(year=int(end[:4]),month=int(end[4:6]),day=int(end[6:8])) 
except Exception as e:
    print(e)
    print('Invalid input format, check again.')
    sys.exit()

try:
    with open('proxies_list.txt','r') as txtfile:
        proxy_list = [s.strip('\n') for s in txtfile.readlines()]
except:
    print('Reading proxies failed')
    sys.exit()


for i in range(interval.days):
    
    try:
        
        pg_url = API_URL.format(end,int(time.time()))
        print(pg_url)
        time.sleep(random.randint(3,5))
        if not proxies:
            resp = requests.get(pg_url,headers=Headers, proxies=proxies,timeout=5)
        else:
            resp = requests.get(pg_url,headers=Headers,timeout=5)
        end_date = datetime(year=int(end[:4]),month=int(end[4:6]),day=int(end[6:8]))
        
        if 'data' in resp.json():
            data = resp.json()['data']
            print('Found data : '.format(end))
            toSQL(data, end)
        else:
            print('No Found data : '.format(end))
                    
        end = dateformat(end_date)
    except Exception as e:
        print(e)
        proxy = random.sample(proxy_list, k=1)[0]
        proxies = {
                "http": "http://"+proxy,
                "https": "http://"+proxy
                  }


