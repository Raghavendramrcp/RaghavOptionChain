from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import JsonResponse
import requests

from datetime import datetime
from home.models import Fyers_Access_Token, Fyers_Auth_Inputs, MCXSymbol, EquitySymbol
from home.fyersapi import FyerApiClass

from .models import Save_PE_Ratio



import datetime

from django.utils import timezone
from datetime import datetime, time

from datetime import *

from django.shortcuts import render
from datetime import datetime, timedelta
import requests


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse


def app_detail_model(pk):
    app_model = get_object_or_404(Fyers_Auth_Inputs, user_ass_id=pk)
    client_id = app_model.client_id
    return client_id


def access_token(pk):
    access_token_model = get_object_or_404(Fyers_Access_Token, app_ass_id=pk)
    access_token = access_token_model.auth_code
    return access_token

def indexcandlestickchart_view():
    client_id = app_detail_model(pk)
    access_token_value = access_token(pk)

    api_methods = FyerApiClass(client_id, access_token_value)

    bank_nifty_symbol = 'NSE:NIFTYBANK-INDEX'
    fin_nifty_symbol = 'NSE:NIFTYFINSRV2550-INDEX'
    nifty_symbol = 'NSE:NIFTY50-INDEX'

    bnf_quote = api_methods.get_quote(bank_nifty_symbol)
    bnf_quote_value = bnf_quote

    finnifty_quote = api_methods.get_quote(fin_nifty_symbol)
    finnifty_quote_value = finnifty_quote

    nifty_quote = api_methods.get_quote(nifty_quote)
    nifty_quote_value = nifty_quote

    data_ce = {
    "symbol": bank_nifty_symbol_ce,
    "resolution": "15",
    "date_format": "1",
    "range_from": "2023-06-27",
    "range_to": "2023-06-27",
    "cont_flag": "1"
    }
    