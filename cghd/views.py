from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cghd.models import XlsInfo, Business, Business_Actual
from django.contrib.auth.models import User
import cghd.excel
import os
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import hashlib
import datetime
import logging
# from django.template import RequestContext

# Create your views here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('---------{}'.format(BASE_DIR))
DATE_FORMAT = '%Y-%m-%d'
logger = logging.getLogger(__name__)

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
	if req.method == "POST":
		msg = u"数据保存成功"
		hiddenData = req.POST.get('hiddenData')
		hiddenData = hiddenData.replace(' style="display:none;"','').replace(' class="dbclicktd"','').replace('</td>','').replace('</tr>','').replace('</tbody>','').replace('</table>','')		
		print(hiddenData)
		trs = hiddenData.split('<tr>')
		for i in range(2, len(trs)):
			tr = trs[i].replace('</tr>','')
			tds = tr.split('<td>')
			print(tds)
			print('----------------------------------------')
			Business_Actual(
				Order_No = tds[1],
				Area = tds[2],
				In_Out = tds[3],
				C_Type = tds[4],
				C_ID = tds[5],
				C_BriefName = tds[6],
				Unload_Address = tds[7],
				Unload_Date = tds[8],
				Unload_Time = tds[9],
				S_ID = tds[10],
				S_BriefName = tds[11],
				Source_Address = tds[12],
				Trade_Type = tds[13],
				Gap_Price = tds[14],
				GP_Price = tds[15],
				CG_Price = tds[16],
				Sales_Price = tds[17],
				Transport_Price = tds[18],
				DGL_Price = tds[19],
				Transport_Distance = tds[20],
				DFX_Cost = tds[21],			
				Salesmen = tds[22],
				Create_Date = tds[23],
				State = tds[24],
				Dispatch_Mark = tds[25],
				Create_Ip = get_client_ip(req),
				Create_By = user.username
			).save()
		
		return render(req, 'cghd/salesOrder.html', {'user': user, 'msg': msg})
	else:
		return render(req, 'cghd/salesOrder.html', {'user': user, 'urlPath': req.path})

@login_required
def transportData(req):
	user = req.user
	if req.method == "POST":
		msg = u"维护运输数据成功"
		hiddenData = req.POST.get('hiddenData')		
		hiddenData = hiddenData.replace(' style="display:none;"','').replace(' class="dbclicktd"','').replace('</td>','').replace('</tr>','').replace('</tbody>','').replace('</table>','')
		# print(hiddenData)
		trs = hiddenData.split('<tr>')
		for i in range(2, len(trs)):
			tr = trs[i].replace('</tr>','')
			tds = tr.split('<td>')
			print(tds)
			carrierBriefName = tds[12]
			loadDate = tds[13]
			tractorNo = tds[14]
			tankNo = tds[15]
			driver = tds[16]
			supercargo = tds[17]
			teleNo = tds[18]
			gapPounds = tds[19]
			loadQTY = tds[20]
			unloadQTY = tds[21]
			bid = tds[26]
			logger.debug(u'用户{}修改id={}记录如下:\ncarrierBriefName: {}\tloadDate: {}\ttractorNo: {}\ttankNo: {}\tdriver: {}\tsupercargo: {}\tteleNo: {}\tgapPounds: {}\tloadQTY: {}\tunloadQTY: {}'.format(user.username,bid,carrierBriefName,loadDate,tractorNo,tankNo,driver,supercargo,teleNo,gapPounds,loadQTY,unloadQTY))
			print('----------------------------------------')
			try:
				pass
				Business_Actual.objects.filter(id=bid).update(
					Carrier_BriefName=carrierBriefName,
					Load_Date=loadDate,
					Tractor_No=tractorNo,
					Tank_No=tankNo,
					Driver=driver,
					Supercargo=supercargo,
					Tele_No=teleNo,
					Gap_Pounds=gapPounds,
					Load_QTY=loadQTY,
					Unload_QTY=unloadQTY,
					Update_By=user.username,
					Update_Ip=get_client_ip(req),
					Update_Date=datetime.datetime.now()				
					)
			except Exception as e:
				return HttpResponse('<h1>Error<p style="color:red;">{}</p></h1>'.format(e))	

		return HttpResponse('<h1>{}</h1>'.format(msg))
	else:
		return render(req, 'cghd/transportData.html', {'user': user, 'urlPath': req.path})

