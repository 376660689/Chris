import sys
import time
import requests
import json


headers = {
    "User-Agent": "Mozilla/5.0(Macintosh;Intel Mac OS X 10.13;rv:64.0) Gecko/20100101 Firefox/64.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def ip2addr(host):
    '''
        返回ip或者域名的归属地
    '''
    InterFaceTotal = {
                        'pconline': 'http://whois.pconline.com.cn/ip.jsp?ip=%s' % host,
                        'taobao': 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % host,
                      }
    try:
        for InterfaceName in InterFaceTotal:
            req = requests.get(
                InterFaceTotal[InterfaceName],
                headers = headers
            )
            if req.status_code == 200:
                if InterfaceName == "pconline":
                    return req.text.replace('\n', '').replace('\r', '')

                if InterfaceName == "taobao":
                    res = json.loads(req.text)['data']
                    return '%s %s' % (res['country'], res['city'])
            else:
                continue
    except Exception as msg:
        raise msg

ip2addr('49.229.65.225')