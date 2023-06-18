from django.urls import path
from .views import option_chain_view

urlpatterns = [
    path('nifty_option_chain/<int:pk>/', option_chain_view, name='nifty_optionchain_hp'),
]