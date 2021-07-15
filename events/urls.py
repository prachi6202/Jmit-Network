from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('',views.EventListView.as_view(),name='list'),
    path('your_events/',views.your_events,name='your_events'),
    path('create/',views.EventCreateView.as_view(),name='create'),
    path('update/<uuid:pk>/',views.EventUpdateView.as_view(),name='update'),
    path('delete/<uuid:pk>/',views.EventDeleteView.as_view(),name='delete')
]
