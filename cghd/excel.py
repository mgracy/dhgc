import xlrd

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
				dict1[header[j].replace('\n','')] ='{}'.format(str(rowValues[j]))
			tmpDict = dict1.copy()
			dataList.append(tmpDict)

	return dataList