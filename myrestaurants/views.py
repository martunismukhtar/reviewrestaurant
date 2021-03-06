from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import RestaurantReview, Restaurant
from .forms import RestaurantForm

from .Analyzer import Analizer

class LoginRequiredMixin(object):
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class CheckIsOwnerMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(CheckIsOwnerMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

class LoginRequiredCheckIsOwnerUpdateView(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
    template_name = 'myrestaurants/form.html'

class RestaurantDetail(DetailView):
    model = Restaurant
    template_name = 'myrestaurants/restaurant_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        context['RATING_CHOICES'] = RestaurantReview.RATING_CHOICES
        return context

class RestaurantCreate(LoginRequiredMixin, CreateView):
    model = Restaurant
    template_name = 'myrestaurants/form.html'
    form_class = RestaurantForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RestaurantCreate, self).form_valid(form)

@login_required()
def review(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if RestaurantReview.objects.filter(restaurant=restaurant, user=request.user).exists():
        RestaurantReview.objects.get(restaurant=restaurant, user=request.user).delete()

    getrating = request.POST.get('rating', 0)
    rating = 0
    if request.POST['comment'] != None:
        cm = Analizer().proses(request.POST['comment'])
        if getrating == 0:
            rating = 0
        else:
            if cm < 0:
                rating = getrating + int(cm)
            else:
                rating = getrating

    new_review = RestaurantReview(
        rating=rating,
        comment=request.POST['comment'],
        user=request.user,
        restaurant=restaurant)
    new_review.save()

    return HttpResponseRedirect(reverse('myrestaurants:restaurant_detail', args=(restaurant.id,)))