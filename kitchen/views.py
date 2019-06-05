from django.shortcuts import render
from restaurant_admin import models
from django.views.generic.base import TemplateView
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,user_passes_test


def is_kitchen_admin(user):
    if user.position == 'KA':
        return True
    else:
        return False

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_kitchen_admin),name='dispatch')
class TableStateListView(View):
    template_name = 'kitchen/TableStatelist.html'
    model = models.Table
    fields = '__all__'
    chosen_object = None
    queryset = models.Table.objects.all()

    def get(self, *args, **kwargs):
        self.queryset = self.model.objects.all()
        return render(self.request, 'kitchen/TableStatelist.html', context={'object_list': self.queryset,
                                                                            'chosen_object': self.chosen_object})

    def post(self, *args, **kwargs):
        postvalues = self.request.POST
        print(postvalues)
        if postvalues.get('table_id', None):
            print('yes')
            id = self.request.POST.get('table_id')
            self.chosen_object = self.model.objects.get(pk=id)
            self.queryset = self.model.objects.all()
        return render(self.request, 'kitchen/TableStatelist.html', context={'object_list': self.queryset,
                                                                            'chosen_object': self.chosen_object})


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_kitchen_admin),name='dispatch')

class TableOrdersView(TemplateView):
    template_name = 'kitchen/TableOrders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_list = models.Table.objects.get(pk=kwargs['pk']).OrderList_Table.all()
        context['order_list'] = order_list

        return context
