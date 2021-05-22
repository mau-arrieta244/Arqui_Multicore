#Proyecto arqui testing
import multiprocessing
import queue
from sys import setswitchinterval
import requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
import webbrowser
import multiprocessing as mp
from multiprocessing import Queue
from multiprocessing import Pool
from multiprocessing import Process
import time
start_time = time.time()

#header se usa para que paginas web crean que está entrando un usuario, no un bot
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}

#formato base de datos
'''
{
    "Nombre juego":[linkMetacritic, link precio new egg, link howLongToBeat, etc...],
    "Nombre juego2":[linkMetacritic, link precio new egg, link howLongToBeat, etc...]
}
'''
baseDatos = {

             "Control":['https://www.metacritic.com/game/playstation-4/control',
             "https://www.newegg.com/p/N82E16879708076",
             'https://howlongtobeat.com/game?id=57507',
             'https://www.bestbuy.ca/en-ca/product/control-ps4/13626416'],

             "Tales of Arise":['https://www.metacritic.com/game/playstation-4/tales-of-berseria',
             "https://www.newegg.com/p/N82E16879253234",
             'https://howlongtobeat.com/game?id=33713',
             'https://www.bestbuy.ca/en-ca/product/tales-of-arise-ps5/15447858'],

             "Outriders":['https://www.metacritic.com/game/playstation-4/outriders',
             "https://www.newegg.com/p/N82E16879262258",
             'https://howlongtobeat.com/game?id=68276',
             'https://www.bestbuy.ca/en-ca/product/outriders-day-one-edition-ps5/15012081'],

             "AceCombat7:SkiesUnknown":['https://www.metacritic.com/game/playstation-4/ace-combat-7-skies-unknown',
             'https://www.newegg.com/bandai-namco-games-ace-combat-7-skies-unknown-playstation-4/p/N82E16879253196?Description=ace%207&cm_re=ace_7-_-79-253-196-_-Product',
             'https://howlongtobeat.com/game?id=53763',
             'https://www.bestbuy.ca/en-ca/product/red-dead-redemption-2-ps4/10513695'],

             "Ancestors:TheHumankindOdyssey":['https://www.metacritic.com/game/playstation-4/ancestors-the-humankind-odyssey',
             'https://www.newegg.com/private-division-ancestors-the-humankind-odyssey/p/N82E16832014006?Description=ancestors%20humankind&cm_re=ancestors_humankind-_-32-014-006-_-Product&quicklink=true',
             'https://howlongtobeat.com/game?id=69316',
             'https://www.bestbuy.ca/en-ca/product/ancestors-the-humankind-odyssey-xbox-one-digital-download/14338266'],

             "AstrobotRescueMission":['https://www.metacritic.com/game/playstation-4/astro-bot-rescue-mission',
             'https://www.newegg.com/sony-astro-bot-rescue-mission-playstation-4/p/N82E16879261736?Description=astro%20bot%20rescue&cm_re=astro_bot%20rescue-_-79-261-736-_-Product',
             'https://howlongtobeat.com/game?id=61569',
             'https://www.bestbuy.ca/en-ca/product/astro-bot-rescue-mission-for-playstation-vr-ps4/12856332'],

             "AssassinsCreed:Odyssey":['https://www.metacritic.com/game/playstation-4/assassins-creed-odyssey',
             'https://www.newegg.com/ubisoft-assassin-s-creed-odyssey-playstation-4/p/N82E16879807026?Description=assassins%20creed%20odyssey&cm_re=assassins_creed%20odyssey-_-79-807-026-_-Product',
             'https://howlongtobeat.com/game?id=57503',
             'https://www.bestbuy.ca/en-ca/product/assassin-s-creed-odyssey-playstation-4/15239319'] 
            }




