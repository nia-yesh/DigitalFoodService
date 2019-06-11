from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from restaurant_admin.models import *
from .forms import FormOrder
from django.shortcuts import render
from django.views import View


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if 'food_orders_list' not in self.request.session:
            fo_list = []
            self.request.session['food_orders_list'] = fo_list
        fo_list = self.request.session['food_orders_list']
        ordered_foods = FoodOrder.objects.filter(pk__in=fo_list)

        if 'order_list_pk' not in self.request.session:
            ol = OrderList.objects.create()
            self.request.session['order_list_pk'] = ol.pk
        ol_pk = self.request.session['order_list_pk']
        order_list = OrderList.objects.get(pk=ol_pk)

        context['food_order'] = ordered_foods.values()
        context['order_status'] = order_list.status
        context['cat_first_pk'] = FoodCategory.objects.first().pk

        return context

    def post(self, request, *args, **kwargs):
        ol_pk = self.request.session['order_list_pk']
        order_list = OrderList.objects.get(pk=ol_pk)
        order_list.status = "DE"
        order_list.save()
        return HttpResponseRedirect('')


class FoodCategoryListView(ListView):
    model = FoodCategory
    context_object_name = 'categories'
    template_name = 'customer/category_list.html'

    def get_context_data(self, **kwargs):
        context = super(FoodCategoryListView, self).get_context_data(**kwargs)
        if 'food_orders_list' not in self.request.session:
            fo_list = []
            self.request.session['food_orders_list'] = fo_list
        fo_list = self.request.session['food_orders_list']
        ordered_foods = FoodOrder.objects.filter(pk__in=fo_list)

        if 'order_list_pk' not in self.request.session:
            ol = OrderList.objects.create()
            self.request.session['order_list_pk'] = ol.pk
        ol_pk = self.request.session['order_list_pk']
        order_list = OrderList.objects.get(pk=ol_pk)

        context['food_order'] = ordered_foods.values()
        context['order_status'] = order_list.status

        return context


# TODO : clear session and database after pay

# TODO : dont refresh the page after adding or removing food


class FoodCategoryDetailView(DetailView):
    model = FoodCategory
    context_object_name = 'category'
    template_name = 'customer/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FoodCategoryDetailView, self).get_context_data(**kwargs)
        # del self.request.session['order_list_pk']
        if 'food_orders_list' not in self.request.session:
            fo_list = []
            self.request.session['food_orders_list'] = fo_list
        fo_list = self.request.session['food_orders_list']
        ordered_foods = FoodOrder.objects.filter(pk__in=fo_list)

        if 'order_list_pk' not in self.request.session:
            ol = OrderList.objects.create()
            self.request.session['order_list_pk'] = ol.pk
        ol_pk = self.request.session['order_list_pk']
        order_list = OrderList.objects.get(pk=ol_pk)

        context['food_order'] = ordered_foods.values()
        context['ordered'] = ordered_foods.values_list('food', flat=True).distinct()
        context['order_status'] = order_list.status
        context['categories'] = FoodCategory.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('addFood'):
            food_pk = request.POST.get('food_pk')
            food = Food.objects.get(pk=food_pk)

            if 'food_orders_list' not in self.request.session:
                fo_list = []
                self.request.session['food_orders_list'] = fo_list
            fo_list = self.request.session['food_orders_list']
            ordered_foods = FoodOrder.objects.filter(pk__in=fo_list)

            try:
                ordered_foods = ordered_foods.get(food=food)
                ordered_foods.number = ordered_foods.number + 1
                ordered_foods.cost = ordered_foods.cost + food.cost
                ordered_foods.save()
            except ObjectDoesNotExist:
                food_order = FoodOrder(food=food, number=1, cost=food.cost)
                food_order.save()
                fo_list.append(food_order.pk)
                self.request.session['food_orders_list'] = fo_list

            return HttpResponseRedirect(self.request.path_info)

        if request.POST.get('removeFood'):
            food_pk = request.POST.get('food_pk')
            food = Food.objects.get(pk=food_pk)

            if 'food_orders_list' not in self.request.session:
                fo_list = []
                self.request.session['food_orders_list'] = fo_list
            fo_list = self.request.session['food_orders_list']
            ordered_foods = FoodOrder.objects.filter(pk__in=fo_list)

            try:
                ordered_foods = ordered_foods.get(food=food)
                if ordered_foods.number == 1:
                    fo_list.remove(ordered_foods.pk)
                    self.request.session['food_orders_list'] = fo_list
                    ordered_foods.delete()
                else:
                    ordered_foods.number = ordered_foods.number - 1
                    ordered_foods.cost = ordered_foods.cost - food.cost
                    ordered_foods.save()
            except ObjectDoesNotExist:
                pass

            return HttpResponseRedirect('')

        return HttpResponseRedirect('')


