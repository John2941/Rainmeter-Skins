import requests
import base64
import re
import os
from bs4 import BeautifulSoup

print 'Updating TING information'
s = requests.Session()
url_login, url = "https://ting.com/account/login", 'https://ting.com/account'

login = {
        'first_name':'',
        'last_name':'',
        'phone':'',
        'email':'',     # enter email
        'password':'',  # enter password
        'confirm_password':'',
        'send_news':'on',
        'send_device_alerts':'on',
        'existing_user_login':'existing_user_login'
        }
s.post(url_login, login)
account_text = s.get(url)
soup = BeautifulSoup(account_text.text)#.encode('utf-8', 'ignore')

numbers = soup.findAll('span',{'class':'detail'})
price_tier = soup.findAll('div',{'class':'note'})
price_of_price_tier = soup.findAll('li',{'class':'center'})## [0] = minutes [1] = text [2] = data
current_price = soup.findAll('p',{'class':'highlight marketing'})
current_bill = re.findall(r'<strong>\s*(.*)</strong>',str(current_price[0]))[0]
end_bill_cycle = re.findall(r'and closes on (.+)\s*\((.*)\)',str(current_price[0]))[0] # [0].strip() contains the date [1] has the number of days left
matts_stats = 1
stephanys_stats = 1
#numbers[1].string will give me my number... no need to loop take that out

##<a href="/account/current_usage?type=minutes">Minutes</a>#megabytesChart > li.center > h3
print 'Success!'

x1 = 'Minutes: {0} -- Price Tier: {2} {1}'.format(numbers[0].text.strip(), price_tier[0].text.strip(), re.findall(r'<br/>\s*(.*)\s*<br/>', str(price_of_price_tier[0]))[0])
minute_totals = numbers[0].text.strip()
minute_tier = price_tier[0].text.strip().strip('()')
minute_price = re.findall(r'<br/>\s*(.*)\s*<br/>',str(price_of_price_tier[0]))[0].strip('$')
x2 = 'Texts: {0}  -- Price Tier: {2} {1}'.format(numbers[1].text.strip(),price_tier[1].text.strip(),re.findall(r'<br/>\s*(.*)\s*<br/>',str(price_of_price_tier[1]))[0])
text_totals = numbers[1].text.strip()
text_tier = price_tier[1].text.strip().strip('()')
text_price = re.findall(r'<br/>\s*(.*)\s*<br/>',str(price_of_price_tier[1]))[0].strip('$')
x3 = 'Data: {0} Megabytes -- Price Tier: {2} {1}'.format(numbers[2].text.strip(),price_tier[2].text.strip(),re.findall(r'<br/>\s*(.*)\s*<br/>',str(price_of_price_tier[2]))[0])
data_totals = numbers[2].text.strip()
data_tier = price_tier[2].text.strip().strip('()')
data_price = re.findall(r'<br/>\s*(.*)\s*<br/>',str(price_of_price_tier[2]))[0].strip('$')
x4 = 'Current Bill: {0} and closes out on {1} ({2})'.format(current_bill,end_bill_cycle[0].strip(),end_bill_cycle[1])
current_bill = re.findall(r'<strong>\s*(.*)</strong>',str(current_price[0]))[0]
current_bill_amountonly = re.findall('<strong>\s*\$([\d\.]{2,6})\W',str(current_price[0]))[0]
x5 = 'Average Bill: {0}'.format(numbers[5].text.strip())
average_bill = numbers[5].text.strip().strip('$')
x6 = 'Last Bill: {0}'.format(numbers[6].text.strip())
last_bill = numbers[6].text.strip().strip('$')

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(current_dir + '\results.txt','w') as f:
    f.write('1['+x1+']\n')
    f.write('minute_total('+minute_totals+')\n')
    f.write('minute_tierF('+re.findall('\d*[^\D*]\d*',minute_tier)[0]+')\n')
    f.write('minute_tierL('+re.findall('\d*[^\D*]\d*',minute_tier)[1]+')\n')
    f.write('minute_price('+minute_price+')\n')
    f.write('2['+x2+']\n')
    f.write('text_total('+text_totals+')\n')
    f.write('text_tierF('+re.findall('\d*[^\D*]\d*',text_tier)[0]+')\n')
    f.write('text_tierL('+re.findall('\d*[^\D*]\d*',text_tier)[1]+')\n')
    f.write('text_price('+text_price+')\n')
    f.write('3['+x3+']\n')
    f.write('data_total('+data_totals+')\n')
    f.write('data_tierF('+re.findall('\d*[^\D*]\d*',data_tier)[0]+')\n')
    f.write('data_tierL('+re.findall('\d*[^\D*]\d*',data_tier)[1]+')\n')
    f.write('data_price('+data_price+')\n')
    f.write('4['+x4+']\n')
    f.write('current_bill('+current_bill_amountonly+')\n')
    f.write('5['+x5+']\n')
    f.write('average_bill('+average_bill.strip('$')+')\n')
    f.write('6['+x6+']\n')
    f.write('last_bill('+last_bill.strip('$')+')\n')