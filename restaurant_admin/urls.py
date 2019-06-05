from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    #path(r'login/', auth_views.LoginView.as_view(template_name='restaurant_admin/login.html', name='login'),
    path(r'login/', views.login, name='login'),
    path(r'change_password/', views.change_password, name='change_password'),
    path(r'logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(r'Home/', views.Home, name='admin_home'),

    path(r'FoodCategory_delete/<int:pk>', views.FoodCategoryDeleteView.as_view(), name='FoodCategory_delete'),
    path(r'FoodCategory_detail/<int:pk>/', views.FoodCategoryDetailView.as_view(), name='FoodCategory_detail'),
    path(r'FoodCategoryHome_detail', views.FoodCategoryHomeDetailView.as_view(), name='FoodCategoryHome_detail'),

    path(r'Food_delete/<int:pk>/', views.FoodDeleteView.as_view(), name='Food_delete'),
    path(r'Food_detail/<int:pk>/', views.FoodDetailView.as_view(), name='Food_detail'),

    path(r'FoodHome_detail', views.FoodHomeDetailView.as_view(), name='FoodHome_detail'),

    path(r'Worker_delete/<int:pk>/', views.WorkerDeleteView.as_view(), name='Worker_delete'),
    path(r'Worker_detail/<int:pk>/', views.WorkerDetailView.as_view(), name='Worker_detail'),
    path(r'WorkerHome_detail', views.WorkerHomeDetailView.as_view(), name='WorkerHome_detail'),

    path(r'Table_delete/<int:pk>/', views.TableDeleteView.as_view(), name='Table_delete'),
    path(r'Table_detail/<int:pk>/', views.TableDetailView.as_view(), name='Table_detail'),
    path(r'TableHome_detail', views.TableHomeDetailView.as_view(), name='TableHome_detail'),

    path(r'Cost_detail/<int:pk>/', views.CostDetailView.as_view(), name='Cost_detail'),
    path(r'Cost_delete/<int:pk>/', views.CostDeleteView.as_view(), name='Cost_delete'),
    path(r'CostHome_detail', views.CostHomeDetailView.as_view(), name='CostHome_detail'),

    path(r'Poll_detail/<int:pk>/', views.PollDetailView.as_view(), name='Poll_detail'),
    path(r'Poll_delete/<int:pk>/', views.PollDeleteView.as_view(), name='Poll_delete'),
    path(r'PollHome_detail',views.PollHomeDetailView.as_view(), name='PollHome_detail'),
    path(r'Poll_result',views.PollResult, name='Poll_result'),
]