@login_required
def changeOrder(req):
	user = req.user
	if req.method == "POST":
		msg = u"变更订单数据成功"
		hiddenData = req.POST.get('hiddenData')		
		hiddenData = hiddenData.replace(' style="display:none;"','').replace(' class="dbclicktd"','').replace('</td>','').replace('</tr>','').replace('</tbody>','').replace('</table>','')
		# print(hiddenData)
		trs = hiddenData.split('<tr>')
		for i in range(2, len(trs)):
			tr = trs[i].replace('</tr>','')
			tds = tr.split('<td>')
			print(tds)
			state = tds[29]
			bid = tds[31]
			logger.debug(u'用户{}修改id={}记录如下:State: {}'.format(user.username,bid,state))
			print('----------------------------------------')
			try:
				pass
				Business_Actual.objects.filter(id=bid).update(					
					State=state,
					Update_By=user.username,
					Update_Ip=get_client_ip(req),
					Update_Date=datetime.datetime.now()				
					)
			except Exception as e:
				return HttpResponse('<h1>Error<p style="color:red;">{}</p></h1>'.format(e))	

		return HttpResponse('<h1>{}</h1>'.format(msg))

	return render(req, 'cghd/changeOrder.html', {'user': user, 'urlPath': req.path})

@login_required
def getOrderInfo(req):
	salesNo = req.GET.get('salesNo')
	area = req.GET.get('area')
	sourceAddress = req.GET.get('sourceAddress')
	unloadDate = req.GET.get('unloadDate')
	salesMen = req.GET.get('salesMen')
	clientType = req.GET.get('clientType')
	salesDate = req.GET.get('salesDate')
	supplier = req.GET.get('supplier')

	sFilter = ""
	# if salesNo:
	# 	sFilter += "Order_No='" + salesNo + "',"
	# if area:
	# 	sFilter += "Area='" + area + "',"
	# if sourceAddress:
	# 	sFilter += "Source_Address='" + sourceAddress + "',"
	# if unloadDate:
	# 	sFilter += "Unload_Date='" + unloadDate + "',"
	# if salesMen:
	# 	sFilter += "Salesmen='" + salesMen + "',"
	# if clientType:
	# 	sFilter += "C_Type='" + clientType + "',"
	# if salesDate:
	# 	sFilter += "Create_Date='" + salesDate + "',"
	# if supplier:
	# 	sFilter += "S_BriefName='" + supplier + "'"	

	print(sFilter)
	print('uuuuuuuuuuuuuuuuuuu')
	# businessLists = Business.objects.filter(Unload_Date=date).filter(Area=area).filter(C_BriefName=clientName)
	businessLists = Business_Actual.objects.all()
	
	if salesNo:
		businessLists = businessLists.filter(Order_No=salesNo)
	if area:
		businessLists = businessLists.filter(Area=area)
	if sourceAddress:
		businessLists = businessLists.filter(Source_Address=sourceAddress)
	if unloadDate:
		businessLists = businessLists.filter(Unload_Date=unloadDate)
	if salesMen:
		businessLists = businessLists.filter(Salesmen=salesMen)
	if clientType:
		businessLists = businessLists.filter(C_Type=clientType)
	if salesDate:
		businessLists = businessLists.filter(Create_Date=salesDate)
	if supplier:
		businessLists = businessLists.filter(S_BriefName=supplier)

	print('len--{}'.format(len(businessLists)))
	print(type(businessLists))
	dataList = []

	for businessList in businessLists:
		data = {}
		data['Order_No'] = str(businessList.Order_No)
		data['In_Out'] = str(businessList.In_Out)
		data['Area'] = str(businessList.Area)
		data['C_ID'] = str(businessList.C_ID)
		data['C_Type'] = str(businessList.C_Type)
		data['C_BriefName'] = str(businessList.C_BriefName)
		data['Unload_Address'] = str(businessList.Unload_Address)
		data['Unload_Date'] = str(businessList.Unload_Date)
		data['Unload_Time'] = str(businessList.Unload_Time)
		data['S_ID'] = str(businessList.S_ID)
		data['S_BriefName'] = str(businessList.S_BriefName)
		data['Source_Address'] = str(businessList.Source_Address)
		data['Carrier_ID'] = str(businessList.Carrier_ID)
		data['Carrier_BriefName'] = str(businessList.Carrier_BriefName)
		data['Gap_Price'] = str(businessList.Gap_Price)
		data['GP_Price'] = str(businessList.GP_Price)
		data['CG_Price'] = str(businessList.CG_Price)
		data['Transport_Price'] = str(businessList.Transport_Price)
		data['DGL_Price'] = str(businessList.DGL_Price)
		data['Transport_Distance'] = str(businessList.Transport_Distance)
		data['Trade_Type'] = str(businessList.Trade_Type)
		data['Load_Date'] = str(businessList.Load_Date)
		data['Tractor_No'] = str(businessList.Tractor_No)
		data['Tank_No'] = str(businessList.Tank_No)
		data['Driver'] = str(businessList.Driver)
		data['Supercargo'] = str(businessList.Supercargo)
		data['Tele_No'] = str(businessList.Tele_No)
		data['Gap_Pounds'] = str(businessList.Gap_Pounds)
		data['Load_QTY'] = str(businessList.Load_QTY)
		data['Unload_QTY'] = str(businessList.Unload_QTY)
		data['Actual_PO_Amount'] = str(businessList.Actual_PO_Amount)
		data['PO_Price'] = str(businessList.PO_Price)
		data['PO_QTY'] = str(businessList.PO_QTY)
		data['Actual_Sales_Amount'] = str(businessList.Actual_Sales_Amount)
		data['Sales_Price'] = str(businessList.Sales_Price)
		data['Sales_QTY'] = str(businessList.Sales_QTY)
		# data['Actual_Logistics_Amount'] = str(businessList.Actual_Logistics_Amount)
		data['Logistics_Price'] = str(businessList.Logistics_Price)
		data['Logistics_QTY'] = str(businessList.Logistics_QTY)
		data['Actual_Logistics_Price'] = str(businessList.Actual_Logistics_Price)
		data['Salesmen'] = str(businessList.Salesmen)
		data['M_Deviation'] = str(businessList.M_Deviation)
		data['D_Deviation'] = str(businessList.D_Deviation)
		data['State'] = str(businessList.State)
		data['Create_Date'] = str(businessList.Create_Date)
		data['Dispatch_Mark'] = str(businessList.Dispatch_Mark)
		data['id'] = str(businessList.id)
		dataList.append(data)

	return HttpResponse(str(dataList).replace("'",'"'))



