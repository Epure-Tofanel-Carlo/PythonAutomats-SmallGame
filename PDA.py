from collections import deque


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
        return "Fila nu exista"

    # verific daca exista toate sectiunile de care am nevoie
    for section in ['[Alfabet]', '[StackAlphabet]', '[Stari]', '[Functia]']:
        if section not in sectiuni or sectiuni[section] == []:
            return f"Sectiunea {section} nu este gasita"

    # verific daca exista o singura stare de start, si macar una de final
    start_states = [state for state in sectiuni['[Stari]'] if ',S' in state]
    final_states = [state for state in sectiuni['[Stari]'] if ',F' in state]
    if len(start_states) != 1:
        return "Ar trebui sa fie exact o singura stare initiala"
    if len(final_states) == 0:
        return "Ar trebui sa fie macar o stare finala"

    return sectiuni


def emulate_pda(pda, str):
    # scot informatiile din PDA
    alphabet = pda['[Alfabet]']
    stack_alphabet = pda['[StackAlphabet]']
    states = pda['[Stari]']
    transitions = pda['[Functia]']
    initial_state = [state.split(',')[0] for state in states if 'S' in state][0]
    final_states = [state.split(',')[0] for state in states if 'F' in state]

    # Initializez starile curente si stackul
    current_states = deque([(initial_state, 0, ['$'])])  # (state, position, stack)

    while current_states:  # Cat timp avem stari curente
        state, pos, stack = current_states.popleft()  # Iau prima stare, pozitia in string, si stackul
        # aici pentru exemplul din curs cu 0011, trebuie sa verific si daca stackul e gol cu and stack[-1] == '$', trn schimbat codul daca vrem ca stare finala sa fie si daca e goala stiva
        if pos == len(str) and state in final_states:  # Daca suntem intr o stare finala, la finalul string ului, returnam acceptat
            return "Acceptat"

        # Daca inca sunt simboluri de citit, sau daca sunt tranzitii epsilon
        s = str[pos] if pos < len(str) else '*'

        for transition in transitions:  # Trec prin lista de tranzitii
            src, a, b, c, dest = transition.split(',') # vezi curs

            if state == src and (s == a or a == '*') and (stack[-1] == b or b == '*'):  # Daca tranzitia e valida
                next_stack = stack.copy()

                if b != '*':  # Daca tranzitia nu e epsilon pe stack(vezi curs)
                    next_stack.pop()

                if c != '*':  # Daca tranzitia pune ceva pe stack
                    next_stack.append(c)

                next_pos = pos + 1 if a != '*' else pos  # Mergi la urmatorul simbol daca tranzitia nu e epsilon la string

                current_states.append((dest, next_pos, next_stack))  # Adauga noua stare, pozitia urmatoare, si noul stack

    return "Respins"


fisier = input()
pda = load_section(fisier)
print(pda)
string = input()
print(emulate_pda(pda, string))