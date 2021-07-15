from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)
from . import models
from .forms import eventForm
# Create your views here.
from django.db.models import Q
import datetime
# def cn(request):
#     n=models.event.objects.filter(Q(club_name__username__contains=request.user.username))
#     return n

def your_events(request):

    n=models.event.objects.filter(Q(club_name__username__contains=request.user.username))
    x=list(n)
    x.reverse()
    return render(request,'events/your_events.html',{'n':x})

class EventListView(ListView):
    model = models.event
    ordering = ['-date_created']
    paginate_by = 4

class EventCreateView(CreateView):

    model = models.event
    form_class = eventForm

    def form_valid(self, form):
        form.instance.club_name = self.request.user
        return super().form_valid(form)


class EventUpdateView(UpdateView):

    model = models.event
    form_class = eventForm
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     a=cn()
    #     context['a'] =a
    #     return context

class EventDeleteView(DeleteView):
    model = models.event
    success_url = reverse_lazy("events:list")
