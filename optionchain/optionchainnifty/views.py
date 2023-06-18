from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import JsonResponse
import requests

from datetime import datetime
from home.models import Fyers_Access_Token, Fyers_Auth_Inputs, MCXSymbol, EquitySymbol
from home.fyersapi import FyerApiClass

from .models import Save_PE_Ratio

from datetime import datetime, timedelta

from datetime import datetime, timedelta

def app_detail_model(pk):
    app_model = get_object_or_404(Fyers_Auth_Inputs, user_ass_id=pk)
    client_id = app_model.client_id
    return client_id


def access_token(pk):
    access_token_model = get_object_or_404(Fyers_Access_Token, app_ass_id=pk)
    access_token = access_token_model.auth_code
    return access_token

from django.shortcuts import render
from datetime import datetime, timedelta
import requests

from django.shortcuts import render
from datetime import datetime, timedelta
import requests

def option_chain_view(request, pk):
    client_id = app_detail_model(pk)
    access_token_value = access_token(pk)

    api_methods = FyerApiClass(client_id, access_token_value)

    nifty_symbol = 'NSE:NIFTY50-INDEX'

    quote = api_methods.get_quote(nifty_symbol)
    quote_value = quote
    print(quote)

    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    # Set the request headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)

        # Check if the response was successful (status code 200)
        if response.status_code == 200:
            # Access the JSON data from the response
            json_data = response.json()

            # Extract the option chain data from the JSON
            option_chain_data = json_data["records"]["data"]

            # Create empty lists for storing extracted data
            ce_data = []
            pe_data = []

            # Get the current date
            current_date = datetime.now().date()

            # Calculate the date for next week expiry
            next_week_expiry = current_date + timedelta(days=(7 - current_date.weekday() + 3))

            # Variables to store the sum of change in open interest
            call_change_in_oi_sum = 0
            put_change_in_oi_sum = 0

            # Iterate over the option chain data
            for data in option_chain_data:
                expiry_date = datetime.strptime(data["expiryDate"], "%d-%b-%Y").date()

                # Check if the expiry date is the next week expiry
                if expiry_date == next_week_expiry:
                    if "CE" in data:
                        strike_price = data["strikePrice"]
                        if strike_price % 50 == 0 and strike_price >= quote_value - 500 and strike_price <= quote_value + 500:
                            open_interest = data["CE"]["openInterest"]
                            change_in_open_interest = data["CE"]["changeinOpenInterest"]
                            ce_data.append({
                                "optionType": "CE",
                                "strikePrice": strike_price,
                                "expiryDate": data["expiryDate"],
                                "openInterest": open_interest,
                                "changeInOpenInterest": change_in_open_interest
                            })
                            call_change_in_oi_sum += change_in_open_interest
                    if "PE" in data:
                        strike_price = data["strikePrice"]
                        if strike_price % 50 == 0 and strike_price >= quote_value - 500 and strike_price <= quote_value + 500:
                            open_interest = data["PE"]["openInterest"]
                            change_in_open_interest = data["PE"]["changeinOpenInterest"]
                            pe_data.append({
                                "optionType": "PE",
                                "strikePrice": strike_price,
                                "expiryDate": data["expiryDate"],
                                "openInterest": open_interest,
                                "changeInOpenInterest": change_in_open_interest
                            })
                            put_change_in_oi_sum += change_in_open_interest

            # Sort the extracted data by strike price
            ce_data.sort(key=lambda x: x["strikePrice"])
            pe_data.sort(key=lambda x: x["strikePrice"])

            put_call_ratio = round(float(put_change_in_oi_sum) / float(call_change_in_oi_sum), 2)

            if put_call_ratio > 1.25:
                recommendation = "BUY"
            elif put_call_ratio < 0.75:
                recommendation = "SELL"
            else:
                recommendation = "Market Sideways"

            save_pe_value = Save_PE_Ratio(value=put_call_ratio)
            save_pe_value.save()

            # Create the context dictionary
            context = {
                "ce_option_chain_data": ce_data,
                "pe_option_chain_data": pe_data,
                "next_week_expiry": next_week_expiry.strftime("%d-%b-%Y"),
                "call_change_in_oi_sum": call_change_in_oi_sum,
                "put_change_in_oi_sum": put_change_in_oi_sum,
                "PE_Ratio": put_call_ratio,
                "save_pe_value": save_pe_value,
                "bnf_value": quote_value,
                "recommendation": recommendation,
            }

            # Render the template with the context
            return render(request, 'optionchainnifty/optionchainhomepage.html', context)

        else:
            context = {
                "error": f"Request failed with status code: {response.status_code}"
            }
            return render(request, 'optionchainapp/optionchainhomepage.html', context, status=response.status_code)

    except requests.RequestException as e:
        context = {
            "error": "An error occurred"
        }
        return render(request, 'optionchainapp/optionchainhomepage.html', context, status=500)



