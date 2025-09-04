import requests
from bs4 import BeautifulSoup
url = "https://www.gismeteo.kz/weather-kyzylorda-5319/10-days/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text,"html.parser")
    print("hello")
    day = soup.find_all("a",class_=["row-item link link-hover", "row-item link-red link-hover"])
    # headlines = soup.find_all("temperature-value")
    headlines = soup.find_all("div",class_="value")
    
    obj = []
    
    for d in day:
        day_ = d.find("div",class_="day")
        date_ = d.find("div",class_="date")
        if day_ and date_:  # проверка, что теги найдены
            data = {
                "day":day_.get_text(strip=True),
                "date":date_.get_text(strip=True)
            }
            obj.append(data)
            # print(f"{day_.get_text(strip=True)}")
            # print(f"{date_.get_text(strip=True)}")
    # print(obj)
    
    for i,h in enumerate(headlines[:10],0):
        max_v = h.find("div",class_="maxt")
        min_v = h.find("div",class_="mint")
        
        if max_v and min_v:
            max_value = max_v.find("temperature-value")
            min_value = min_v.find("temperature-value")
            
            if max_value and min_value:
                obj[i]["max"] = max_value.get("value","")
                obj[i]["min"] = min_value.get("value","")
                print(obj[i])
    RESULT = obj  
    
else:
    print("errors:",response.status_code)
    
    