def precioBestBuy(url,queue):
    try:
        resultado = requests.get(url,headers=header).text
        soup = BeautifulSoup(resultado,'lxml')
        body = soup.find('body')
        panelPrecio = body.find('div',class_='productPricingContainer_3gTS3')
        precio = panelPrecio.find('span',class_="screenReaderOnly_3anTj large_3aP7Z").text
        queue.put(precio)
        #print(precio)
    except AttributeError:
        #print("N/A")
        queue.put("N/A")

def precioNewEggIndividual(url,queue):
    try:
        resultado = requests.get(url,headers=header).text
        soup = BeautifulSoup(resultado,'lxml')
        body = soup.find('body')
        panelPrecio = body.find('div',class_='product-price')
        panelPrecio1 = panelPrecio.find('ul',class_='price')
        precio = panelPrecio1.find('li',class_='price-current').text
        queue.put(precio)
    except AttributeError:
        queue.put("N/A")
    #print(precio)

def metaScoreIndividual(url,queue):
    try:
        resultado = requests.get(url,headers=header).text

        soup = BeautifulSoup(resultado,'lxml')
        body = soup.find('body')


        #MetaScore -------------------------------------------------------------
        panelRating = body.find('div',class_='metascore_w xlarge game positive')
        #print(panelRating.prettify())

        metaScore = panelRating.find('span').text
        queue.put(metaScore)
        #print(metaScore)
        
    except AttributeError:
        try:
            resultado = requests.get(url,headers=header).text

            soup = BeautifulSoup(resultado,'lxml')
            body = soup.find('body')


            #MetaScore -------------------------------------------------------------
            panelRating = body.find('div',class_='metascore_w xlarge game mixed')
            #print(panelRating.prettify())

            metaScore = panelRating.find('span').text
            queue.put(metaScore)
            #print(metaScore)

        except AttributeError:
            resultado = requests.get(url,headers=header).text

            soup = BeautifulSoup(resultado,'lxml')
            body = soup.find('body')


            #MetaScore -------------------------------------------------------------
            panelRating = body.find('div',class_='metascore_w xlarge game negative')
            #print(panelRating.prettify())

            metaScore = panelRating.find('span').text
            queue.put(metaScore)
            #print(metaScore)



def howLongToBeat(url,queue):
    resultado = requests.get(url,headers=header).text
    soup = BeautifulSoup(resultado,'lxml')
    body = soup.find('body')
    panelTiempo = body.find('div',class_='game_times')
    tiempo = panelTiempo.find('div').text
    queue.put(tiempo)
    #print(tiempo)


