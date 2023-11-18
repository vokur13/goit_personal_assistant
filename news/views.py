import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


url = "https://www.ukr.net/news/"
url_bank = "https://api.privatbank.ua/p24api/exchange_rates?date="
url_weather = "https://ua.sinoptik.ua/погода-"

news_title = {
    "politics": "Політичні новини",
    "economics": "Економіка та бізнес",
    "science": "Наука і технології майбутнього",
    "sport": "Спортивні події",
    "health": "Новини медицини, здоров’я та краси",
}

currency_code = {
    "USD": "долар США",
    "EUR": "євро",
    "CHF": "швейцарський франк",
    "GBP": "британський фунт",
    "SEK": "шведська крона",
    "CAD": "канадський долар",
    "XAU": "золото",
}

weather_cities = ["Київ", "Харків", "Дніпро", "Львів", "Одеса"]


def show(request, category=None):
    new_url = url + category + ".html"
    list_news = parsing(new_url)
    paginator = Paginator(list_news, 10)
    page = request.GET.get("page")
    try:
        news_on_page = paginator.page(page)
    except PageNotAnInteger:
        news_on_page = paginator.page(1)
    except EmptyPage:
        news_on_page = paginator.page(paginator.num_pages)
    return render(
        request,
        "news.html",
        {"list_news": news_on_page, "news_title": news_title[category]},
    )


def parsing(url):
    list_news = list()
    n = 100  # кол-во новостей
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    news = soup.find_all("section", class_="im")
    for index, new in zip(range(n), news):
        title = new.find("a", class_="im-tl_a")
        source = new.find("span", class_="im-pr_span")
        if not source:
            source = new.find("a", class_="im-pr_a")
        source_res = source.text.strip("()")
        match = re.match(r"^(\d+)\sновин[и]?$", source_res)
        if match:
            continue
        link = title["href"]
        dict_new = {"title": title.text, "source": source_res, "link": link}
        list_news.append(dict_new)
    return list_news


def rates(request):
    today = datetime.now()
    current_date = today.strftime("%d.%m.%Yр.")
    new_url_bank = url_bank + current_date[:-2]
    response_bank = requests.get(new_url_bank).json()
    list_exchange = list()
    for currency in currency_code:
        res = [
            k
            for k in filter(
                lambda el: el["currency"] == currency, response_bank["exchangeRate"]
            )
        ]
        one_dict = {
            "currency": currency,
            "name_currency": currency_code[currency],
            "sale": round(res[0]["saleRateNB"], 2),
        }
        list_exchange.append(one_dict)
    return render(
        request,
        "rates.html",
        context={"list_rates": current_date, "list_exchange": list_exchange},
    )


def weather(request):
    list_weather = list()
    for city in weather_cities:
        new_url_weather = url_weather + city.lower()
        response = requests.get(new_url_weather)
        soup = BeautifulSoup(response.text, "lxml")
        tbody = soup.find("table", class_="weatherDetails")
        tr = tbody.find("tr", class_="temperature")
        t1 = tr.find("td", class_="p3")
        t2 = tr.find("td", class_="p4 bR")
        t3 = tr.find("td", class_="p5")
        t4 = tr.find("td", class_="p6 bR")
        t5 = tr.find("td", class_="p7")
        t6 = tr.find("td", class_="p8")
        morning_t = t1.text + "..." + t2.text
        day_t = t3.text + "..." + t4.text
        night_t = t5.text + "..." + t6.text
        tusk = tr.find_next_sibling("tr").find_next_sibling("tr")
        tusk_m = tusk.find("td", class_="p3").text
        tusk_d = tusk.find("td", class_="p5").text
        tusk_n = tusk.find("td", class_="p7").text
        vologist = tusk.find_next_sibling("tr")
        vol_m = vologist.find("td", class_="p3").text
        vol_d = vologist.find("td", class_="p5").text
        vol_n = vologist.find("td", class_="p7").text
        viter = vologist.find_next_sibling("tr")
        vit_m = viter.find("td", class_="p3").find("div").get("data-tooltip")
        vit_d = viter.find("td", class_="p5").find("div").get("data-tooltip")
        vit_n = viter.find("td", class_="p7").find("div").get("data-tooltip")
        opadu = viter.find_next_sibling("tr")
        opadu_m = opadu.find("td", class_="p3").text
        opadu_d = opadu.find("td", class_="p5").text
        opadu_n = opadu.find("td", class_="p7").text
        dict_weather = {
            "city": city,
            "morning_t": morning_t,
            "day_t": day_t,
            "night_t": night_t,
            "tusk_m": tusk_m,
            "tusk_d": tusk_d,
            "tusk_n": tusk_n,
            "vologist_m": vol_m,
            "vologist_d": vol_d,
            "vologist_n": vol_n,
            "viter_m": vit_m,
            "viter_d": vit_d,
            "viter_n": vit_n,
            "opadu_m": opadu_m,
            "opadu_d": opadu_d,
            "opadu_n": opadu_n,
        }
        list_weather.append(dict_weather)
    today = datetime.now()
    current_date = today.strftime("%d.%m.%Yр.")
    return render(
        request,
        "weather.html",
        context={"context_weather": current_date, "list_weather": list_weather},
    )
