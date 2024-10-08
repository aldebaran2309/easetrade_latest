from logging import _STYLES
from types import LambdaType
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from matplotlib import figure

# from django.http import HttpResponse
import requests
import json
import pandas as pd
import pandas_datareader as data
from datetime import date

# from tensorflow.python.eager import context
from .models import Stock
from .forms import StockForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Contact
from nsepython import *

# Create your views here.


def index(request):
    from bsedata.bse import BSE

    b = BSE()
    gainer = b.topGainers()
    loser = b.topLosers()

    n50name = nse_get_index_quote("NIFTY 50")["indexName"]
    n50lastPrice = nse_get_index_quote("NIFTY 50")["last"]
    n50_change = (
        float(nse_get_index_quote("NIFTY 50")["last"].replace(",", ""))
        * float(nse_get_index_quote("NIFTY 50")["percChange"])
        / 100
    )
    n50lastchange = round(n50_change, 2)
    n50lastpChange = nse_get_index_quote("NIFTY 50")["percChange"]
    nbname = nse_get_index_quote("NIFTY BANK")["indexName"]
    nblastPrice = nse_get_index_quote("NIFTY BANK")["last"]
    nb_change = (
        float(nse_get_index_quote("NIFTY BANK")["last"].replace(",", ""))
        * float(nse_get_index_quote("NIFTY BANK")["percChange"])
        / 100
    )
    nblastchange = round(nb_change, 2)
    nblastpChange = nse_get_index_quote("NIFTY BANK")["percChange"]
    niname = nse_get_index_quote("NIFTY IT")["indexName"]
    nilastPrice = nse_get_index_quote("NIFTY IT")["last"]
    ni_change = (
        float(nse_get_index_quote("NIFTY IT")["last"].replace(",", ""))
        * float(nse_get_index_quote("NIFTY IT")["percChange"])
        / 100
    )
    nilastchange = round(ni_change, 2)
    nilastpChange = nse_get_index_quote("NIFTY IT")["percChange"]
    nnname = nse_get_index_quote("NIFTY NEXT 50")["indexName"]
    nnlastPrice = nse_get_index_quote("NIFTY NEXT 50")["last"]
    nn_change = (
        float(nse_get_index_quote("NIFTY NEXT 50")["last"].replace(",", ""))
        * float(nse_get_index_quote("NIFTY NEXT 50")["percChange"])
        / 100
    )
    nnlastchange = round(nn_change, 2)
    nnlastpChange = nse_get_index_quote("NIFTY NEXT 50")["percChange"]
    # for t in gainer:
    #     diff1 = t["ltp"]-t["previousPrice"]
    #     diff1 = round(diff1, 2)
    #     t.update({'inrdiff': diff1})

    # for i in loser:
    #     diff = i["previousPrice"] - i["ltp"]
    #     diff = round(diff, 2)
    #     i.update({'inrdiff': diff})

    context = {
        "gainer": gainer,
        "loser": loser,
        "n50name": n50name,
        "n50lastPrice": n50lastPrice,
        "n50lastchange": n50lastchange,
        "n50lastpChange": n50lastpChange,
        "nbname": nbname,
        "nblastPrice": nblastPrice,
        "nblastchange": nblastchange,
        "nblastpChange": nblastpChange,
        "niname": niname,
        "nilastPrice": nilastPrice,
        "nilastchange": nilastchange,
        "nilastpChange": nilastpChange,
        "nnname": nnname,
        "nnlastPrice": nnlastPrice,
        "nnlastchange": nnlastchange,
        "nnlastpChange": nnlastpChange,
    }
    return render(request, "index.html", context)


