import requests
import json
import re
import time

headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
#基金今日预计走势
def compare(val1,val2):
    if float(val1) - float(val2) > 0:
        return 1
    elif float(val1) - float(val2) < 0:
       return -1 
    else:
        return 0  

def jj(codes,hs):
    l=[]
    for code in codes:
        url = f"http://fundgz.1234567.com.cn/js/{code}.js"
        r = requests.get(url,headers = headers)
        content = r.text
        pattern = r'^jsonpgz\((.*)\)'
        search = re.findall(pattern, content)
        try:
            result = json.loads(search[0])
        except:
            print(code + '获取最新估值失败')
            r = [h for h in hs if h['fundcode']== code]
            result = r[0]
        else:
            result = json.loads(search[0])
            result['jzrq'] = result['jzrq'][5::]
        try:
            result['zzl'] = jj_dwjz([code])[-1]['equityReturn']
        except:
            print(code + '获取历史数据失败')
            result[0] = [h for h in hs if h['fundcode']== code]
            l.append(result[0])
        else:
            result['bh'] = 0
            for h in hs:
                if h['fundcode'] == code:
                    result['bh']= compare(result['gsz'],h['gsz'])
            l.append(result)
    d = update_date(l)
    return [l,d]
    #'fundcode': '003834', 'name': '华夏能源革新股票', 'jzrq': '2021-02-19', 'dwjz': '2.8550', 'gsz': '2.9333', 'gszzl': '2.74', 'gztime': '2021-02-22 13:42'}

def update_date(list):
    d=[]
    for l in list:
       d.append(l['jzrq']) 
    if d.count(max(d)) >= len(list)/2:
        return max(d)
    else:
        return min(d)

#基金单位净值变化趋势
def jj_dwjz(codes):
    l = []
    for code in codes:
        if code =='968061':
            url='http://overseas.1234567.com.cn/overseasapi/OpenApiHander.ashx?api=HKFDApi&m=MethodJZ&hkfcode=1002075741&action=2'
            r = requests.get(url,headers = headers)
            data = json.loads(r.text)
            ll =[]
            for i in data['Data']:
                ii={}
                ii['code'] = i['FCODE']
                ii['x'] = i['PDATE']
                ii['y'] = i['NAVCHG']
                ii['equityReturn'] = i['NAVCHGRT']
                ii['unitMoney'] = ''
                ll.append(ii)
            ll.reverse()
            l = l + ll
        else:
            url = f'http://fund.eastmoney.com/pingzhongdata/{code}.js'
            r = requests.get(url,headers = headers)
            pattern = r' Data_netWorthTrend = (.*?);'
            content = re.findall(pattern,r.text)
            data = json.loads(content[0])
            for i in data:
                i['code'] = code
                i['x'] = timeStamp(i['x'])
                l.append(i)
    return l
    #{'x': '2021-02-19', 'y': 2.855, 'equityReturn': -2.36, 'unitMoney': ''}]

#基金累计净值变化趋势
def jj_ljjz(codes):
    for code in codes:
        url = f'http://fund.eastmoney.com/pingzhongdata/{code}.js'
        r = requests.get(url,headers = headers)
        pattern = r'Data_netWorthTrend =(.*?);'
        content = re.findall(pattern,r.text)
        data = json.loads(content[0])
        l = []
        for i in data:
            i['x'] = timeStamp(i['x'])
            l.append(i)
    return l

#将时间戳（毫秒级）转换成时间,只保留年月日
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime

if __name__ == '__main__':
    jj(['968061','004997'],[])