def paralelo1():
    juegos = list(baseDatos.keys())[:3]

    #para almacenar resultados de segundo y tercer nivel de paralelismo
    queue = Queue()
    
    for juego in juegos:

        procesos=[]
        resultados=[]

        

        
        # for indice in listaIndices:
        #     url = baseDatos[juego][indice]
        urlMetacritic = baseDatos[juego][0]
        urlNewEgg = baseDatos[juego][1]
        urlHowLong = baseDatos[juego][2]
        urlBestBuy = baseDatos[juego][3]
        

        #segundo y tercer nivel de paralelismo, obtiene en paralelo..
        #.. la info de las 4 paginas para cada juego
        if __name__ == "__mp_main__":
        
            p5 = Process(target=metaScoreIndividual(urlMetacritic,queue))
            p6 = Process(target=precioNewEggIndividual(urlNewEgg,queue))
            p7 = Process(target=precioBestBuy(urlBestBuy,queue))
            p8 = Process(target=howLongToBeat(urlHowLong,queue))


            procesos.append(p5)
            procesos.append(p6)
            procesos.append(p7)
            procesos.append(p8)

            p5.start()
            p6.start()
            p7.start()
            p8.start()

            
            #por medio del Queue, se almacenan aca los returns de esas funciones
            #es necesario obtener los returns asi ya que las llamadas ocurren en paralelo
            #y no se puede asignar una variable a un Process y esperar que se obtenga ese return
            for proceso in procesos:
                result = queue.get()
                resultados.append(result)

            p5.join()
            p6.join()
            p7.join()
            p8.join()

        metascore = resultados[0]
        precioNewEgg = resultados[1]
        precioBest = resultados[2]
        howLong = resultados[3]
        howLong = howLong[:11]

        f = open("C:\\Users\\mauar\\Desktop\\proyAqui_Multicore\\proyecto_Arqui_Multicore\\indexMau.html","r")
        #lectura del file
        contents = f.read()
        
        sopa = BeautifulSoup(contents,'lxml')
        f.close()
        plantsTag = sopa.find('div',class_="plants")
        row = (plantsTag.find_all(class_="row")[1])

        figura1 = sopa.new_tag('div',class_="col-xl-4 col-lg-4 col-md-6 col-sm-12")
        row.insert(0,figura1)

        figura2 = sopa.new_tag('div',class_="plants-box")
        figura1.insert(0,figura2)
            
        figure = sopa.new_tag('figure')
        
        figura2.insert(0,figure)
        imagen = sopa.new_tag('img')
        
        #imagen['alt'] = "imagen.."
        imagen['src']="images/"+juego+".jpg"
        
        figure.insert(0,imagen)
            

        h3 = sopa.new_tag('h3')
        h3.string = juego
        figure.insert_after(h3)

        p1 = sopa.new_tag('p')
        p1.string = "NewEgg: "+precioNewEgg
        h3.insert_after(p1)

        p2 = sopa.new_tag('p')
        p2.string = "BestBuy: "+precioBest
        p1.insert_after(p2)

        p3 = sopa.new_tag('p')
        p3.string = "MetaCritic: "+metascore
        p2.insert_after(p3)

        p4 = sopa.new_tag('p')
        p4.string = "HowLongToBeat: "+howLong
        p3.insert_after(p4)

        with open("C:\\Users\\mauar\\Desktop\\proyAqui_Multicore\\proyecto_Arqui_Multicore\\indexMau.html","w")as outf:
            outf.write(str(sopa))
    
    
    
            
    
    
    


def paralelo2():
    juegos = list(baseDatos.keys())[3:]
    

    #para almacenar resultados de segundo y tercer nivel de paralelismo
    queue = Queue()
    
    for juego in juegos:

        procesos=[]
        resultados=[]

        

        
        # for indice in listaIndices:
        #     url = baseDatos[juego][indice]
        urlMetacritic = baseDatos[juego][0]
        urlNewEgg = baseDatos[juego][1]
        urlHowLong = baseDatos[juego][2]
        urlBestBuy = baseDatos[juego][3]
        

        #segundo y tercer nivel de paralelismo, obtiene en paralelo..
        #.. la info de las 4 paginas para cada juego
        if __name__ == "__mp_main__":
        
            p5 = Process(target=metaScoreIndividual(urlMetacritic,queue))
            p6 = Process(target=precioNewEggIndividual(urlNewEgg,queue))
            p7 = Process(target=precioBestBuy(urlBestBuy,queue))
            p8 = Process(target=howLongToBeat(urlHowLong,queue))


            procesos.append(p5)
            procesos.append(p6)
            procesos.append(p7)
            procesos.append(p8)

            p5.start()
            p6.start()
            p7.start()
            p8.start()

            
            #por medio del Queue, se almacenan aca los returns de esas funciones
            #es necesario obtener los returns asi ya que las llamadas ocurren en paralelo
            #y no se puede asignar una variable a un Process y esperar que se obtenga ese return
            for proceso in procesos:
                result = queue.get()
                resultados.append(result)

            p5.join()
            p6.join()
            p7.join()
            p8.join()

        metascore = resultados[0]
        precioNewEgg = resultados[1]
        precioBest = resultados[2]
        howLong = resultados[3]
        howLong = howLong[:11]

        f = open("C:\\Users\\mauar\\Desktop\\proyAqui_Multicore\\proyecto_Arqui_Multicore\\indexMau.html","r")
        #lectura del file
        contents = f.read()
        
        sopa = BeautifulSoup(contents,'lxml')
        f.close()
        plantsTag = sopa.find('div',class_="plants")
        row = (plantsTag.find_all(class_="row")[1])

        figura1 = sopa.new_tag('div',class_="col-xl-4 col-lg-4 col-md-6 col-sm-12")
        row.insert(0,figura1)

        figura2 = sopa.new_tag('div',class_="plants-box")
        figura1.insert(0,figura2)
            
        figure = sopa.new_tag('figure')
        
        figura2.insert(0,figure)
        imagen = sopa.new_tag('img')
        
        #imagen['alt'] = "image..."
        imagen['src']="images/"+juego+".jpg"
        
        figure.insert(0,imagen)
            

        h3 = sopa.new_tag('h3')
        h3.string = juego
        figure.insert_after(h3)

        p1 = sopa.new_tag('p')
        p1.string = "NewEgg: "+precioNewEgg
        h3.insert_after(p1)

        p2 = sopa.new_tag('p')
        p2.string = "BestBuy: "+precioBest
        p1.insert_after(p2)

        p3 = sopa.new_tag('p')
        p3.string = "MetaCritic: "+metascore
        p2.insert_after(p3)

        p4 = sopa.new_tag('p')
        p4.string = "HowLongToBeat: "+howLong
        p3.insert_after(p4)

        with open("C:\\Users\\mauar\\Desktop\\proyAqui_Multicore\\proyecto_Arqui_Multicore\\indexMau.html","w")as outf:
            outf.write(str(sopa))
    
    

    




