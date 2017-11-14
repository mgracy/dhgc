import xlrd
from django.utils import timezone

def ReadXls(excelFile):
	data = xlrd.open_workbook(excelFile)
	table = data.sheets()[0]
	nrows= table.nrows
	ncols = table.ncols

	dataList = []
	dict1 = {}
	header = []

	for i in range(0, nrows):
		if i== 0:
			header = table.row_values(0)

		else:
			rowValues = table.row_values(i)

			for j in range(0,ncols):
				if header[j].replace('\n','').find('日期') >= 0:
					print(rowValues[j])
					if rowValues[j]:
						dict1[header[j].replace('\n','')] ='{}'.format(str(xlrd.xldate.xldate_as_datetime(rowValues[j], data.datemode)))
					else:
						dict1[header[j].replace('\n','')] ='{}'.format(str(timezone.now()))
				else:
					dict1[header[j].replace('\n','')] ='{}'.format(str(rowValues[j]))
			tmpDict = dict1.copy()
			dataList.append(tmpDict)

	return dataList