from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cghd.models import XlsInfo
from django.contrib.auth.models import User
import cghd.excel
import os
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# from django.template import RequestContext

# Create your views here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('---------{}'.format(BASE_DIR))

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
		file = req.FILES['upfile'].name

		excelFile = os.path.join(BASE_DIR, file)
		dataList = cghd.excel.ReadXls(excelFile)

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
		file = req.FILES['upfile'].name

		excelFile = os.path.join(BASE_DIR, file)
		dataList = cghd.excel.ReadXls(excelFile)

		print(str(dataList))

		return HttpResponse(str(dataList).replace("'",'"'))
	else:
		return HttpResponse("get")

@csrf_exempt
def uploadAr(req):
	if req.method == "POST":
		file = req.FILES['upfile'].name

		excelFile = os.path.join(BASE_DIR, file)
		dataList = cghd.excel.ReadXls(excelFile)

		print(str(dataList))

		return HttpResponse(str(dataList).replace("'",'"'))
	else:
		return HttpResponse("get")

@csrf_exempt
def uploadAp(req):
	if req.method == "POST":
		file = req.FILES['upfile'].name

		excelFile = os.path.join(BASE_DIR, file)
		dataList = cghd.excel.ReadXls(excelFile)

		print(str(dataList))

		return HttpResponse(str(dataList).replace("'",'"'))
	else:
		return HttpResponse("get")

def uploadedFile(req):
	if req.method == "POST":
		file = req.FILES['upfile'].name

		excelFile = os.path.join(BASE_DIR, file)
		dataList = cghd.excel.ReadXls(excelFile)

		print(str(dataList))

		return HttpResponse(str(dataList).replace("'",'"'))
	else:
		return HttpResponse("get")

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')

class UserFormLogin(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())