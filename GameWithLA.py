global_dict_adiacente = {"Entrance Hall": ["Dining Room","Armoury"],
               "Dining Room": ["Entrance Hall", "Treasury", "Kitchen"],
               "Kitchen": ["Pantry", "Dining Room"],
               "Armoury": ["Entrance Hall", "Throne Room", "Treasury"],
               "Treasury": ["Library","Dining Room","Armoury","Wizard's Study"],
               "Library": ["Treasury","Secret Exit"],
               "Pantry": ["Kitchen"],
               "Throne Room": ["Armoury", "Wizard's Study"],
               "Wizard's Study": ["Treasury","Secret Exit","Throne Room"],
               "Secret Exit": ["Wizard's Study", "Library"] }
global_dict_description = {"Entrance Hall": "The grand foyer of the Castle of Illusions",
               "Dining Room": "A room with a large table filled with an everlasting feast.",
               "Kitchen": "A room packed with peculiar ingredients.",
               "Armoury": "A chamber filled with antiquated weapons and armour.",
               "Treasury": "A glittering room overflowing with gold and gemstones.",
               "Library": "A vast repository of ancient and enchanted texts.",
               "Pantry": "A storage area for the Kitchen.",
               "Throne Room": "The command center of the castle.",
               "Wizard's Study": "A room teeming with mystical artifacts.",
               "Secret Exit": "The hidden passage that leads out of the Castle of Illusions."}

global_current_state = "Entrance Hall"
global_current_list = ["your clothes"]
global_flag = 0
def load_section(nume_fisier):
    fisier = nume_fisier
    try:
        sectiuni = {}

        f = open(fisier, 'r')
        ct = 0

        for linie in f:
            linie = linie.strip()  # dau trim
            if linie:  # ignor linii goale
                if linie[0] != '#':  # ignore commenturi
                    if '[' and ']' in linie and linie not in sectiuni:  # daca e section header
                        sectiuni[linie] = []
                        valoare = linie
                        ct += 1
                    else:
                        if ct != 0:
                            if linie not in sectiuni[valoare]:  # daca nu e section header, il adaug ca valoare mai sus
                                sectiuni[valoare].append(linie)

        f.close()
    except FileNotFoundError:
        return "File not found"

    # verific daca exista toate sectiunile de care am nevoie
    for section in ['[Alfabet]', '[ListAlphabet]', '[Stari]', '[Functia]', '[ListaInitiala]']:
        if section not in sectiuni or sectiuni[section] == []:
            return f"Sectiunea {section} lipseste"

    # daca exista * in alfabet, returnam eroare
    if '*' in sectiuni['[Alfabet]']:
        return "Alfabetul nu poate contine '*'"

    # verific daca exista o singura stare de start, si macar una de final
    start_states = [state for state in sectiuni['[Stari]'] if ',S' in state]
    final_states = [state for state in sectiuni['[Stari]'] if ',F' in state]
    if len(start_states) != 1:
        return "Ar trebui sa fie exact o singura stare initiala"
    if len(final_states) == 0:
        return "Ar trebui sa fie macar o singura stare finala"

    return sectiuni


def emulate_la(la, command):
    global global_current_state
    global global_current_list

    # scot informatiile din LA
    alphabet = la['[Alfabet]']

    if command not in alphabet:        # verific daca comanda este valida
        return "Respins, introdu o comanda corecta"
    if command == 'look':  # Daca comanda e look
        print(global_dict_description[global_current_state])  # Afisez descrierea
        print("You can see: " + ", ".join(global_dict_adiacente[global_current_state]))  # Afisez obiectele din camera
        return "Comanda efectuata cu succes"
    if command == 'inventory':  # Daca comanda e inventory
        print("You are carrying: " + ", ".join(global_current_list))  # Afisez lista de obiecte
        return "Comanda efectuata cu succes"
    list_alphabet = la['[ListAlphabet]']
    states = la['[Stari]']
    transitions = la['[Functia]']
    final_states = [state.split(',')[0] for state in states if 'F' in state]
    # Daca inca sunt simboluri de citit
    for transition in transitions:  # Trec prin lista de tranzitii
            src, a, list_symbol, dest, symbol_to_remove, symbol_to_add = transition.split(',')

            if global_current_state == src and command == a and (list_symbol in global_current_list or list_symbol == '*'):  # Daca tranzitia e valida

                if symbol_to_remove != '*':  # Daca tranzitia da remove la ceva din lista
                    global_current_list.remove(symbol_to_remove)

                if symbol_to_add != '*':  # Daca tranzitia adauga ceva in lista
                    global_current_list.append(symbol_to_add)

                print (dest)  # Afisez starea in care ajung

                global_current_state = dest  # Setez starea curenta

                if global_current_state in final_states:  # Daca am ajuns intr-o stare finala
                    if global_current_state == 'Secret Exit':
                     global global_flag
                     global_flag = 1
                     return "Comanda efectuata cu succes, ai gasit iesirea secreta si a scapat din castel"
                return "Comanda efectuata cu succes"

    return "Respins"

def joc():
    fisier = "Jocinfo"
    la = load_section(fisier)
    print(la)
    print("Bine ai venit in acest joc!")
    ok = True
    while ok:
        print("Te rog sa introduci o comanda! ")
        comanda = input()
        if comanda == "exit":
            return  "Ai iesit din joc"
        print(emulate_la(la,comanda))
        if global_flag == 1:
            return "Ai iesit din joc"
        print("Momentan te afli in " + global_current_state)

joc()