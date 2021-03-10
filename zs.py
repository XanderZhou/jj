import requests
import json

def zs_compare(val1,val2):
    if int(val1) - int(val2) >0:
        return 1
    elif int(val1) - int(val2) <0:
        return -1
    else:
        return 0

def zs(codes,ls):
    result= []
    for code in codes:
        url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={code}&fields=f43,f169,f170' 
        r = requests.get(url)
        content = r.text
        content = json.loads(content)
        jg = content['data']
        jg['code'] = code
        for l in ls:
            if l['code'] == code:
                jg['bh']= zs_compare(jg['f43'],l['f43'])
        result.append(jg) 
    return result 
#对就上证指数、深证成数、创业板指
#codes = ['1.000001','0.399001','0.399006']