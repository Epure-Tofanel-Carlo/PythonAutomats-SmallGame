import time

def load_section(nume_fisier):
    fisier = nume_fisier
    try:

      sectiuni = {}

      f = open(fisier, 'r')
      ct = 0

      for linie in f:
          linie = linie.strip()                    # scoatem \n din text
          if linie:                                 # ignoram liniile goale altfel da eroare
           if linie[0] != '#':                      # ignoram commenturile
              if '[' and ']' in linie and linie not in sectiuni:             # daca e section header, adaugam in dictionar ca si key, contorizam
                 sectiuni[linie] = []
                 valoare = linie
                 ct += 1                           # tinem minte cate sectiuni avem
              else:
                  if ct != 0:
                    if linie not in sectiuni[valoare]:   # daca nu e section header, adaugam ca si value in key-ul precedent
                      sectiuni[valoare].append(linie)

      f.close()
    except FileNotFoundError:
        return "Nu exista acest fisier"
    if '[Alfabet]' not in sectiuni or sectiuni['[Alfabet]'] == []:      # Verificam daca avem alfabet
        return "Nu avem Alfabet"
    if '[Stari]' not in sectiuni or len(sectiuni['[Stari]']) == []:     # Verificam daca avem stari
        return "Nu avem Stari"
    flag1 = 0
    flag2 = 0
    cheie = '[Stari]'
    for stare in sectiuni[cheie]:                                       # Verificam daca avem stare initiala si/sau finala
        stare = stare.split(',')                                        # & daca avem mai mult de o stare initiala
        if 'S' in stare:
            flag1 +=1
        if 'F' in stare:
            flag2 = 1
    if flag2 == 0:
        return "Nu avem stare finala"
    if flag1 != 1:
        return "Nu avem sau avem mai mult de o stare initiala"
    if '[Functia]' not in sectiuni:      # Verificam daca avem functia sau header-ul in sine
        return "Nu avem Functia"

    return sectiuni


def emulate_dfa(dfa, str):
    keys = list(dfa.keys())
    s_f = []
    for stare in dfa[keys[1]]:              #salvam starea initiala si starea finala
        if 'S' in stare:
            s_c = stare.split(',')[0]
        if 'F' in stare:
            s_f.append(stare.split(',')[0])
    for s in str:                               # trecem prin fiercare simbol al stringului
        if s in dfa[keys[0]]: # dfa[alfabet]
            for tranzitii in dfa[keys[2]]: # dfa[functie]      # trecem prin lista noastra de tranzitii, verificam tranzitiile si o luam pe prima
                tranzitii = tranzitii.split(',')               # valida si apoi schimbam starea initiala
                if s_c == tranzitii[0] and s == tranzitii[1]:
                    s_c = tranzitii[2]
                    break

    if s_c in s_f:                               # daca starea curenta corespunde cu starea finala memorata initial, automatul accepta cuvantul
        return "Acceptat"
    else:
        return "Respins"

fisier = input()
dfa = load_section(fisier)
print(dfa)
string = input()
emulate_dfa(dfa, string)
'''start = time.time()'''
'''
for i in range(1000000):
    emulate_dfa(dfa, string)
print(time.time() - start)
'''