from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	user = request.user
	http_referer = request.META.get('HTTP_REFERER')
	print('http_referer is {}'.format(http_referer))
	if not http_referer:
		http_referer = "/accounts/login"
	else:
		http_referer = "/accounts/login?next={}".format(http_referer)
	
	return render(request, 'cghd/index.html',{'user':user, 'http_referer':http_referer})

def finduser(request):
	user = User.objects.filter(username=request.GET['username'])	
	if user:
		return HttpResponse("{'code':200,'text':'the account is exists.'}")
	else:
		return HttpResponse("{'code':404,'text':'the account is not exists.'}")

def login(request):
	if request.user.is_authenticated(): 
		return HttpResponseRedirect('/')

	if request.method =="POST":
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
	    
		user = auth.authenticate(username=username, password=password)

		if user is not None and user.is_active:
			auth.login(request, user)
			forward_url = '/'
			if request.GET:
				forward_url = request.GET['next']
			return HttpResponseRedirect(forward_url)
		else:
			message = 'We didn’t recognize that password.'
			return render(request, 'cghd/login2.html', {'message':message})

	else:
		return render(request, 'cghd/login2.html', {})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/index/')

