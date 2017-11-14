from django.conf.urls import url
from . import views

urlpatterns = [	
	url(r'^$', views.index, name='index'),
	url(r'^upload/$', views.uploadFile),
	url(r'^basicdata/$', views.basicData),
	# 业务主数据
	url(r'^master/$', views.master),
	url(r'^uploads/$', views.uploadedFile),
	url(r'^supplier/$', views.supplier),
	url(r'^uploadSupplier/$', views.uploadSupplier),
	url(r'^uploadMaster/$', views.uploadMaster),
	url(r'^uploadFile/$', views.uploadFile),
	url(r'^ar/$', views.ar),
	url(r'^ap/$', views.ap),
	url(r'^planschedule/$', views.planSchedule),
	url(r'^businessfreight/$', views.businessFreight),
	url(r'^businesspurchasesale/$', views.businessPurchaseSale),
	url(r'^fingareport/$', views.finGAReport),
	url(r'^loadunload/$', views.loadUnload),
	# url(r'^login/$', views.login, name='login'),
	# url(r'^upload/$', views.upload_file, name='upload'),
	# url(r'^logout/$', views.logout_user, name='logout'),
]