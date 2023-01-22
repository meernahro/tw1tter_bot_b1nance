from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("actions/",views.actions,name="actions")
]