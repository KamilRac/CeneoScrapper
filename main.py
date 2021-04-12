import requests 
import json 
from bs4 import BeautifulSoup

respons = requests.get ("https://www.ceneo.pl/32622086#tab=reviews")
page=2

while respons : 

    pageDOM= BeautifulSoup(respons.text, 'html.parser')

    opinions = pageDOM.select ("div.js_product-review")
    opinionsList=[]

    for opinion in opinions:
        opinionId=opinion["data-entry-id"]
        author = opinion.select("span.user-post__author-name").pop(0).get_text().strip()
        try: 
                rcmd=opinion.select("span.user-post__author-recomendation").pop(0).get_text().strip()
                rcmd = True if rcmd =="Polecam" else False
        except IndexError:
                rcmd = None
        stars=opinion.select("span.user-post__score-count").pop(0).get_text().strip()
        stars = float(stars.split("/")[0].replace(",", "."))
        content=opinion.select("div.user-post__text").pop(0).get_text().strip()
        content=content.replace("\n", " ").replace("\r", " ")
        pros=opinion.select("div[class*=\"positives\"] ~div.review-feature_item")
        pros=[item.get_text().stript for item in pros]
        cons=opinion.select("div[class*=\"negatives\"] ~div.review-feature_item")
        cons=[item.get_text().stript for item in cons]
        try:
                purchased=bool(opinion.select("div.review-pz").pop(0).get_text().strip())
        except IndexError: 
                purchased = False
        publishDate=opinion.select("span.user-post__published > time:nth-child(1)").pop(0)["datetime"].strip()
        try: 
                purchaseDate=opinion.select("span.user-post__published > time:nth-child(2)").pop(0)["datetime"].strip()
        except IndexError:
                purchaseDate = None 
        useful=int(opinion.select("span[id^=\"votes-yes\"]").pop(0).get_text().strip())
        useless=int(opinion.select("span[id^=\"votes-no\"]").pop(0).get_text().strip())

        opinionDict = {
                "opinionId": opinionId,
                "author": author,
                "rcmd": rcmd,
                "starts": stars ,
                "content": content,
                "pros": pros,
                "cons": cons,
                "purchased": purchased,
                "publishDate": publishDate, 
                "purchaseDate": purchaseDate,
                "useful": useful,
                "useless": useless
            }
        opinionsList.append(opinionDict)
    respons = requests.get("https://www.ceneo.pl/32622086/opinie"+str(page), allow_redirects=False)
    if respons.status_code==200:
        page+=1
    else: 
        break

with open("./opinions/32622086.json", "w", encoding="UTF-8") as f:
    json.dump (opinionsList, f, indent=4 , ensure_ascii=False)

#print(json.dumps(opinionDict, indent=4, ensure_ascii=False))