def prices(request):
    import requests
    import json
    from nsepython import nse_eq
    import plotly.graph_objects as go
    from plotly.offline import plot
    from datetime import date, datetime

    if request.method == "POST":
        ticker = request.POST["ticker"]

        data_nse = nse_eq(ticker)
        companyName = data_nse["info"]["companyName"]
        lastPrice = data_nse["priceInfo"]["lastPrice"]
        dayHigh = data_nse["priceInfo"]["intraDayHighLow"]["max"]
        dayLow = data_nse["priceInfo"]["intraDayHighLow"]["min"]
        high52 = data_nse["priceInfo"]["weekHighLow"]["max"]
        low52 = data_nse["priceInfo"]["weekHighLow"]["min"]
        previousClose = data_nse["priceInfo"]["previousClose"]
        open = data_nse["priceInfo"]["open"]
        pChange = data_nse["priceInfo"]["pChange"]
        change = data_nse["priceInfo"]["change"]
        # totalTradedVolume = data_nse["preOpenMarket"]["totalTradedVolume"]

        symbol = data_nse["info"]["symbol"]
        industry = data_nse["metadata"]["industry"]
        sector = data_nse["industryInfo"]["sector"]
        founded = data_nse["metadata"]["listingDate"]

        # plotly graph

        def candlestick():
            import yfinance as yf

            # Data viz
            import plotly.graph_objs as go

            # Interval required 1 minute
            data = yf.download(tickers=ticker + ".NS", period="1d", interval="1m")
            # declare figure
            fig = go.Figure()
            # Candlestick
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data["Open"],
                    high=data["High"],
                    low=data["Low"],
                    close=data["Close"],
                    name="market data",
                )
            )
            # Add titles
            fig.update_layout(
                title="Candlestick Chart", yaxis_title="Stock Price (INR per Shares)"
            )
            # X-Axes
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=15,
                                label="15m",
                                step="minute",
                                stepmode="backward",
                            ),
                            dict(
                                count=45,
                                label="45m",
                                step="minute",
                                stepmode="backward",
                            ),
                            dict(count=1, label="HTD", step="hour", stepmode="todate"),
                            dict(count=3, label="3h", step="hour", stepmode="backward"),
                            dict(step="all"),
                        ]
                    )
                ),
            )
            candlestick_div = plot(fig, output_type="div")
            return candlestick_div

        # def heatmap():

        #    import calendar
        #    import jugaad_data.nse as nse
        #    import plotly.express as px

        #    stock = nse.stock_df(symbol=ticker, from_date=date(2012,8,1), to_date=datetime.now().date())
        #    stock['M'] = stock['DATE'].dt.month
        #    stock['Y'] = stock['DATE'].dt.year

        #    stock.sort_values('DATE', inplace=True)
        #    stock.reset_index(drop=True, inplace=True)
        #    stock.set_index('DATE', inplace=True)
        #    stock_monthly = stock.resample("M").last()
        #    stock_monthly['Returns'] = (stock_monthly['CLOSE'] - stock_monthly['CLOSE'].shift(1))*100/stock_monthly['CLOSE'].shift(1)
        #    heatmap_ret = pd.pivot_table(stock_monthly, index='Y', columns='M', values=['Returns'])
        #    a1 = heatmap_ret.__array__()
        #    heatmap_ret.columns = [calendar.month_name[i] for i in range(1,13) ]
        #    fig1 = px.imshow(a1,
        #                     labels=dict(x="Months", y="Year", color="Performance"),
        #                     x=heatmap_ret.columns,
        #                     y=['2021','2020','2019','2018','2017','2016','2015','2014','2013','2012'],
        #                     title="Heatmap of "+ticker
        #                 )
        #    fig1.update_xaxes(side="top")
        #    heatmap_div = plot(fig1, output_type='div')
        #    return heatmap_div

    context = {
        "candlestick": candlestick(),
        # 'heatmap':heatmap(),
        "companyName": companyName,
        "lastPrice": lastPrice,
        "dayHigh": dayHigh,
        "dayLow": dayLow,
        "high52": high52,
        "low52": low52,
        "previousClose": previousClose,
        "open": open,
        "pChange": pChange,
        "change": change,
        # 'totalTradedVolume': totalTradedVolume,
        "symbol": symbol,
        "industry": industry,
        "sector": sector,
        "founded": founded,
    }

    return render(request, "prices.html", context)
    # else:
    #     return render(request, 'prices.html', {'ticker': "Enter a Ticker symbol above"})


def add_stock(request):
    uname = request.user
    name = uname.username
    if request.method == "POST":
        stock = Stock()
        username = name
        ticker = request.POST.get("ticker")
        stock.uname = username
        stock.ticker = ticker
        stock.save()
        messages.success(request, ("Stock has been added!"))
        return redirect("add_stock")

    else:
        from nsepython import nse_eq

        data = Stock.objects.filter(uname=name)
        companyName, lastPrice, dayHigh, dayLow = [], [], [], []
        previousClose, open, pChange, change = [], [], [], []

        for i in data:
            sname = i.ticker
            data_nse = nse_eq(sname)
            companyName.append(data_nse["info"]["symbol"])
            lastPrice.append(data_nse["priceInfo"]["lastPrice"])
            dayHigh.append(data_nse["priceInfo"]["intraDayHighLow"]["max"])
            dayLow.append(data_nse["priceInfo"]["intraDayHighLow"]["min"])
            previousClose.append(data_nse["priceInfo"]["previousClose"])
            open.append(data_nse["priceInfo"]["open"])
            pChange.append(round(data_nse["priceInfo"]["pChange"], 2))
            change.append(round(data_nse["priceInfo"]["change"], 2))

        context = {
            "companyName": companyName,
            "lastPrice": lastPrice,
            "dayHigh": dayHigh,
            "dayLow": dayLow,
            "previousClose": previousClose,
            "open": open,
            "pChange": pChange,
            "change": change,
            "data": data,
            # 'ticker':ticker,
        }

    return render(request, "add_stock.html", context)


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted!"))
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, "delete_stock.html", {"ticker": ticker})


