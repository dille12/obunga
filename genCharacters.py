
from character import Character

class Dialogue:
    def __init__(self, character, day, flags, type, dialogue):
        self.character = character
        self.flags = flags
        self.day = day
        self.type = type
        self.dialogue = dialogue

        # {day: {state: [lines]}}

class showUp:
    def __init__(self, character, day, request, pay, dialogue = {}, onFlags = []):
        character.showUps.append(self)
        self.character = character
        self.day = day
        self.onFlags = onFlags
        self.dialogue = {}
        self.request = request
        self.pay = pay

    def addDialogue(self, state, dialogue):
        self.dialogue[state] = []
        for x in dialogue:
            self.dialogue[state].append([x, self.character.name])
        




def genCharacters(game):

    makke = Character(game, "Matias Pekkanen")
    makke.setDeathText("Matiaksen ruumiista löytyi vain ehjä maha...")
    makke.setOrganOnHarvest("maksa")

    day1 = showUp(makke, 1, "munuainen", 0)
    day1.addDialogue("intro", ["Kun olin lapsi, aina halusin toisen munuaisen.", "Mutta minulla ei ole raha!"])
    day1.addDialogue("accept", ["Kiitos Maria!"])
    day1.addDialogue("deny", ["..."])

    day2deny = showUp(makke, 2, "munuainen", 0, onFlags=["1deny"])
    day2deny.addDialogue("intro", ["Vaikka olen rahaton, tarvitsen minäkin elimiä.", "Pyydän!"])
    day2deny.addDialogue("accept", ["Viimein.", "Typerys."])
    day2deny.addDialogue("deny", ["Nauti tästä päivästä.", "Huominen on viimeinen päiväsi kaupustelijana."])

    Jouni = Character(game, "Jouni Pekkanen")

    Jouni.setDeathText("Jounin silmät ammottavat tyhjyyttään. Varmaankin toistuvasta pettymyksestä poikaansa.")
    Jouni.setOrganOnHarvest("maksa")

    day2 = showUp(Jouni, 2, "munuainen", 3, onFlags=["1 Matias Pekkanen killed"])
    day2.addDialogue("intro", ["Tiedän että tapoit poikani.", "Hän oli hirvittävä lapsi.", "Mutta Jumala sinut periköön teostasi."])
    day2.addDialogue("accept", ["Varo selustaasi."])
    day2.addDialogue("deny", ["Ei sillä ole väliä.", "Otan sen mielummin sinulta."])

    day2 = showUp(Jouni, 2, "", 0, onFlags=["1 Matias Pekkanen accept"])
    day2.addDialogue("intro", ["Kiitos kun autoit poikaani!", "Vaikka hulttio se poika onkin.", "Voi kuinka loli voikaan viedä miestä..."])


    oskari = Character(game, "Oskari Heikkinen")
    oskari.setDeathText("Oskarin ruumis on läpimätä vuosien alkoholismista.")
    oskari.setOrganOnHarvest("maha")
    




    day1 = showUp(oskari, 1, "maksa", 1)
    day1.addDialogue("intro", ["Minun ei kuuluisi olla täällä.", "Mutta maksani pettää."])
    day1.addDialogue("accept", ["Otat suuren riskin, seppä ei koskaan unohda."])
    day1.addDialogue("deny", ["Ehkä on parempi näin.", "Mutta kuulet vielä vasarani kaikuja."])

    day3deny = showUp(oskari, 3, "maksa", 2, onFlags=["1deny"])
    day3deny.addDialogue("intro", ["En pyydä enää.", "Sinä *tarvitset* maksaa enemmän kuin minä."])
    day3deny.addDialogue("accept", ["Minä… kuulen niiden äänen taas.", "Seppä ei unohda."])
    day3deny.addDialogue("deny", ["Olen takonut viimeisen vasarani.", "Mutta huomenna, sen lyönti kuuluu päässäsi."])

    mirror = Character(game, "???")
    mirror.setDeathText("Se sekopää jonka tapoin on kadonnut tyystin!")
    mirror.setOrganOnHarvest("")

    day3 = showUp(mirror, 3, "sydän", 3)
    day3.addDialogue("intro", ["Sinä olet väsynyt.", "Voisit olla vapaa, jos annat sydämesi."])
    day3.addDialogue("accept", ["Kiitos.", "Näet itsesi pian."])
    day3.addDialogue("deny", ["Ei ole väliä.", "Katsot itseäsi peilistä joka päivä, eikö?"])


    day5 = showUp(mirror, 5, "sydän", 3, onFlags=["3deny"])
    day5.addDialogue("intro", ["Viimeinen päivä.", "Tänään… valitset, kumpi jää."])
    day5.addDialogue("accept", ["Viisas valinta.", "Tai ehkä se ei ollut sinun valintasi ollenkaan."])
    day5.addDialogue("deny", ["Älä katso peiliin tänään.", "Se saattaa katsoa takaisin."])


    henry = Character(game, "Henry Tapio Piiroinen")
    henry.setDeathText("Onpa iso mies. Karvainen mies. Epilepsia, 46v.")
    henry.setOrganOnHarvest("sydän")
    day2 = showUp(henry, 2, "sydän", 2)
    day2.addDialogue("intro", ["Tykkäätkö isoista miehistä?", "Karvaisista miehistä?", "Minulla on epilepsia ja huono sydän.", "Tarvitsisin uuden."])
    day2.addDialogue("accept", ["*Hän tuijottaa sinua tyhjä ilme kasvoillaan*", "*Lopulta hän löntystää pois*"])
    day2.addDialogue("deny", ["46v, täysin yksin..."])


    day3 = showUp(henry, 3, "sydän", 3, onFlags=["2deny"])
    day3.addDialogue("intro", ["Kyborgihenry tässä terve.", "Tarvitsisin sen sydämen ja vähän äkkiä."])
    day3.addDialogue("accept", ["*Henry ottaa paidan pois ja tuijottaa sinua*", "*Lopulta hän löntystää pois*"])
    day3.addDialogue("deny", ["Olen kauhean sairas.", "Epilepsia muunmuassa."])


    henrik = Character(game, "Henrik Salonen")
    henrik.setDeathText("Henrik. Luuseri.")
    henrik.setOrganOnHarvest("munuainen")



    day2 = showUp(henrik, 2, "sydän", 2)  
    day2.addDialogue("intro", ["Minun täytyy saada uusi sydän.", "Hän ei halua minua enää, mutta tämä voi muuttaa kaiken."])
    day2.addDialogue("accept", ["Kiitos! Hän *huomaa* minut taas."])
    day2.addDialogue("deny", ["Olen jo kuollut.", "Sinä vain päätit milloin."])




    veeti = Character(game, "Veeti Rautio")
    veeti.setDeathText("Veetin maha on täynnä hyytynyttä verta.")
    veeti.setOrganOnHarvest("munuainen")


    day3 = showUp(veeti, 3, "maksa", 3)  
    day3.addDialogue("intro", ["Tarvitsen maksan, mutta älä kysy miksi.", "*Heh.*"])
    day3.addDialogue("accept", ["Nyt voin juoda taas.", "Ei alkoholia… mutta verta."])
    day3.addDialogue("deny", ["Viime yönä sinä jo annoit sen minulle.", "*Etkö muista?*"])

    aino = Character(game, "Aino Lehtonen")
    aino.setDeathText("Ainon kieli on revitty erittäin epäsiististi.")
    aino.setOrganOnHarvest("maksa")




    day4 = showUp(aino, 4, "maha", 1)  
    day4.addDialogue("intro", ["[Hän ojentaa sinulle paperin. Siinä lukee: 'Anna minulle maha.']"])
    day4.addDialogue("accept", ["[Hän ei sano mitään, mutta nyökkää ja kävelee pois.]"])
    day4.addDialogue("deny", ["[Hän tuijottaa sinua liian pitkään. Silmät eivät räpäytä.]"])

    vilho = Character(game, "Vilho Manner")
    vilho.setDeathText("Vilhon vasen jalka on läpimätä.")
    vilho.setOrganOnHarvest("maha")



    day1 = showUp(vilho, 1, "munuainen", 2)  
    day1.addDialogue("intro", ["Olen nähnyt kuolemaa enemmän kuin kukaan täällä.", "Mutta yksi munuainen lisää ei tekisi pahaa."])
    day1.addDialogue("accept", ["Kiitos, poika.", "Ehkä nyt voin juoda ilman kipua."])
    day1.addDialogue("deny", ["Ei ole väliä.", "Olen jo haudassa, eikö niin?"])

    helmi = Character(game, "Helmi Koistinen")
    helmi.setDeathText("Helmen ruumis on erittäin aliravittu.")
    helmi.setOrganOnHarvest("sydän")


    day2 = showUp(helmi, 4, "maha", 3)  
    day2.addDialogue("intro", ["Oma vatsani ei enää toimi.", "Tarvitsen uuden, jotta voin syödä kunnolla."])
    day2.addDialogue("accept", ["Mmm…", "Haistatko tuon liha? Nyt voin nauttia siitä."])
    day2.addDialogue("deny", ["Sinä et ymmärrä.", "Jos en syö… *hän* syö minut."])

    saara = Character(game, "Saara Karhunen")
    saara.setDeathText("Saaran päällä on edelleen hääkaapu.")
    saara.setOrganOnHarvest("maha")



    day5 = showUp(saara, 5, "maksa", 2)  
    day5.addDialogue("intro", ["En koskaan saanut juoda häämaljaani.", "Mutta vielä on aikaa."])
    day5.addDialogue("accept", ["Tervehdykseksi hääpäivälleni.", "Tule tanssimaan kanssani veden alla."])
    day5.addDialogue("deny", ["Hän ei koskaan saapunut alttarille.", "Ehkä siksi olen vielä täällä."])

    petri = Character(game, "Petri Jokinen")
    petri.setDeathText("Naapurin Petri. Mitä minä olen tehnyt...")
    petri.setOrganOnHarvest("munuainen")


    day1 = showUp(petri, 1, "munuainen", 1)  
    day1.addDialogue("intro", ["Hei naapurini!", "Voisitko lainata minulle munuaisen?"])
    day1.addDialogue("accept", ["Sinä olet hyvä ystävä.", "Nähdään taas pian!"])
    day1.addDialogue("deny", ["Hmm.", "No, ehkä voin lainata sinulta silti jotain yöllä."])

    #petri_return = Character(game, "Petri Jokinen")
    day3 = showUp(petri, 3, "sydän", 2, onFlags=["1 Petri Jokinen accept"])  
    day3.addDialogue("intro", ["Hei taas, ystäväni!", "Mun munuainen… se ei toimi enää.", "Se *ei kuulu minulle.*"])
    day3.addDialogue("accept", ["Kiitos! Nyt kaikki on kuten pitää."])
    day3.addDialogue("deny", ["Obunga kuiskaa, tiedäthän?", "Hän sanoo, ettei tämä ole viimeinen asia, jonka otan."])

    ella = Character(game, "Ella Jokinen")
    ella.setDeathText("Ellan kaulassa oli painauma, kuin näkymättömät sormet olisivat puristaneet häntä.")
    ella.setOrganOnHarvest("sydän")


    day4 = showUp(ella, 4, "sydän", 0, onFlags=["1 Petri Jokinen killed"])  
    day4.addDialogue("intro", ["Tiedän, mitä teit mun Petri-paralle.", "Hänellä oli pahoja tapoja… mutta ei hän ansainnut sitä."])
    day4.addDialogue("accept", ["Puhdistit syntini, nyt annan sinulle anteeksi."])
    day4.addDialogue("deny", ["Hän tulee takaisin.", "Obunga antaa hänen tulla takaisin."])

    day4 = showUp(ella, 4, "sydän", 3, onFlags=["1 Petri Jokinen deny"])  
    day4.addDialogue("intro", ["Miten saatoit kieltäytyä antamasta naapurillesi munuaista.", "Eikö sinulla ole sydäntä?", "Toivottavasti on, sillä tarvitsen yhden."])
    day4.addDialogue("accept", ["Kiitos, mutta toivottavasti autat vielä Petriä."])
    day4.addDialogue("deny", ["Näinä tuomion päivinä Obunga tuomitsee syntejämme.", "Haluatko tosiaan että hän näkee sinut noin tuomitsevana?"])

    day4 = showUp(ella, 3, "sydän", 3, onFlags=["1 Petri Jokinen accept"])  
    day4.addDialogue("intro", ["Kiitos kun autoit naapuriasi hädässä.", "Olen hänen vaimonsa, ja hän tarvitsee nyt uuden sydämen.", "Hän oli liian heikko tullakseen tänne itse."])
    day4.addDialogue("accept", ["Kiitos tuhannesti!."])
    day4.addDialogue("deny", ["Harmi...", "Saatoit juuri tuomita naapurisi kuolemaan."])


    jouni_corrupt = Character(game, "Jouni Pekkanen?")
    jouni_corrupt.setDeathText("Jounin ruumis katosi yön aikana. Vain hänen sydämensä jäi lattialle.")
    jouni_corrupt.setOrganOnHarvest("sydän")

    day3 = showUp(jouni_corrupt, 3, "sydän", 3, onFlags=["2 Jouni Pekkanen accept"])  
    day3.addDialogue("intro", ["Tämä sydän ei ollut minun.", "Mutta nyt *olen* se, jolta se otettiin."])
    day3.addDialogue("accept", ["Obunga on ylpeä.", "Olen osa jotakin suurempaa."])
    day3.addDialogue("deny", ["Minä katson sinua unissasi.", "Ei enää kauaa."])

    ilona = Character(game, "Ilona Saarinen")
    ilona.setDeathText("Ilona oli pureskellut omat sormensa irti ennen kuolemaansa.")
    ilona.setOrganOnHarvest("maksa")


    day2 = showUp(ilona, 2, "maha", 1)  
    day2.addDialogue("intro", ["Hirveä nälkä.", "Ottaisin yhden mahalaukun kiitos!"])
    day2.addDialogue("accept", ["*Nam.*", "Herkullista!"])
    day2.addDialogue("deny", ["No mä meen keburullan kautta himaan sit.", ":("])


    day5 = showUp(ilona, 5, "maksa", 2, onFlags=["2 Ilona Saarinen accept"])  
    day5.addDialogue("intro", ["Se mitä söin… en tunne sitä enää.", "Mutta Obunga sanoi, että maksa auttaa."])
    day5.addDialogue("accept", ["*Nam.*", "Ehkä nyt se maistuu taas hyvältä."])
    day5.addDialogue("deny", ["Se tulee ulos. Se hiipii yöllä.", "Se tarvitsee sinut."])

    tapani = Character(game, "Father Tapani")
    tapani.setDeathText("Hänen suunsa oli auki kuin kuiskaten viimeisen rukouksen.")
    tapani.setOrganOnHarvest("sydän")


    day5 = showUp(tapani, 4, "sydän", 1, onFlags=["1 killed", "2 killed", "3 killed"])  
    day5.addDialogue("intro", ["Katumus tulee myöhään, kauppias.", "Mutta ei koskaan liian myöhään Obungalle.", "Kuinka kehtaat teurastaa tämän kylän asukkaita näin?", "Kolme päivää olet pitänyt puotiasi auki, ja jokaisena päivänä veri on vuotanut.", "Anna minulle sydän, niin annan sinulle syntisi anteeksi."])
    day5.addDialogue("accept", ["Sydän sopii meille kaikille.", "Tämä on lahja."])
    day5.addDialogue("deny", ["Obunga tulee huomenna.", "Nauti viimeisestä yöstäsi."])

    juhani = Character(game, "Juhani")
    juhani.setDeathText("Juhani tykkäs selkeesti huumeista.")
    juhani.setOrganOnHarvest("sydän")


    day2 = showUp(juhani, 2, "", 0, onFlags=["1 killed"])  
    day2.addDialogue("intro", ["Jumalan päivää arvon elinkauppias!", "Olen kuullut että pyörität murhauspalveluita sivussa.", "Jos tappaisit puolestani niin palkitsen sinut ruhtinaallisesti.",
                               "Murhattava on Ella Jokinen, naapurisi vaimo.", "Jos satut törmäämään häneen, pistä se lihoiksi.", "Ella Jokinen..."])
    

    day4 = showUp(juhani, 5, "", 5, onFlags=["4 Ella Jokinen killed"])
    day4.addDialogue("intro", ["Kuulin uutiset, hurraa!", "Ella Jokinen on kadonnut eikä ruumista löydetty!", "Tässä viisi kolikkoa vaivanpalkaksi."])

    Asmodeus = Character(game, "Asmodeus")
    day5 = showUp(Asmodeus, 5, "sydän", 3)
    day5.addDialogue("intro", ["Itse kaikkivoipa Saatanakin tarvitsee sydämen.", "Ja sinähän annat minulle yhden."])
    day5.addDialogue("accept", ["Saatana kiittää", "ja kuittaa."])
    day5.addDialogue("deny", ["Toivottavasti sinulla on varaa vuokraasi..."])
    Asmodeus.setDeathText("Ei tainnut olla tämä äijä kaikkivoipa Saatana.")
    Asmodeus.setOrganOnHarvest("munuainen")



    Rääpijä = Character(game, "Rääpijä")
    day5 = showUp(Rääpijä, 5, "maksa", 1)
    day5.addDialogue("intro", ["No hei viisuista tuttu rääpijä tässä moikka!", "Annas minulle tuore maksa niin voin ryypätä kuten tvstä tutussa kappaleessa chsa hcsahcacssa."])
    day5.addDialogue("accept", ["Ahhh vittu viimein pääsee ryyppää."])
    day5.addDialogue("deny", ["Sori ei oo rahaa enää ku felloffasin.", "Sä tuomitsit rääpijän just kuoleen."])
    Rääpijä.setDeathText("Rääpijän maha on räjähtämäisillään. Vitun läski.")
    Rääpijä.setOrganOnHarvest("maha")


    isojalka = Character(game, "Isojalka")
    day5 = showUp(isojalka, 5, "maha", 2)
    day5.addDialogue("intro", ["RAAAAAAAHHHHH"])
    day5.addDialogue("accept", ["Kiitos!", "rraraAAAAHh"])
    day5.addDialogue("deny", ["*Isojalka murahtaa turhautuneesti*"])
    isojalka.setDeathText("Skalpellisi ei meinaa pystyä isojalan nahkaan. Löydät kumminkin sydämen lopulta.")
    isojalka.setOrganOnHarvest("sydän")

    obunga = Character(game, "OBUNGA")
    obunga.obunga = True
    day6 = showUp(obunga, 6, "", 0)
    day6.addDialogue("intro", ["TERVEHDYS KUOLEVAINEN.",
                               "OLET MAKSANUT VUOKRASI AJALLAAN.",
                               "NÄEN ETTÄ ELINKAUPPASI ON PYÖRINYT HYVIN.",
                               "KYLÄLÄISETKÄÄN EIVÄT LYNKANNEET SINUA MURHIESI EDESTÄ.",
                               "MUTTA SYNTISI OVAT PESEMÄTTÖMÄT.",
                               "KIITOS MUUTAMASTA ROPOSESTA JOTKA ANNOIT.",
                               ":)"])