def autoScrape(indiceInicial,indiceFinal):
    '''
    Llama las funciones de scraping para cada juego en la "base de datos" (diccionario)
    Entradas: N/A
    Salidas: N/A
    '''
    juegos = list(baseDatos.keys())[indiceInicial:indiceFinal+1]
    for juego in juegos:
        #para el paralelismo aca, podemos simplemente hacer una listaIndices = [0,1,2,3]
        #y dividir la lista entre los distintos procesadores para obtener todo en paralelo y no secuencial...
        
        # for indice in listaIndices:
        #     url = baseDatos[juego][indice]


        print("\n ------------------------------ \n")
        print(juego,"\n")
        print("Metascore: ")
        urlMetacritic = baseDatos[juego][0]
        metaScoreIndividual(urlMetacritic)

        #como manejar ofertas? comparar estos dos precios y calcular cuanto % menos
        #vale el menor de ambas opciones
        print("\nPrecio (NewEgg)")
        urlNewEgg = baseDatos[juego][1]
        precioNewEggIndividual(urlNewEgg)

        print("\nPrecio (BestBuy)")
        try:
            urlBestBuy = baseDatos[juego][3]
            precioBestBuy(urlBestBuy)
        except IndexError:
            print("N/A")
            pass

        print("\n Tiempo para completar: ")
        urlHowLong = baseDatos[juego][2]
        howLongToBeat(urlHowLong)



#############################################################################################
#############################################################################################
#                                Programa Principal                                         #
#############################################################################################
#############################################################################################





#Proceso paralelo

def paralel():
    

    if __name__ == "__main__":
        
        '''
        Jobs, pipe lists y send_end... son necesarios para recuperar el return de las funciones paralelas.
        los returns se guardan en lista result_list y de ahi se ajustan para el HTML
        '''
        

        
        

        p1 = Process(target=paralelo1)
        
        #pipe_list.append(recv_end1)
        p1.start()

        
        p2 = Process(target=paralelo2)
        
        
        p2.start()

        p1.join()
        p2.join()

        print("\n -----duracion proceso:  %s segundos ------" %(time.time()-start_time))





#proceso paralelo


paralel()


#proceso secuencial


#autoScrape(0,5)
#print("\n -----duracion proceso:  %s segundos ------" %(time.time()-start_time))
