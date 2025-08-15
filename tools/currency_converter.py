#usd to tl

from langchain.tools import tool #bu dekorator sayesinde fonksiyonumuz bir langchain araci(tool) olarak tanimlanabilecek
import requests #http istekleri yapmak icin gerekli olan kutuphane

@tool #@tool sayesinde convert_usd_to_try fonksiyonu langchain ajanlari tarafindan kullanilabilecek bir arac oldugu belirtilir
def convert_usd_to_try(amount: float) -> str:
    ''' 
    usd miktarini try ye cevir
    amount parametresi sadece sayi olmali
    '''
    try:
        #eger kullanicidan gelen "amount " degeri bir string ise ornegin "100 usd"
        #sayisal olmayan karakterleri cikarmak ve floata cevirmek
        if isinstance(amount,str):
            #rakamlar ve noktalari birakalim, diger karakterleri filtrele ve floata cevir
            amount = float("".join(filter(lambda c:c.isdigit() or c == ".", amount)))

        #CoinGecko API sinden USD/TRY donusum oranini alalim
        url = "https://api.coingecko.com/api/v3/simple/price?ids=usd&vs_currencies=try"

        #bu url e get istegi gonder
        response  = requests.get(url)

        #eger api istegi basarisiz olursa ornegin 404 veya 500 seklinde
        if response.status_code != 200:
            return f"API hatasi. Kod: {response.status_code}"
        
        #apiden donen json verisini dictionary olarak alalim
        data = response.json()

        #dictionary icerisinden dolarin rate degerini alalim
        rate = data["usd"]["try"]

        #kullanicinin verdigi amount ile doviz kurunu carpalim
        result = amount*rate

        #"100 usd = 4000 TRY (Kur: 40)"
        return f"{amount} usd = {result:.2f} TRY (Kur: {rate:.2f})"
    except Exception as e:
        return f"Hata olustu {e}"
    
if __name__ == "__main__":
    #test etmek icin 100 dolar yazalim
    test_amount =100
    print(f"{test_amount} USD -> TRY")
    print(convert_usd_to_try.run({"amount": test_amount}))