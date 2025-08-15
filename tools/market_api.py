'''  
finnhub api ile hisse senedi bilgilerini alalim
api_key: https://finnhub.io/dashboard
'''
from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv() #.env dosyasini yukleyerek icersindeki api anahtarini erisilebilir hale getirir

@tool # langchain tarafindan kullanilacak olan get_stock_info fonksiyonunu isaretler
def get_stock_info(ticker: str) -> str:
    '''  
    bir hisse senedi sembolu (orn: AAPL) icin guncel fiyat bilgiisi doner
    Parametre:
        ticker (str): hisse senedinin sembolu (orn: "AAPL","GOOGL")
    Output:
        str: guncell hisse bilgilerini iceren metin
    '''
    try:
        #.env dosyasindan Finnhub api anahtarini al
        api_key = os.getenv("FINNHUB_API_KEY")

        #eger api anahtari yoksa kullaniciya hata mesaji return et

        if not api_key:
            return "API anahtari bulunamadi"
        
        #Finnhub api dan belirli bir hisse senedi icin fiyat bilgilerini alan url tanimla
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"

        #API ye get istegi gonder
        response = requests.get(url)
        
        #eger istek basarisiz ise (403,404,500 vs)
        if response.status_code != 200:
            return f"API hatasi: {response.status_code}"
        
        #API den gelen yaniti coz
        data = response.json()

        #json icinden guncel fiyat (c), acilis fiyati (o), en yuksek fiyat (h), en dusuk fiyat(l)
        current = data.get("c") #current price
        open_ = data.get("o") #openning price
        high = data.get("h") #day's high price
        low = data.get("l") #day's low

        return (
            f"{ticker} Hisse bilgisi: \n"
            f"-Guncel Fiyat: {current} USD\n"
            f"-Acilis: {open_} USD\n"
            f"-Gun ici en yuksek: {high} \n"                                                    
            f"-Gun ici en dusuk: {low} \n"                                                    
        )
    except Exception as e:
        return f"Hata olustu: {e}"
    
if __name__ == "__main__":
    print(get_stock_info.run({"ticker": "GOOGL"}))