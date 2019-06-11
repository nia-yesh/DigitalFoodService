from . import views
from django.conf.urls import url

app_name = 'kitchen'

urlpatterns = [
    url(r'Tables_list', views.TableStateListView.as_view(), name='TableState_list'),
    url(r'Tables_order/<int:pk>/', views.TableOrdersView.as_view(), name='TableOrders'),
    url(r'update', views.update, name='update')
]
