# Graafialgoritmit syksy 2021
# Ohjelmointiharkkatyö 3
# Aapo Hetemaa


# Kapulapeliprojektisssa tavoitteena on tutkia jotenkin annetun graafin G
# solmujen sentraalisuussuhteita, ja asettaa ne sen perusteella järjestykseen.

# Tässä on tarkoitus soveltaa Page Rank -algoritmia

# Ohjelman voi testata antamalla main-funktion graafille tiedostonimen. Kapula-
# ralli-funktion kutsussa voi testata erilaisia parametreja. Niiden merkitys on
# selitetty alla funktion kuvauksessa.
# Testaaminen vaatii, että numpy-kirjasto on asennettuna, jotta sen importtaus
# onnistuu.
# Varsinainen työ tapahtuu kapularalli-funktiossa.

from graafi3 import Graph
import numpy as np

# Funktio Hyödyntää Page Rank -algoritmia ja asettaa graafin G solmut "tärkeys"
# järjestykseen.
# isWeighted on bool-arvo, joka kertoo, onko graafin mahdolliset
# painotukset tarkoitus ottaa huomioon pelissä. Painotetulle graafille voidaan
# myös asettaa arvoksi False, jolloin kaikki kaaret painotetaan yhtä
# arvokkaiksi. Kuitenkin, jos painottamattomalle graafille asetetaan True, niin
# ohjelma kaatuu.
# d on "hyppytodennäköisyys", todnäk sille, että kapula arvotaan tasajakauman
# kautta kokonaan uudelle solmulle. Epsilon on pieni luku, jota käytetään
# sen tutkimiseen, milloin iteroinnin voi lopettaa, ts. milloin jakauma ei
# enää muutu juurikaan. Testeissä hyvin toimivat ainakin oletusarvot d = 0.001,
# epsilon = 0.000001 (miljoonasosa). Näillä iteraatiokertoja tuli isommillakin
# testigraafeilla (satoja solmuja) vain joitain kymmeniä.
# Funktio palauttaa graafin G solmut listassa Page Rank -algoritmin mukaisessa
# tärkeysjärjestyksessä. Tämä on samalla kapularallipelin mukainen
# voittotodennäköisyysjärjestys.
# Funktio olettaa, että G:n solmut ovat luonnollisia lukuja alkaen 1:stä, koska
# solmujen nimiä käytetään suoraan numpy arrayn indeksointiin
def kapularalli(G, isWeighted=False, d=0.001, epsilon=0.000001):
    # Luodaan kytkentämatriisi, jossa ykkösen tilalla aina kaaren paino
    vertexnum = len(G.V)
    A = np.zeros((vertexnum, vertexnum))
    for u in G.V:
        for v in G.AL[u]:
            # Tässä oletuksena, että solmut ovat lukuja alkaen 1:stä
            # => voidaan indeksoida suoraan matriisiin. Eli rivi u, sarake v
            # arvo 1 => kaari (u,v)
            # Jos painotettu, annetaan kaaripainon arvo
            if isWeighted:
                A[u-1, v-1] = G.W[(u, v)]
            # Jos ei, painona 1
            else:
                A[u - 1, v - 1] = 1
    # Kytkentämatriisi alustetaan todnäkmatriisiksi
    M = np.zeros((vertexnum, vertexnum))
    for rownum in range(vertexnum):
        weightsum = np.sum(A[rownum, :])
        M[rownum, :] = A[rownum, :] / weightsum
    M = np.transpose(M)

    # Ja iterointi
    # todnäkvektori aluksi tasajakaumalla
    x0 = np.ones((vertexnum, 1)) / vertexnum
    x_prev = np.ones((vertexnum, 1)) / vertexnum
    print(x_prev)

    # Kunnes erotuksen normi on pieni
    iterate = True
    i = 1
    while iterate:
        x = np.multiply(d, x0) + np.multiply((1 - d), np.matmul(M, x_prev))
        # Seuraavat 2 riviä testitulosteita => helppo seurata edistymistä
        print("Iteration " + str(i) + ": ")
        print(np.transpose(x))
        i += 1
        iterate = np.linalg.norm(x - x_prev) >= epsilon
        x_prev = x

    # Järjestetään solmut todnäkvektorin jakauman mukaan
    nodes_in_order = []
    for u in range(vertexnum):
        maxnode = np.argmax(x)
        # Poistetaan se
        x[maxnode] = -1
        # Lisätään listaan oikeiden solmujen nimet
        nodes_in_order.append(maxnode + 1)
    return nodes_in_order




def main():
    G = Graph("kapula_testiG2")
    nodes = kapularalli(G)
    print(nodes)

main()




