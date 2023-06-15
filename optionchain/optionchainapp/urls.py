from django.urls import path
from .views import option_chain_view

urlpatterns = [
    path('option_chain/<int:pk>/', option_chain_view, name='optionchain_hp'),
]