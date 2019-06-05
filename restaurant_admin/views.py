from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from . import models
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm,AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.views import View
from . import forms


def is_restaurant_admin(user):
    if user.position == 'RA':
        return True
    else:
        return False

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():

            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('restaurant_admin:login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        print(form.error_messages)

    return render(request, 'restaurant_admin/change_password.html', {
        'form': form
    })

def login(request):
    if request.method =='POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            from django.contrib.auth import authenticate, login
            user_x = models.User.objects.filter(username=form.cleaned_data['username'])
            if len(user_x) !=0:
                if user_x[0].password == form.cleaned_data['password']:
                    if user_x[0].is_active:
                        if user_x[0].position == "RA":
                            login(request,user_x[0])
                            return render(request, 'restaurant_admin/home.html')
                        elif user_x[0].position == "KA":
                            login(request,user_x[0])
                            return render(request, 'kitchen/TableStatelist.html')
                    else:
                        messages.error(request,'حساب کاربری غیر فعال است ')
                        return redirect('restaurant_admin:login')
                else:
                    messages.error(request, 'پسورد یا نام کاربری اشتباه است')
                    return redirect('restaurant_admin:login')

            else:
                messages.error(request,'پسورد یا نام کاربری اشتباه است')
                return redirect('restaurant_admin:login')
        else:
            messages.error(request, 'پسورد یا نام کاربری اشتباه است')
            return redirect('restaurant_admin:login')

    else:
        form = forms.LoginForm()
        return render(request, 'restaurant_admin/login.html', {
            'form': form
        })


@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')
@login_required
def Home(request):
    return render(request,'restaurant_admin/home.html')


class SpecialView(View):

    def get(self,*args,**kwargs):

        self.queryset=self.model.objects.all()
        return render(self.request, self.template_name,context={'object_list':self.queryset,
                                                             'chosen_object': self.chosen_object,
                                                             'update_form': self.update_form,
                                                             'create_form':self.create_form,
                                                             'create_bool':self.create_bool})
    def post(self,*args,**kwargs):
        postvalues = self.request.POST
        print('post values {}'.format(postvalues))
        if postvalues.get('id', None):
            print('id')
            id = self.request.POST.get('id')
            self.chosen_object= self.model.objects.get(pk=id)

        if self.chosen_object != None:
            print('this')
            self.queryset=self.model.objects.all()
            self.update_form=self.form(instance=self.chosen_object)
            return render(self.request,self.template_name,context={'object_list':self.queryset,
                                                                    'chosen_object': self.chosen_object,
                                                                    'update_form': self.update_form})

        if postvalues.get('edit',None):
            print('yes')
            self.chosen_object=self.model.objects.get(pk=postvalues['pk'])
            self.update_form=self.form(self.request.POST,  self.request.FILES,instance=self.chosen_object)
            print(self.update_form)
            if self.update_form.is_valid():
                print('this')
                cost=self.update_form.save()
                cost.save()
                self.queryset= self.model.objects.all()
                return render(self.request,self.template_name,context={'object_list':self.queryset})
            else:
                self.queryset= self.model.objects.all()
                return render(self.request,self.template_name,context={'object_list':self.queryset,
                                                                        'update_form':self.update_form,
                                                                        'chosen_object':self.chosen_object})

        if postvalues.get('create', None):
            self.create_bool=True
            self.create_form=self.form()
            self.queryset= self.model.objects.all()
            return render(self.request,self.template_name,context={'object_list':self.queryset,
                                                                    'create_form':self.create_form,
                                                                    'create_bool':self.create_bool})

        if postvalues.get('create_1',None):
            self.create_form=self.form(self.request.POST, self.request.FILES)
            print(self.create_form.errors)
            print('((((((()))))))')
            print(self.create_form)
            if self.create_form.is_valid():
                print('yes this is valid')
                cost= self.create_form.save()
                cost.save()
                self.queryset= self.model.objects.all()
                return render(self.request,self.template_name,context={'object_list':self.queryset})
            else:
                self.create_bool=True
                self.queryset= self.model.objects.all()

                return render(self.request,self.template_name,context={'object_list':self.queryset,'create_form':self.create_form,
                                                                        'create_bool':self.create_bool})

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')
@method_decorator(login_required, name='dispatch')
class FoodCategoryDetailView(DetailView):
    template_name = 'restaurant_admin/FoodCategorydetail.html'
    model = models.FoodCategory
    fields = '__all__'

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class FoodCategoryHomeDetailView(SpecialView):
    template_name = 'restaurant_admin/FoodCategoryHomedetail.html'
    form=forms.FoodCategoryForm
    model = models.FoodCategory
    fields='__all__'
    create_form= None
    update_form= None
    chosen_object=None
    create_bool = False

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class FoodCategoryDeleteView(DeleteView):
    template_name = 'restaurant_admin/FoodCategorydelete.html'
    model = models.FoodCategory
    fields = '__all__'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('restaurant_admin:FoodCategoryHome_detail')

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class FoodDetailView(DetailView):
    template_name = 'restaurant_admin/Fooddetail.html'
    model = models.Food
    fields = '__all__'

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class FoodHomeDetailView(SpecialView):
    template_name = 'restaurant_admin/FoodHomedetail.html'
    form=forms.FoodForm
    model = models.Food
    fields='__all__'
    chosen_object=None
    update_form=None
    create_bool=False
    create_form=None

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class FoodDeleteView(DeleteView):
    template_name = 'restaurant_admin/Fooddelete.html'
    model = models.Food
    fields = '__all__'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('restaurant_admin:FoodHome_detail')

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class WorkerDetailView(DetailView):
    template_name = 'restaurant_admin/Workerdetail.html'
    model = models.Worker
    fields = '__all__'

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class WorkerHomeDetailView(SpecialView):
    template_name = 'restaurant_admin/WorkerHomedetail.html'
    form=forms.WorkerForm
    model = models.Worker
    fields='__all__'
    chosen_object=None
    update_form=None
    create_bool=False
    create_form=None

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class WorkerDeleteView(DeleteView):
    model = models.Worker
    fields = '__all__'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('restaurant_admin:WorkerHome_detail')

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class TableDetailView(DetailView):
    template_name = 'restaurant_admin/Tabledetail.html'
    model = models.Table
    fields = '__all__'

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class TableHomeDetailView(SpecialView):
    template_name = 'restaurant_admin/TableHomedetail.html'
    form= forms.TableForm
    model = models.Table
    fields='__all__'
    create_form=None
    create_bool = False
    update_form=None
    chosen_object=None

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class TableDeleteView(DeleteView):
    model = models.Table
    fields = '__all__'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('restaurant_admin:TableHome_detail')

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class CostDetailView(DetailView):
    template_name = 'restaurant_admin/Costdetail.html'
    model = models.Cost
    fields = '__all__'

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class CostHomeDetailView(SpecialView):
    template_name = 'restaurant_admin/CostHomedetail.html'
    form= forms.CostForm
    create_form= None
    update_form= None
    chosen_object=None
    create_bool = False
    model = models.Cost
    fields='__all__'

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class CostDeleteView(DeleteView):
    template_name = 'restaurant_admin/Costdelete.html'
    model = models.Cost
    fields = '__all__'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('restaurant_admin:CostHome_detail')

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class PollDetailView(DetailView):
    template_name = 'restaurant_admin/Polldetail.html'
    model = models.Poll
    fields = '__all__'

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class PollHomeDetailView(SpecialView):
    template_name = 'restaurant_admin/PollHomedetail.html'
    form= forms.PollForm
    create_form= None
    update_form= None
    chosen_object=None
    create_bool = False
    model = models.Poll
    fields='__all__'

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@method_decorator(login_required, name='dispatch')
class PollDeleteView(DeleteView):
    template_name = 'restaurant_admin/Polldelete.html'
    model = models.Poll
    fields = '__all__'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('restaurant_admin:PollHome_detail')

@method_decorator(user_passes_test(is_restaurant_admin),name='dispatch')

@login_required
def PollResult(request):
    polls = models.Poll.objects.all()
    return render(request, 'restaurant_admin/pollresult.html',context={'polls':polls})