class OrderListView(FormMixin, ListView):
    model = OrderList
    template_name = 'customer/order_list.html'
    form_class = FormOrder

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        if 'food_orders_list' not in self.request.session:
            fo_list = []
            self.request.session['food_orders_list'] = fo_list
        fo_list = self.request.session['food_orders_list']
        ordered_foods = FoodOrder.objects.filter(pk__in=fo_list)

        if 'order_list_pk' not in self.request.session:
            ol = OrderList.objects.create()
            self.request.session['order_list_pk'] = ol.pk
        ol_pk = self.request.session['order_list_pk']
        order_list = OrderList.objects.get(pk=ol_pk)

        context['food_order'] = ordered_foods.values()
        context['ordered_foods'] = ordered_foods
        context['ordered'] = ordered_foods.values_list('food', flat=True).distinct()
        context['order_status'] = order_list.status

        cost_vals = Cost.objects.get(pk=1)
        food_costs = ordered_foods.values_list('cost', flat=True).distinct()
        food_numbers = ordered_foods.values_list('number', 'food').distinct()

        total_food_costs = 0
        for cost in food_costs:
            total_food_costs += cost

        n = 0
        for item in food_numbers:
            if Food.objects.get(pk=item[1]).takeaway_price:
                n += item[0]

        packaging_charge = cost_vals.packaging_cost * n
        tax = cost_vals.tax * total_food_costs / 100
        service_charge = cost_vals.service_charge * total_food_costs / 100

        context['packaging_charge'] = packaging_charge
        context['tax'] = tax
        context['service_charge'] = service_charge
        context['total_food_cost'] = total_food_costs
        context['total_cost_wt'] = total_food_costs + service_charge + tax + packaging_charge
        context['total_cost_nt'] = total_food_costs + service_charge + tax
        context['cat_first_pk'] = FoodCategory.objects.first().pk

        self.request.session['total_cost_wt'] = total_food_costs + service_charge + tax + packaging_charge
        self.request.session['total_cost_nt'] = total_food_costs + service_charge + tax
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('addFood'):

            food_pk = request.POST.get('food_pk')
            food = Food.objects.get(pk=food_pk)

            if 'food_orders_list' not in self.request.session:
                fo_list = []
                self.request.session['food_orders_list'] = fo_list
            fo_list = self.request.session['food_orders_list']
            ordered_foods = FoodOrder.objects.filter(pk__in=fo_list)

            try:
                ordered_foods = ordered_foods.get(food=food)
                ordered_foods.number = ordered_foods.number + 1
                ordered_foods.cost = ordered_foods.cost + food.cost
                ordered_foods.save()
            except ObjectDoesNotExist:
                food_order = FoodOrder(food=food, number=1, cost=food.cost)
                food_order.save()
                fo_list.append(food_order.pk)
                self.request.session['food_orders_list'] = fo_list

            return HttpResponseRedirect('')

        if request.POST.get('removeFood'):
            food_pk = request.POST.get('food_pk')
            food = Food.objects.get(pk=food_pk)

            if 'food_orders_list' not in self.request.session:
                fo_list = []
                self.request.session['food_orders_list'] = fo_list
            fo_list = self.request.session['food_orders_list']
            ordered_foods = FoodOrder.objects.filter(pk__in=fo_list)

            try:
                ordered_foods = ordered_foods.get(food=food)
                if ordered_foods.number == 1:
                    fo_list.remove(ordered_foods.pk)
                    self.request.session['food_orders_list'] = fo_list
                    ordered_foods.delete()
                else:
                    ordered_foods.number = ordered_foods.number - 1
                    ordered_foods.cost = ordered_foods.cost - food.cost
                    ordered_foods.save()
            except ObjectDoesNotExist:
                pass

            return HttpResponseRedirect('')

        if request.POST.get('order'):
            form = FormOrder(request.POST)

            if 'order_list_pk' not in self.request.session:
                ol = OrderList.objects.create()
                self.request.session['order_list_pk'] = ol.pk
            ol_pk = self.request.session['order_list_pk']
            order_list = OrderList.objects.get(pk=ol_pk)
            table = Table.objects.get(pk=form['tables'].value())

            if 'food_orders_list' not in self.request.session:
                fo_list = []
                self.request.session['food_orders_list'] = fo_list
            fo_list = self.request.session['food_orders_list']
            ordered_foods = FoodOrder.objects.filter(pk__in=fo_list)

            order_list_food_orders = order_list.FoodOrder_list.all()

            for order in order_list_food_orders:
                if order not in ordered_foods:
                    order.delete()

            for order in ordered_foods:
                try:
                    of = order_list_food_orders.get(food=order.food)
                    of.delete()
                except ObjectDoesNotExist:
                    pass
                tmp = FoodOrder(food=order.food, number=order.number, cost=order.cost)
                tmp.order_list = order_list
                tmp.save()

            order_list.details = form['details'].value()
            order_list.takeaway = form['takeaway'].value()
            if order_list.takeaway:
                order_list.cost = self.request.session['total_cost_wt']
            else:
                order_list.cost = self.request.session['total_cost_nt']

            if order_list.status == 'NO':
                order_list.status = 'OR'
            elif order_list.status == 'OR' or order_list.status == 'CH':
                order_list.status = 'CH'
                old_table = Table.objects.get(pk=order_list.table.pk)
                old_table.table_availability = True
                old_table.save()

            order_list.table = table

            table.table_availability = False
            table.save()
            order_list.save()
            return redirect('index')

        return HttpResponseRedirect('')


