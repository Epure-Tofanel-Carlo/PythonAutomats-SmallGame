from collections import deque

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
                 ct += 1                           # tinem minte cate sectiuni avem (useless btw)
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


def emulate_nfa(nfa, str):
    keys = list(nfa.keys())
    s_f = []
    s_c = deque()  # Storez in double queue starile curent si pozitia simbolului curent
    for stare in nfa[keys[1]]:  # Storez starea initiala si finala
        if 'S' in stare:
            s_c.append((stare.split(',')[0], 0))  # Dau append la starea initala si la 0 fiind pozitia simbolului curent
        if 'F' in stare:
            s_f.append(stare.split(',')[0])

    while s_c:  # Cat timp exista stari curent in queue
        state, pos = s_c.popleft()  # Iau prima stare si pozitia simbolului
        if pos == len(str):  # Daca am ajuns la finalul input-ului
            if state in s_f:  # Si ne aflam intr o stare finala atunci string-ul este acceptat
                return "Acceptat"
        else:  # Daca mai sunt simboluri de citit din string
            s = str[pos]  # luam urmatorul simbol
            for tranzitii in nfa[keys[2]]:  # Trecem prin lista de tranzitii
                tranzitii = tranzitii.split(',')
                if state == tranzitii[0] and (s == tranzitii[1] or tranzitii[1] == '*'):  # Daca tranzitia e valida
                    next_pos = pos + 1 if tranzitii[1] != '*' else pos
                    s_c.append((tranzitii[2], next_pos))  # Dam append la noua stare, si la urmatoarea pozitie in queue

    return "Respins"


fisier = input()
nfa = load_section(fisier)
print(nfa)
string = input()
print(emulate_nfa(nfa, string))
