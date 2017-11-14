from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import hashlib
from disk.models import FileInfo
from django.utils import timezone
import os
import json

# Create your views here.

def index(request):
	return render(request, 'disk/index.html')

def upload(request):
	if request.method == "POST":
		myFile = request.FILES.get('upfile')
		if not myFile:
			return HttpResponse('no file is uploaded')

		file = myFile.read()
		if not file:
			return HttpResponse('The file is not exists')

		md5 = hashlib.md5(file).hexdigest()
		filename = myFile.name
		filesize = myFile.size
		fileInfo = FileInfo.objects.filter(md5=md5)
		user_ip = get_client_ip(request)
		now = timezone.localtime(timezone.now())

		if not fileInfo:
			try:
				with open('disk/files/{}'.format(md5), 'wb') as fn:
					fn.write(file)
					print('try: files/disk')
			except Exception as e:
				THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
				my_file = os.path.join(THIS_FOLDER, 'files/{}'.format(md5))
				print('except-before: /files/disk')
				with open(my_file, 'wb') as fn:
					fn.write(file)
					print('except-after: /files/disk')
			else:
				print('no exception: 666')
			finally:
				print('finally: 886')

		print('now is {}'.format(now))
		FileInfo(name=filename,size=filesize,md5=md5,created_date= now, user_ip=user_ip).save()
		return HttpResponseRedirect('/disk/s/{}'.format(md5))
	else:
		return HttpResponse('GET')


def download_list(request, md5):
	fileInfo = FileInfo.objects.filter(md5=md5)
	if not fileInfo:
		return render(request, 'disk/error_404.html')

	files = {
		'name': fileInfo[0].name,
		'size': fileInfo[0].size,
		'downloads': fileInfo[0].downloads,
		'created_date': fileInfo[0].created_date.strftime('%Y-%m-%d %H:%M:%S'),
		'url':'/disk/files/{}'.format(fileInfo[0].name)
	}

	print(files)
	return render(request, 'disk/uploadfiles.html', {'files': files})

def download_detail(request):
	referer = request.META.get('HTTP_REFERER')	
	if not referer:
		return render(request, 'disk/error_404.html')

	md5 = referer[-32:]
	fileinfo = FileInfo.objects.filter(md5=md5)
	if not fileinfo:
		return render(request, 'disk/error_404.html')

	file = None
	try:
		file = open('files/{}'.format(md5), 'rb').read()
	except Exception as e:
		THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
		my_file = os.path.join(THIS_FOLDER, 'files/{}'.format(md5))
		file = open(my_file, 'rb').read()		
	else:
		pass
	finally:
		pass

	fileinfo[0].downloads = fileinfo[0].downloads + 1
	fileinfo[0].save()
	response=HttpResponse(file)
	response['Content-type'] = 'application/octet-stream'
	return response

def search(request):
	ip = get_client_ip(request)
	name = request.GET.get('kw', '')
	fileInfo = FileInfo.objects.filter(name__contains=name)
	if not fileInfo:
		return HttpResponse('[]')

	fileinfoLen = len(fileInfo)
	fileinfoList = []

	for x in range(0,fileinfoLen):
		files = {
			"ip": fileInfo[0].user_ip,
			"name":fileInfo[0].name,
			"size":fileInfo[0].size,
			"downloads":fileInfo[0].downloads,
			"created_date": fileInfo[0].created_date.strftime('%Y-%m-%d %H:%M:%S'),
			"url":"/disk/files/{}".format(fileInfo[0].name)
		}
		fileinfoList.append(files)

	return HttpResponse(str(fileinfoList))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip