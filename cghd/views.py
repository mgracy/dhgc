from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cghd.models import XlsInfo, Business
from django.contrib.auth.models import User
import cghd.excel
import os
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import hashlib
# from django.template import RequestContext

# Create your views here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('---------{}'.format(BASE_DIR))

def t2(req):
	user = req.user
	return render(req, 'cghd/t2.html',{'user':user})

@login_required
def index(req):
	user = req.user
	print('index..................')
	return render(req, 'cghd/index.html',{'user':user})

def uploaded(req):
	print('uploaded..................')
	return render(req, 'cghd/uploaded.html')

@login_required
def basicData(req):
	return render(req, 'cghd/basicData.html', {'urlPath': req.path})

@login_required
def master(req):
	return render(req, 'cghd/master.html', {'urlPath': req.path})


def login(req):
	if req.method == "POST":
		uf = UserFormLogin(req.POST)
		if uf.is_valid():
			username = uf.cleaned_data["username"]
			password = uf.cleaned_data["password"]
			userResult = User.objects.filter(username=username,password=password)
			if len(userResult) > 0:
				return render(req, 'ff.html', {})
			else:
				return HttpResponse('该用户不存在')

	else:
		uf = UserFormLogin()

	return render(req, 'userlogin.html', {'uf': uf})

@login_required
def supplier(req):
	return render(req, 'cghd/supplier.html', {'urlPath': req.path})

@login_required
def ar(req):
	return render(req, 'cghd/ar.html', {'urlPath': req.path})

@login_required
def ap(req):
	return render(req, 'cghd/ap.html', {'urlPath': req.path})

@login_required
def planSchedule(req):
	return render(req, 'cghd/planSchedule.html', {'urlPath': req.path})

@login_required
def businessFreight(req):
	return render(req, 'cghd/businessFreight.html', {'urlPath': req.path})

@login_required
def businessPurchaseSale(req):
	return render(req, 'cghd/businessPurchaseSale.html', {'urlPath': req.path})

@login_required
def finGAReport(req):
	return render(req, 'cghd/finGAReport.html', {'urlPath': req.path})

@login_required
def loadUnload(req):
	return render(req, 'cghd/loadUnload.html', {'urlPath': req.path})
@csrf_exempt
def uploadFile(req):
	if req.method == "POST":
		myFile = req.FILES.get('upfile')
		file = myFile.read()
		author = req.user.username
		with open('cghd/files/{}-{}'.format(author, myFile.name), 'wb') as fn:
			fn.write(file)
		my_file = os.path.join(BASE_DIR, 'files/{}-{}'.format(author, myFile.name))

		dataList = cghd.excel.ReadXls(my_file)

		print(str(dataList))

		return HttpResponse(str(dataList).replace("'",'"'))
	else:
		return HttpResponse("get")

@csrf_exempt
def uploadSupplier(req):
	if req.method == "POST":
		file = req.POST.get(u'fileName')

		excelFile = os.path.join(BASE_DIR, file)
		dataList = cghd.excel.ReadXls(excelFile)
		return HttpResponse("{'code':200}")
	else:
		print(req.method)
		return HttpResponse("get")

