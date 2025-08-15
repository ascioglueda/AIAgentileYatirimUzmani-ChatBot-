'''  
duckduckgosearchrun, langchain kutuphanesi iceriside gelen hazir bir arac
web aramasi yapmak icin duckduckgo motorunu kullan
'''

from langchain.tools import DuckDuckGoSearchRun
#duckduckgo arama aracinin bir ornegini olustur
search = DuckDuckGoSearchRun()

if __name__ == "__main__": #burasi sadece test icin, search_tool.py dosyasini direkt calistirmak icin 
    #aranacak terimi belirle
    query = "bugün denizlide hava kac derece"

    #arama motoruna sorgu gonder ve sonucu al
    result =search.run(query)

    #arama sonucunu ekrana yazdir
    print(f"Arama sonucu: \n{result}")