def about(request):
    messages.success(request, "welcome to about page")
    return render(request, "about.html")


def desc(request):
    return render(request, "desc.html")


def desc2(request):
    return render(request, "desc2.html")


# def dtree(request):
#     return render(request, 'dtree.html')


def contact(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.desc = desc
        contact.save()
        messages.success(request, " Your query has been successfully submitted")
    return render(request, "contact.html")


# def prediction(request):
#     return render(request,'prediction.html')


def index_learn(request):
    return render(request, "index_learn.html")


def intro_stock_market(request):
    return render(request, "intro_stock_market.html")


def fundamental_analysis(request):
    return render(request, "fundamental_analysis.html")


def technical_analysis(request):
    return render(request, "technical_analysis.html")


def the_need_to_invest(request):
    return render(request, "the_need_to_invest.html")


def regulators(request):
    return render(request, "regulators.html")


def ipo_market(request):
    return render(request, "ipo_market.html")


def the_stock_markets(request):
    return render(request, "the_stock_markets.html")


def jargons(request):
    return render(request, "jargons.html")


def clearing_and_settlement(request):
    return render(request, "clearing_and_settlement.html")


def corporate_actions(request):
    return render(request, "corporate_actions.html")


def intro_fund_analy(request):
    return render(request, "intro_fund_analy.html")


def mindset_investor(request):
    return render(request, "mindset_investor.html")


def read_annual_report(request):
    return render(request, "read_annual_report.html")


def understanding_p_l_1(request):
    return render(request, "understanding_p_l_1.html")


def understanding_p_l_2(request):
    return render(request, "understanding_p_l_2.html")


def understanding_bal_sheet_1(request):
    return render(request, "understanding_bal_sheet_1.html")


def understanding_bal_sheet_2(request):
    return render(request, "understanding_bal_sheet_2.html")


def cashflow_statement(request):
    return render(request, "cashflow_statement.html")


def background(request):
    return render(request, "background.html")


def introducing_tech_analysis(request):
    return render(request, "introducing_tech_analysis.html")


def chart_types(request):
    return render(request, "chart_types.html")


def getting_started_candlesticks(request):
    return render(request, "getting_started_candlesticks.html")


def single_cad_patterns_part1(request):
    return render(request, "single_cad_patterns_part1.html")


def single_cad_patterns_part2(request):
    return render(request, "single_cad_patterns_part2.html")


def single_cad_patterns_part3(request):
    return render(request, "single_cad_patterns_part3.html")


def support_resistance(request):
    return render(request, "support_resistance.html")


def volumes(request):
    return render(request, "volumes.html")


def moving_averages(request):
    return render(request, "moving_averages.html")


def indicators(request):
    return render(request, "indicators.html")


def dow_theory_1(request):
    return render(request, "dow_theory_1.html")


def dow_theory2(request):
    return render(request, "dow_theory2.html")


def news(request):
    api_request = requests.get(
        "https://api.polygon.io/v2/reference/news?limit=10&order=descending&sort=published_utc&ticker=AAPL&published_utc.gte=2021-04-26&apiKey=XL5JZiyXF4aVL6zzsnVpp8jg4gYXp9ta"
    )
    api = json.loads(api_request.content)
    return render(
        request,
        "news.html",
        {
            "api": api,
        },
    )


def handelSignup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        # check for errorneous input
        if len(username) > 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect("index")

        if not username.isalnum():
            messages.error(
                request, " User name should only contain letters and numbers"
            )
            return redirect("index")
        if pass1 != pass2:
            messages.error(request, " Passwords do not match")
            return redirect("index")
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your Account has been successfully created")
        return redirect("index")
    else:
        return HttpResponse("404 - NOT FOUND")


def handelLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginpassword"]
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("index")

    return HttpResponse("404- Not found")

    return HttpResponse("login")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("index")
    return HttpResponse("handelLogout")