@login_required
def orderData(req):
	user = req.user
	if req.method == "POST":
		msg = u"维护订单数据成功"
		hiddenData = req.POST.get('hiddenData')		
		hiddenData = hiddenData.replace(' style="display:none;"','').replace(' class="dbclicktd"','').replace('</td>','').replace('</tr>','').replace('</tbody>','').replace('</table>','')
		print(hiddenData)
		print('--------------')
		trs = hiddenData.split('<tr>')
		for i in range(2, len(trs)):
			tr = trs[i].replace('</tr>','')
			tds = tr.split('<td>')
			try:
				fPoQty= int(tds[23])
				fPoPrice= int(tds[24])
				fSalesQty= int(tds[25])
				fSalesPrice= int(tds[26])
				fLogisticsQty= int(tds[27])
				fLogisticsPrice= int(tds[28])
				fMDeviation = fSalesPrice*fSalesQty -fPoPrice*fPoQty -fLogisticsPrice*fLogisticsQty;
				fDDeviation = int(fMDeviation)/int(fSalesQty)
			except Exception as e:
				fPoQty= 0
				fPoPrice= 0
				fSalesQty= 0
				fSalesPrice= 0
				fLogisticsQty= 0
				fLogisticsPrice= 0
				fMDeviation = 0
				fDDeviation = 0;
				logger.debug('fSalesQty: {}, error: {}'.format(fSalesQty, e))		

			bid = tds[33]
			logger.debug(u'用户{}修改id={}'.format(user.username,bid))
			print('----------------------------------------')
			try:
				pass
				Business_Actual.objects.filter(id=bid).update(					
					PO_QTY=fPoQty,
					PO_Price=fPoPrice,
					Sales_QTY=fSalesQty,
					Sales_Price=fSalesPrice,
					Logistics_QTY=fLogisticsQty,
					Logistics_Price=fLogisticsPrice,
					Actual_Logistics_Amount=fLogisticsPrice*fLogisticsQty,
					Actual_Sales_Amount=fSalesPrice*fSalesQty,
					Actual_PO_Amount=fPoPrice*fPoQty,
					M_Deviation=fMDeviation,
					D_Deviation=fDDeviation,					
					Update_By=user.username,
					Update_Ip=get_client_ip(req),
					Update_Date=datetime.datetime.now()				
					)
			except Exception as e:
				return HttpResponse('<h1>Error<p style="color:red;">{}</p></h1>'.format(e))	

		return HttpResponse('<h1>{}</h1>'.format(msg))

	return render(req, 'cghd/orderData.html', {'user': user, 'urlPath': req.path})


@login_required
def basicData(req):
	user = req.user
	return render(req, 'cghd/basicData.html', {'user': user, 'urlPath': req.path})

@login_required
def master(req):
	user = req.user
	return render(req, 'cghd/master.html', {'user': user, 'urlPath': req.path})

@login_required
def creditData(req):
	user = req.user
	return render(req, 'cghd/creditData.html', {'user': user, 'urlPath': req.path})

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
	user = req.user
	return render(req, 'cghd/supplier.html', {'user': user, 'urlPath': req.path})

@login_required
def ar(req):
	user = req.user
	return render(req, 'cghd/ar.html', {'user': user, 'urlPath': req.path})

@login_required
def ap(req):
	return render(req, 'cghd/ap.html', {'user': user, 'urlPath': req.path})

@login_required
def planSchedule(req):
	user = req.user
	return render(req, 'cghd/planSchedule.html', {'user': user, 'urlPath': req.path})

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
	user = req.user
	return render(req, 'cghd/businessFreight.html', {'urlPath': req.path})

@login_required
def businessPurchaseSale(req):
	user = req.user
	return render(req, 'cghd/businessPurchaseSale.html', {'urlPath': req.path})

@login_required
def finGAReport(req):
	user = req.user
	return render(req, 'cghd/finGAReport.html', {'user': user, 'urlPath': req.path})

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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip