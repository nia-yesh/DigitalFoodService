from django.contrib import admin
from .models import Poll, Cost, FoodOrder, Food, FoodCategory, OrderList, Table, Subscription, Worker, User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Food)
admin.site.register(FoodCategory)
admin.site.register(FoodOrder)
admin.site.register(OrderList)
admin.site.register(Table)
admin.site.register(Subscription)
admin.site.register(Worker)
admin.site.register(Cost)
admin.site.register(Poll)
admin.site.register(User)
