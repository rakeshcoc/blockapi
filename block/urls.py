from django.conf.urls import url,include
from django.urls import path, re_path
from .views import transaction_view,transaction_create,blocks_view,blocklist,sample,loginView,logoutView
app_name = 'block'
urlpatterns = [
path('viewtransaction/<int:pk>/', transaction_view.as_view(), name = "viewtransaction"),
path('viewandcreate/', transaction_create.as_view(), name = "createtransaction"),
path('viewblock/<int:pk>/', blocks_view.as_view(), name = "viewblocks"),
path('blocklist/', blocklist.as_view(), name = "blocklist"),
path('trn_to_block/<int:id>/',sample,name="transmappedblock"),
path('login/',loginView.as_view()),
path('logout/',logoutView.as_view()),
]