from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

def upload_location(instance, filename):
    return str(instance.id)+'/'

'''
class User(models.Model):
    POSITIONS = (
        ('RA', 'restaurant_admin'),
        ('KA', 'kitchen_admin'),
        ('DE', 'default')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=2, default='DE', choices=POSITIONS)
'''

class User(AbstractUser):
    POSITIONS = (
        ('RA', 'restaurant_admin'),
        ('KA', 'kitchen_admin'),
        ('DE', 'default')
    )
    position = models.CharField(max_length=2, default='DE', choices=POSITIONS)


class Worker(models.Model):
    positions = {'MCH': 'Master Chef',
                 'CH': 'Chef',
                 'W': 'Waitress',
                 'CA': 'Cashier'}

    name = models.CharField(max_length=100)
    f_name = models.CharField(max_length=100)
    position = models.CharField(positions, max_length=3)
    home_addr = models.CharField(max_length=1000)
    regex_phoneNumber = RegexValidator(regex=r"0(21|26|25|86|24|23|81|28|31|44|11|74|83|51|45|17|41|54|87|71|66|34"
                                             r"|56|13|77|76|61|38|58|35|84)[0-9]+")
    regex_mobileNumber = RegexValidator(regex=r"^(\+98|0)?9\d{9}",
                                        message="""your number isn't correct.
                                        true formats :
                                        1) +989999999999 2)09999999999""")
    # how many times using our service???
    phone_number = models.CharField(max_length=100, validators=[regex_phoneNumber])
    mobile_number = models.CharField(max_length=100, validators=[regex_mobileNumber])
    profile = models.ImageField(blank=False, null=False)
    published_date = models.DateField(default=timezone.now())
    national_code = models.IntegerField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name+" "+self.f_name

    def get_absolute_url(self):
        return reverse('restaurant_admin:Worker_detail', args=[self.id])


class Table(models.Model):
    table_number = models.IntegerField(primary_key=True)
    table_availability = models.BooleanField(default=True)
    reservation_state = models.BooleanField(default=False)

    def __str__(self):
        return str(self.table_number)

    def get_absolute_url(self):
        return reverse('restaurant_admin:Table_detail', args=[self.table_number])


class FoodCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant_admin:FoodCategory_detail', args=[self.id])


class Food(models.Model):
    food_name = models.CharField(unique=True, max_length=100)
    food_details = models.CharField(max_length=1000, blank=True)
    food_availability = models.BooleanField(default=True)
    cost = models.PositiveIntegerField()
    food_category = models.ForeignKey(FoodCategory, related_name='foods', on_delete=models.CASCADE)
    food_img = models.ImageField(blank=False, null=False, upload_to='Food_Images')
    takeaway_price = models.BooleanField(default=True)

    def __str__(self):
        return self.food_name

    def get_absolute_url(self):
        return reverse('restaurant_admin:Food_detail', args=[self.id])


class OrderList(models.Model):
    STATUSES = (
        ('NO', 'Not Ordered'),
        ('CH', 'Changed Order'),
        ('OR', 'Ordered'),
        ('PR', 'Preparing'),
        ('RE', 'Ready'),
        ('DE', 'Delivered'),
    )
    table = models.ForeignKey(Table, related_name="OrderList_Table", on_delete=models.CASCADE, null=True)
    details = models.CharField(max_length=1000, blank=True, null=True)
    takeaway = models.BooleanField(default=False, verbose_name='بیرون‌بر')
    status = models.CharField(max_length=2, default='NO', choices=STATUSES)
    cost = models.PositiveIntegerField(default=0)


class FoodOrder(models.Model):
    food = models.ForeignKey(Food, related_name='ordered_food', on_delete=models.CASCADE)
    number = models.IntegerField()
    order_list = models.ForeignKey(OrderList, related_name='FoodOrder_list', on_delete=models.CASCADE, null=True, blank=True)
    cost = models.PositiveIntegerField()

    def __str__(self):
        return self.food.food_name


class Cost(models.Model):
    tax = models.PositiveIntegerField(default=1)
    service_charge = models.PositiveIntegerField(default=1)
    packaging_cost = models.PositiveIntegerField(default=1)

    def get_absolute_url(self):
        return reverse('restaurant_admin:Cost_detail', args=[self.id])


class Subscription(models.Model):
    sub_id = models.AutoField(primary_key=True, null=False, editable=False, unique=True, verbose_name='کد اشتراک')
    sub_name = models.CharField(max_length=100, verbose_name='نام')
    sub_lastName = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    sub_birthDate = models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')
    sub_address = models.CharField(max_length=1000, verbose_name='آدرس')
    regex_phoneNumber = RegexValidator(regex=r"0(21|26|25|86|24|23|81|28|31|44|11|74|83|51|45|17|41|54|87|71|66|34"
                                             r"|56|13|77|76|61|38|58|35|84)[0-9]+")
    regex_mobileNumber = RegexValidator(regex=r"^(\+98|0)?9\d{9}",
                                        message="""your number isn't correct.
                                        true formats :
                                        1) +989999999999 2)09999999999""")
    sub_phone = models.CharField(max_length=100, validators=[regex_phoneNumber], blank=False, verbose_name='شماره تلفن',
                                 unique=True)
    sub_mobile_phone = models.CharField(max_length=100, validators=[regex_mobileNumber], blank=True,
                                        verbose_name='شماره تلفن همراه')

    def get_absolute_url(self):
        return reverse('customer:sub_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.sub_id)


class Poll(models.Model):
    question = models.CharField(max_length=1000)
    good_response = models.IntegerField(default=0)
    medium_response = models.IntegerField(default=0)
    bad_response = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('restaurant_admin:Poll_detail', args=[self.id])
