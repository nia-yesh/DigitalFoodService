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
        if postvalues.get('statustoPR', None):
            orederl_id = self.request.POST.get('statustoPR')
            orderl = models.OrderList.objects.get(pk=orederl_id)
            orderl.status = 'PR'
            orderl.save()
            self.chosen_object = self.model.objects.get(pk=orderl.table.pk)
            self.queryset = self.model.objects.all()

        if postvalues.get('statustoRE', None):
            orederl_id = self.request.POST.get('statustoRE')
            orderl = models.OrderList.objects.get(pk=orederl_id)
            orderl.status = 'RE'
            orderl.save()
            self.chosen_object = self.model.objects.get(pk=orderl.table.pk)
            self.queryset = self.model.objects.all()

        if postvalues.get('table_id', None):
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


def update(request):
    results = models.Table.objects.all()
    result_list =[]
    temp_dict = {}
    for table in results:
        if len(table.OrderList_Table.all()) != 0:
            temp_dict = {'table_number':table.table_number,
                         'table_availability': table.table_availability,
                         'table_status': table.OrderList_Table.all()[0].status}
        else:
            temp_dict = {'table_number': table.table_number,
                         'table_availability': table.table_availability,
                         'table_status': "NO"}
        result_list.append(temp_dict)
        temp_dict = {}
    import json
    from django.http import JsonResponse
    return JsonResponse({'object_list': json.dumps(result_list)})