if __name__ == "__main__":
    class gameTemp:
        def __init__(self):
            self.allClients = []

    def getDaysClients(self, day, flags):
        todaysClients = []
        for client in self.allClients:
            for showUp in client.showUps:

                ShowingUp = True


                if showUp.day == day:
                    
                    for flagCheck in showUp.onFlags:
                        if flagCheck not in client.flags and flagCheck not in self.globalFlags:
                            ShowingUp = False
                            break

                    if ShowingUp:
                        self.todaysClients.append(showUp)


        return todaysClients

    game = gameTemp()
    genCharacters(game)

    requests = {}
    showups = {}
    possibleOrgans = {}
    i = 0

    for x in game.allClients:
        if not x.deathText:
            print(x.name, "lacks death text!")
        if not x.organUponHarvest:
            print(x.name, "lacks organ!")
        else:
            if x.organUponHarvest not in possibleOrgans:
                possibleOrgans[x.organUponHarvest] = 1
            else:
                possibleOrgans[x.organUponHarvest] += 1
            
        for y in x.showUps:
            i += 1
            if y.request not in requests:
                requests[y.request] = 1
            else:
                requests[y.request] += 1

            if not y.onFlags:
                if y.day not in showups:
                    showups[y.day] = 1
                else:
                    showups[y.day] += 1







                
    print(requests)
    print(showups)
    print(possibleOrgans)
    print("Total showups:", i)



def recursiveChoice(todaysClients, day):
    pass