@csrf_exempt
def uploadMaster(req):
	if req.method == "POST":
		myFile = req.FILES.get('upfile')
		file = myFile.read()
		author = req.user.username
		with open('cghd/files/{}-{}'.format(author, myFile.name), 'wb') as fn:
			fn.write(file)
		my_file = os.path.join(BASE_DIR, 'files/{}-{}'.format(author, myFile.name))

		dataList = cghd.excel.ReadXls(my_file)

		# print(str(dataList))
		i = 0
		print('Now, we are going to save the dataList to db...')
		for data in dataList:
			print(u'卸货日期: {}'.format(data['卸货日期']))
			Business(Order = data['订单号'],
				In_Out = data['内外部'],
				Area = data['所属区域'],
				C_ID = data['客户ID'],
				C_BriefName = data['客户名称'],
				Unload_Address = data['卸气地'],
				Unload_Date = data['卸货日期'],
				S_ID = data['供应商ID'],
				S_BriefName = data['供应商'],
				Source_Address = data['气源地'],
				Carrier_ID = data['承运商ID'],
				Carrier_BriefName = data['承运公司'],
				Trade_Type = data['票制'],
				Load_Date = data['装货日期'],
				Tractor_No = data['牵引车号']
				# Tank_No = data['槽车号'],
				# Driver = data['驾驶员'],
				# Supercargo = data['押运员'],
				# Tele_No = data['手机号'],
				# State = data['状态'],
				# Update_Date = data['操作日期'],
				# Load_QTY = data['装气量（吨）'],
				# Unload_QTY = data['卸气量（吨）'],
				# Dispatch_Mark = data['调度备注'],
				# Electricity_Amount = data['电商号'],
				# Sales_QTY = data['销售结算量（吨）'],
				# PO_QTY = data['采购结算量（吨）'],
				# Logistics_QTY = data['物流结算量（吨）'],
				# Sales_Price_Letter = data['销售价格函'],
				# Sales_Price = 0,# data['销售单价'],
				# Sales_Amount = 0,#data['销售金额'],
				# Customer_CheckDate = data['客户核对'],
				# Customer_IsBilling = data['是否开票'],
				# PO_Price_Letter = data['采购价格函'],
				# PO_Price = 0,#data['采购单价'],
				# PO_Amount =0,#data['采购金额'],
				# Supplier_CheckDate = data['供应商核对'],
				# Supplier_IsBilling = data['是否开票'],
				# Logistics_Price_Letter = data['物流价格函'],
				# Logistics_Price = 0,#data['运输单价'],
				# Logistics_Amount = 0,#data['运费金额'],
				# Logistics_CheckDate = data['承运商核对'],
				# Logistics_IsBilling = data['是否开票']
				# M_Deviation = 1,
				# D_Deviation = 1
			).save()
			break
			i += 1
		print('i = {}'.format(i))
		print('Save the dataList to db completely...')

		return HttpResponse(str(dataList).replace("'",'"'))
	else:
		print('fffffffffffffffffffff')
		print(xldate_as_datetime('43034.0'))
		print('fffffffffffffffffffff')
		return HttpResponse("get")
		# M_Deviation = 0,#str2int(data['毛差']),
		# D_Deviation = 0#str2int(data['吨毛差'])
@csrf_exempt
def uploadAr(req):
	if req.method == "POST":
		myFile = req.FILES.get('upfile')
		file = myFile.read()
		author = req.user.username
		with open('cghd/files/{}-{}'.format(author, myFile.name), 'wb') as fn:
			fn.write(file)
		my_file = os.path.join(BASE_DIR, 'files/{}-{}'.format(author, myFile.name))

		dataList = cghd.excel.ReadXls(my_file)

		print(str(dataList))

		return HttpResponse(str(dataList).replace("'",'"'))
	else:
		return HttpResponse("get")

@csrf_exempt
def uploadAp(req):
	if req.method == "POST":
		myFile = req.FILES.get('upfile')
		file = myFile.read()
		author = req.user.username
		with open('cghd/files/{}-{}'.format(author, myFile.name), 'wb') as fn:
			fn.write(file)
		my_file = os.path.join(BASE_DIR, 'files/{}-{}'.format(author, myFile.name))

		dataList = cghd.excel.ReadXls(my_file)

		print(str(dataList))

		return HttpResponse(str(dataList).replace("'",'"'))
	else:
		return HttpResponse("get")

def uploadedFile(req):
	if req.method == "POST":
		myFile = req.FILES.get('upfile')
		file = myFile.read()
		author = req.user.username
		with open('cghd/files/{}-{}'.format(author, myFile.name), 'wb') as fn:
			fn.write(file)
		my_file = os.path.join(BASE_DIR, 'files/{}-{}'.format(author, myFile.name))

		dataList = cghd.excel.ReadXls(my_file)

		print(str(dataList))

		return HttpResponse(str(dataList).replace("'",'"'))
	else:
		return HttpResponse("get")

def str2int(s):
	print('s: {}'.format(s))
	if s:
		print(1)
		return int(s)
	else:
		print(2)
		return 0

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')

class UserFormLogin(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())