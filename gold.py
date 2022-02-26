import requests, json
from  flask import Flask, jsonify
from bs4 import BeautifulSoup as bs
from datetime import datetime

from config import PORT
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home_page():

    url = F"https://gadgets.ndtv.com/finance/gold-rate-in-india"
    gold_List = []
    def home_price():

        response = requests.get(url)
        soup = bs(response.text,"lxml")
        anchor1= soup.find_all('div',"_cptbl _cptblm")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        for State in anchor1:
         Title =  State.find_all('tr',"_cptbltr")

         for value in Title:
            Title1 = value.find("a")
            Title2 = value.find('td',"_lft")

            if(Title1!=None):
                State = Title1.text.strip()
                Price = Title2.text.strip()
                Date_Time = dt_string

                Gold = {
                'City': State,
                '24_Carat_Gold_Rate': Price,
                'Date & Time': Date_Time,
                }

                gold_List.append(Gold)
                New_List = json.dumps(gold_List, indent =2)
                with open("data.json", "w", encoding="utf-8") as file:
                    file.write(str(New_List))
    home_price()
    return jsonify(gold_List)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port= PORT)
    