# def option_chain_view(request, pk):
#
#
#     client_id = app_detail_model(pk)
#     access_token_value = access_token(pk)
#
#     api_methods = FyerApiClass(client_id, access_token_value)
#
#     bank_nifty_symbol = 'NSE:NIFTYBANK-INDEX'
#
#     quote = api_methods.get_quote(bank_nifty_symbol)
#
#     print(quote)
#
#     url = "https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
#
#     # Set the request headers
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#         "Accept-Language": "en-US,en;q=0.9",
#     }
#
#     try:
#         # Send a GET request to the URL
#         response = requests.get(url, headers=headers)
#
#         # Check if the response was successful (status code 200)
#         if response.status_code == 200:
#             # Access the JSON data from the response
#             json_data = response.json()
#
#             # Extract the option chain data from the JSON
#             option_chain_data = json_data["records"]["data"]
#
#             # Create empty lists for storing extracted data
#             extracted_data = []
#
#             # Get the current date
#             current_date = datetime.now().date()
#
#             # Calculate the date for next week expiry
#             next_week_expiry = current_date + timedelta(days=(7 - current_date.weekday() + 3))
#
#             # Iterate over the option chain data
#             for data in option_chain_data:
#                 expiry_date = datetime.strptime(data["expiryDate"], "%d-%b-%Y").date()
#
#                 # Check if the expiry date is the next week expiry
#                 if expiry_date == next_week_expiry:
#                     if "CE" in data:
#                         strike_price = data["strikePrice"]
#                         open_interest = data["CE"]["openInterest"]
#                         change_in_open_interest = data["CE"]["changeinOpenInterest"]
#                         extracted_data.append({
#                             "strikePrice": strike_price,
#                             "expiryDate": data["expiryDate"],
#                             "openInterest": open_interest,
#                             "changeInOpenInterest": change_in_open_interest
#                         })
#                     if "PE" in data:
#                         strike_price = data["strikePrice"]
#                         open_interest = data["PE"]["openInterest"]
#                         change_in_open_interest = data["PE"]["changeinOpenInterest"]
#                         extracted_data.append({
#                             "strikePrice": strike_price,
#                             "expiryDate": data["expiryDate"],
#                             "openInterest": open_interest,
#                             "changeInOpenInterest": change_in_open_interest
#                         })
#
#             # Create the context dictionary
#             context = {
#                 "option_chain_data": extracted_data,
#                 "next_week_expiry": next_week_expiry.strftime("%d-%b-%Y")
#             }
#
#             # Render the template with the context
#             return render(request, 'optionchainapp/optionchainhomepage.html', context)
#
#         else:
#             context = {
#                 "error": f"Request failed with status code: {response.status_code}"
#             }
#             return render(request, 'optionchainapp/optionchainhomepage.html', context, status=response.status_code)
#
#     except requests.RequestException as e:
#         context = {
#             "error": "An error occurred"
#         }
#         return render(request, 'optionchainapp/optionchainhomepage.html', context, status=500)

# def option_chain_view(request):
#     url = "https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
#
#     # Set the request headers
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#         "Accept-Language": "en-US,en;q=0.9",
#     }
#
#     try:
#         # Send a GET request to the URL
#         response = requests.get(url, headers=headers)
#
#         # Check if the response was successful (status code 200)
#         if response.status_code == 200:
#             # Access the JSON data from the response
#             json_data = response.json()
#
#             # Extract the option chain data from the JSON
#             option_chain_data = json_data["records"]["data"]
#
#             # Create empty lists for storing extracted data
#             extracted_data = []
#
#             # Filter options for the desired expiry date
#             expiry_date = "22-Jun-2023"
#             for data in option_chain_data:
#                 if "CE" in data and data["expiryDate"] == expiry_date:
#                     strike_price = data["strikePrice"]
#                     expiry_date = data["expiryDate"]
#                     open_interest = data["CE"]["openInterest"]
#                     change_in_open_interest = data["CE"]["changeinOpenInterest"]
#                     extracted_data.append({
#                         "strike_price": strike_price,
#                         "expiry_date": expiry_date,
#                         "open_interest": open_interest,
#                         "change_in_open_interest": change_in_open_interest
#                     })
#                 if "PE" in data and data["expiryDate"] == expiry_date:
#                     strike_price = data["strikePrice"]
#                     expiry_date = data["expiryDate"]
#                     open_interest = data["PE"]["openInterest"]
#                     change_in_open_interest = data["PE"]["changeinOpenInterest"]
#                     extracted_data.append({
#                         "strike_price": strike_price,
#                         "expiry_date": expiry_date,
#                         "open_interest": open_interest,
#                         "change_in_open_interest": change_in_open_interest
#                     })
#
#             # Render the HTML template with the filtered data
#             html_content = render(request, 'optionchainapp/optionchainhomepage.html', {'extracted_data': extracted_data}).content.decode("utf-8")
#
#             # Return the rendered HTML content as an AJAX response
#             return JsonResponse({"html_content": html_content})
#
#         else:
#             return JsonResponse({"error": "Request failed with status code"}, status=response.status_code)
#
#     except requests.RequestException as e:
#         return JsonResponse({"error": "An error occurred"}, status=500)