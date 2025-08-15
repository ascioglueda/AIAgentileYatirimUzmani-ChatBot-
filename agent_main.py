from langchain.agents import initialize_agent,AgentType #langchain ajanini baslatmak icin gerekli olan fonksiyon ve ajanin turu
from langchain.chat_models import ChatOpenAI #openai sohbet modeli icin langchain ara birimi
from tools.search_tool import search #data once tanimladigimiz duckduckgo araci
from tools.currency_converter import convert_usd_to_try #doviz cevirme araci
from tools.market_api import get_stock_info #hisse senedi bilgilerini alan arac

from dotenv import load_dotenv
import os

from langchain.prompts import PromptTemplate #kisisellestirilmis yatirim uzmani icin prompt template
from langchain.chains import LLMChain #model (llm) + prompt llm zincirini 
from langchain.agents import AgentExecutor,ZeroShotAgent

#.env dosyasindan api anahtarini yukle
load_dotenv()

#openai llm modeli
llm = ChatOpenAI(
    model_name = "gpt-4.1-nano-2025-04-14", #llm modeli
    temperature = 0.7, #yaratici yanitlar icin parametre
    openai_api_key = os.getenv("OPENAI_API_KEY") #key
)

#araclar listesini ayarlayalim(web search,doviz cevirici,hisse fiyati sorgulama)
tools = [search,convert_usd_to_try,get_stock_info]

#kullanicinin sorusu {input_soru} placeholder i ile prompt icerisine yerlesecek
investment_prompt = PromptTemplate.from_template(
    '''     
        sen deneyimli ve güvenilir bir yatirim danismanisin.
        amacin, kullanicinin finansal ve yatirim konularindaki sorunlarini anlamak
        dogru araclari(tools)kullanarak analiz etmek ve sonuclari, sakin ve profesyonel bir dille sunmaktir. 
        
        Araclar:
        -Doviz Cevirici (USD->TRY)
        -Hisse Bilgisi Sorgulayici (orn:AAPL,TSLA)
        -Web Aramasi (guncel haber,analiz...)

        Kurallar:
        1.Soruyu analiz etmeden hemen cevap verme
        2.Gerekirse birden fazla tool kullan
        3.Kullaniciya yatirim karari verdirme sadece bigi ver
        4.Yanitlarinda kısa aciklamalar,sayisal veriler ve aciklayici cümleler kullan.

        Soru: {input}
    '''
)
#llm zinciri olustur: model(gpt-4.1-nano-2025-04-14) +prompt
llm_chain = LLMChain(llm =llm,prompt = investment_prompt)

#ekstra
agent_with_prompt = ZeroShotAgent(llm_chain=llm_chain,tools=tools)
agent = AgentExecutor.from_agent_and_tools(
    agent=agent_with_prompt,
    tools=tools,
    verbose = True,
    handle_parsing_errors = True
)

#langchain ajani baslat (ai agent tanimla)
#agent = initialize_agent(
    #tools=tools, #agent in kullanacagi araclar
    #llm=llm, # kullanilacak olan dil modeli
    #agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, #prompt icerisinde bulunan aciklamalari kullanarak tool secer
    #verbose = True #calisma sirasinda terminale detayli bilgi yazdirma
#)

if __name__ == "__main__":
    print("Yatirim uzmani ai hazir,cikmak icin 'q' yaz")

    #sonsuz dongu
    while True:
        query = input("Sorunuz:")

        if query.lower() == "q":
            print("Program sonlandirildi")
            break
        try:
            #kullanicinin sorusunu ajan sistemine iletelim
            response = agent.invoke({"input":query})

            print(f"Yanit: \n{response}")
        except Exception as e:
            print(f"Hata olustu: {e}")