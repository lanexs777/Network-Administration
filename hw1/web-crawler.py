#!/usr/bin/python3

from prettytable import PrettyTable
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageEnhance, ImageFilter
import urllib
import pytesseract
import time
import requests
import sys
import getpass

def help_():
	print("usage: main.py [-h] username \n\nWeb crawler for NCTU class schedule.\n\npositional argument:\n  username   username of NCTU portal\n\noptional argument: \n  -h, --help show this help message and exit\n")
	sys.exit()

if sys.argv[1].startswith("-"):
	help_()
else:
	username2 = ''.join(sys.argv[1:])
	password2 = getpass.getpass("Enter the password:")

login_success = 0

while login_success == 0:

	session_login = requests.Session()
	url = "https://portal.nctu.edu.tw/portal/login.php"
	login_url = "https://portal.nctu.edu.tw/portal/chkpas.php?"
	t_login = session_login.get(url)

	obj = BeautifulSoup(t_login.text, "html.parser")
	img_ = obj.find("img", {"id":"captcha"})
	img_link = urllib.parse.urljoin(url, img_['src'])

	t = session_login.get(img_link)
	with open("captcha.jpg", "wb") as f:
		f.write(t.content)
		f.close()

	img_open = Image.open('captcha.jpg').convert('LA')
	en_img_c = ImageEnhance.Contrast(img_open).enhance(2)
	en_img_b = ImageEnhance.Brightness(en_img_c).enhance(2)
	text = pytesseract.image_to_string(en_img_b)
	
	username = '0310029'
	password = 'richard777'

	payload = { 'username': username2,
				'password': password2,
				'seccode': text,
				'Submit2': "登入(Login)",
				'pwdtype': "static" }
			
	login = session_login.post(login_url, data=payload)
	if "PortalMain" in login.url:
		login_success = 1
	
obj2 = BeautifulSoup(login.text, "html.parser")
course_pre = obj2.find("",{"name":"_48_INSTANCE_eLMP_iframe"})
course_pre_link = urllib.parse.urljoin(login.url, course_pre['src'])
#print(course_pre_link)

pre_course_ = session_login.get(course_pre_link)

obj3 = BeautifulSoup(pre_course_.text, "html.parser")
course_pre2 = obj3.find("", {"href":"../portal/relay.php?D=cos"})
course_link = urllib.parse.urljoin(course_pre_link, course_pre2['href'])

course_ = session_login.get(course_link)

obj4 = BeautifulSoup(course_.text, "html.parser")
info = obj4.findAll("input")

form_url = "https://course.nctu.edu.tw/jwt.asp"
txtId = info[0]['value']
txtPw = info[1]['value']
ldapDN = info[2]['value']
idno = info[3]['value']
s = info[4]['value']
t = info[5]['value']
txtTimestamp = info[6]['value']
hashKey = info[7]['value']
jwt = info[8]['value']
Chk_SSO = ""
Button1 = info[10]['value']


payload2 = { 'txtId': txtId,
			 'txtPw': txtPw,
			 'ldapDN': ldapDN,
			 'idno': idno,
			 's': s,
			 't': t,
			 'txtTimestamp': txtTimestamp,
			 'hashKey': hashKey,
			 'jwt': jwt,
			 'Chk_SSO': Chk_SSO,
			 'Button1': Button1 }

course_get = session_login.post(form_url, data=payload2)

table = session_login.get("https://course.nctu.edu.tw/adSchedule.asp")
table.encoding = 'big5'
table_obj = BeautifulSoup(table.text, "html.parser")

table = table_obj.find("table", {"colspan":"5"})
rows = table.find_all("tr")

data = []
count = 0
for row in rows:
	table_cell = row.find_all("td")
	if table_cell and count != 0:
		data.append([cell.get_text(strip=True).replace("&nbsp", " ") for cell in table_cell])
	count = 1

#print(data[0])

x = PrettyTable()

x.field_names = data[0]

for i in range(1,16):
	x.add_row(data[i])

print(x.get_string())	
