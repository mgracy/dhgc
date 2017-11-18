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
import datetime
# from django.template import RequestContext

# Create your views here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('---------{}'.format(BASE_DIR))
DATE_FORMAT = '%Y-%m-%d'

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
def salesOrder(req):
	user = req.user
	return render(req, 'cghd/salesOrder.html', {'user': user})

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
def planScheduleQuery(req):
	date = req.GET.get('date')
	area = req.GET.get('area')
	clientName = req.GET.get('clientName')
	businessLists = Business.objects.filter(Unload_Date=date).filter(Area=area).filter(C_BriefName=clientName)
	print('len--{}'.format(len(businessLists)))
	print(type(businessLists))
	dataList = []
	data = {}
	for businessList in businessLists:
		data['订单号'] = str(businessList.Order)
		data['内外部'] = str(businessList.In_Out)
		data['所属区域'] = str(businessList.Area)
		data['客户ID'] = str(businessList.C_ID)
		data['客户名称'] = str(businessList.C_BriefName)
		data['卸气地'] = str(businessList.Unload_Address)
		data['卸货日期'] = str(businessList.Unload_Date)
		data['供应商ID'] = str(businessList.S_ID)
		data['供应商'] = str(businessList.S_BriefName)
		data['气源地'] = str(businessList.Source_Address)
		data['承运商ID'] = str(businessList.Carrier_ID)
		data['承运公司'] = str(businessList.Carrier_BriefName)
		data['票制'] = str(businessList.Trade_Type)
		data['装货日期'] = str(businessList.Load_Date)
		data['牵引车号'] = str(businessList.Tractor_No)
		data['槽车号'] = str(businessList.Tank_No)
		data['驾驶员'] = str(businessList.Driver)
		data['押运员'] = str(businessList.Supercargo)
		data['手机号'] = str(businessList.Tele_No)
		data['状态'] = str(businessList.State)
		data['操作日期'] = str(businessList.Update_Date)
		data['装气量（吨）'] = str(businessList.Load_QTY)
		data['卸气量（吨）'] = str(businessList.Unload_QTY)
		data['调度备注'] = str(businessList.Dispatch_Mark)
		data['电商号'] = str(businessList.Electricity_Amount)
		data['销售结算量（吨）'] = str(businessList.Sales_QTY)
		data['采购结算量（吨）'] = str(businessList.PO_QTY)
		data['物流结算量（吨）'] = str(businessList.Logistics_QTY)
		data['销售价格函'] = str(businessList.Sales_Price_Letter)
		data['销售单价'] = str(businessList.Sales_Price)
		data['销售金额'] = str(businessList.Sales_Amount)
		data['客户核对'] = str(businessList.Customer_CheckDate)
		data['是否开票'] = str(businessList.Customer_IsBilling)
		data['采购价格函'] = str(businessList.PO_Price_Letter)
		data['采购单价'] = str(businessList.PO_Price)
		data['采购金额'] = str(businessList.PO_Amount)
		data['供应商核对'] = str(businessList.Supplier_CheckDate)
		data['是否开票'] = str(businessList.Supplier_IsBilling)
		data['物流价格函'] = str(businessList.Logistics_Price_Letter)
		data['运输单价'] = str(businessList.Logistics_Price)
		data['运费金额'] = str(businessList.Logistics_Amount)
		data['承运商核对'] = str(businessList.Logistics_CheckDate)
		data['是否开票'] = str(businessList.Logistics_IsBilling)
		data['毛差'] = str(businessList.M_Deviation)
		data['吨毛差'] = str(businessList.D_Deviation)
		dataList.append(data)

	return HttpResponse(str(dataList).replace("'",'"'))

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

		print(str(dataList))
		i = 0
		print('Now, we are going to save the dataList to db...')
		for data in dataList:
			print(u'订单号: {}'.format(data['订单号']))
			Business(Order = data['订单号'],
				In_Out = data['内外部'],
				Area = data['所属区域'],
				C_ID = data['客户ID'],
				C_BriefName = data['客户名称'],
				Unload_Address = data['卸气地'],
				Unload_Date = datetime.datetime.strptime(data['卸货日期'], DATE_FORMAT).date(),
				S_ID = data['供应商ID'],
				S_BriefName = data['供应商'],
				Source_Address = data['气源地'],
				Carrier_ID = data['承运商ID'],
				Carrier_BriefName = data['承运公司'],
				Trade_Type = data['票制'],
				Load_Date = datetime.datetime.strptime(data['装货日期'], DATE_FORMAT).date(),
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