# Graafialgoritmit syksy 2021
# Ohjelmointiharkkatyö 1
# Aapo Hetemaa

# Ainoa harkkatyössä tekemäni koodi on alla oleva funktio CountShortest. Kun
# sitä kutsuu oikeilla parametreilla, se palauttaa oikean tuloksen prujun
# tehtävän 2.6 mukaisesti


# Parametreina graafi G, solmujoukko B, lähtösolmu u, maalisolmu v
# Käytännössä funktio on hieman modattu BFS-algoritmi. Etäisyyksien
# tarkastelemisen lisäksi funktio pitää kirjaa siitä, montako joukossa B olevaa
# solmua on lyhimmällä polulla u:sta kuhunkin solmuun. Palauttaa tämän arvon
# solmulle v. Virhetilanteissa, tai jos jompaakumpaa solmua ei ole tai B on
# tyhjä joukko, palauttaa -1.
def CountShortest(G, B, u, v):

    dists = {}
    dists[u] = 0
    Q = [u]

    # dict, jossa jokaiseen solmuun liittyy solmusta s tulevan polun varrella
    # enimmillään olevien B-solmujen määrä
    max_Bnodes = {}
    max_Bnodes[u] = 0
    if u in B:
        max_Bnodes[u] = 1

    # Käytetään looppaussolmuina kirjaimia s ja w (u ja v jo käytössä)
    while Q:
        s = Q.pop(0)
        d = dists[s]
        try:
            for w in G.adj(s):
                if w not in dists:
                    dists[w] = d + 1
                    # Koska w:tä ei ole käyty läpi, sen Bnodes-arvo on sama
                    # kuin solmulla s tai yhtä suurempi (jos w on B:ssä)
                    max_Bnodes[w] = max_Bnodes[s]
                    if w in B:
                        max_Bnodes[w] += 1
                    Q.append(w)

                # Jos w on jo käyty läpi, tutkitaan, pitääkö kasvattaa siihen
                # asti olevien B-solmujen määrää nyt kun siihen tullaan
                # toista reittiä
                # Eli kasvatetaan, jos matka tätä kautta on yhtä suuri (ei edes
                # voi olla pienempi) ja
                # B-solmuja on tätä kautta yhtä paljon tai enemmän
                elif dists[w] == dists[s] + 1 and max_Bnodes[w] <= max_Bnodes[s]:
                    max_Bnodes[w] = max_Bnodes[s]
                    if w in B:
                        max_Bnodes[w] += 1

        except:
            pass

    # Jos v:hen ei ollenkaan polkua u:sta
    if v not in max_Bnodes:
        return -1

    return max_Bnodes[v]
