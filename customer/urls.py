from django.conf.urls import url

from . import views

app_name = 'customer'

urlpatterns = [
    url(r'^$', views.FoodCategoryListView.as_view(), name='category_menu'),
    url(r'^(?P<pk>[-\w]+)/$', views.FoodCategoryDetailView.as_view(), name='food_menu'),
    url(r'^subscript/(?P<pk>[-\w]+)/$', views.SubscriptionDetailView.as_view(), name='sub_detail'),
    url(r'^subscript$', views.SubscriptionCreateView.as_view(), name='subscription'),
    url(r'^orders', views.OrderListView.as_view(), name='orders'),
    url(r'^poll', views.PollView.as_view(), name='poll'),
    url(r'^update', views.update, name='update'),
    url(r'^thankyou', views.EndView.as_view(), name='thank_you'),

]