class SubscriptionDetailView(DetailView):
    model = Subscription
    context_object_name = 'sub'
    template_name = 'customer/subscription_detail.html'


class SubscriptionCreateView(CreateView):
    model = Subscription
    template_name = 'customer/subscription_create.html'
    fields = ('sub_name', 'sub_lastName', 'sub_birthDate', 'sub_address', 'sub_phone', 'sub_mobile_phone')


class PollView(View):
    model = Poll
    template_name = 'customer/poll.html'

    def get(self, request, *args, **kwargs):
        polls = self.model.objects.all()
        questions_arr = []
        for p in polls:
            questions_arr.append(p.pk)
        questions_arr = questions_arr
        print(type(questions_arr))
        return render(request, self.template_name, context={'questions': polls,
                                                            'questions_arr': questions_arr})

    def post(self, request, *args, **kwargs):
        postvalues = self.request.POST
        poll_tuple = []
        poll_list = []
        for post in postvalues:
            if "question" in post:
                poll_tuple = [post.split('_')[1], postvalues[post], None]
                poll_list.append(poll_tuple)
            if "state" in post:
                for tu in poll_list:
                    if tu[0] == post.split('_')[1]:
                        tu[2] = postvalues[post]
                        break

        for post in poll_list:
            if post[2] is None:
                return HttpResponseRedirect('')

        for post in poll_list:
            poll = self.model.objects.get(pk=int(post[0]))
            if tu[2] == "good":
                poll.good_response = poll.good_response + 1
            elif tu[2] == "medium":
                poll.medium_response = poll.medium_response + 1
            elif tu[2] == "bad":
                poll.bad_response = poll.bad_response + 1
            poll.save()

            return redirect('customer:thank_you')


class EndView(TemplateView):
    template_name = 'customer/end.html'

    def get_context_data(self, **kwargs):
        ol_pk = self.request.session['order_list_pk']
        order_list = OrderList.objects.get(pk=ol_pk)
        table = Table.objects.get(pk=order_list.table.pk)
        table.table_availability = True
        table.save()
        order_list.delete()
        self.request.session.flush()


def update(request):
    if 'order_list_pk' not in request.session:
        ol = OrderList.objects.create()
        request.session['order_list_pk'] = ol.pk
    ol_pk = request.session['order_list_pk']
    order_list = OrderList.objects.get(pk=ol_pk)
    diction = {'status': order_list.status}
    import json
    from django.http import JsonResponse
    return JsonResponse({'status': json.dumps(diction)})
