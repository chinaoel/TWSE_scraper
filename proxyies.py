import requests
proxy_api_url = 'https://proxylist.geonode.com/api/proxy-list'
Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
check_proxy_url = 'https://api.ipify.org?format=json'
proxy_list = []

resp = requests.get(proxy_api_url,headers=Headers)
if resp.status_code == 200:
    resp_json = resp.json()
    for i in resp_json['data']:
        proxy_list.append(i['ip'] + ':' + i['port'])
print(proxy_list)
for proxy in proxy_list:
    proxies = {
                "http": "http://"+proxy,
                "https": "http://"+proxy
              }
    try:
        ip = requests.get(check_proxy_url,proxies=proxies, timeout=5).json()['ip']
    except:
        ip = ''
    print(ip, proxy.strip(':')[0])
    if ip != proxy.strip(':')[0] : proxy_list.remove(proxy)
with open('proxies_list.txt','w') as txtfile:
    for proxy in proxy_list:
        txtfile.write(proxy+'\n')