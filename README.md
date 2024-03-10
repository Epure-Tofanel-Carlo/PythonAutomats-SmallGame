#Automate finite și automate pushdown în Python

Acest depozit GitHub conține implementări în Python ale unor automate finite deterministe (DFA), automate finite nedeterministe (NFA), automate pushdown (PDA) și un automat pushdown ipotetic care utilizează o listă în locul unei stive. Acestea sunt folosite într-un joc text-based despre explorarea unui castel.
# Conținutul Depozitului

  DFA.py: Implementarea unui Automat Fini Determinist.
  
  NFA.py: Implementarea unui Automat Fini Nedeterminist.
  
  PDA.py: Implementarea unui Automat Pushdown.
  
  GameWithLA: Jocul text-based despre explorarea unui castel, care utilizează mplementarea unui automat pushdown ipotetic care utilizează o Listă in loc de Stack


# Despre Automate

### DFA (Automat Fini Determinist)
DFA este un model de automat finit în care fiecare stare și simbol de intrare duce la exact o stare următoare.

### NFA (Automat Fini Nedeterminist)
NFA este similar cu DFA, dar diferă în sensul că poate avea mai multe stări următoare pentru o combinație dată de stare și simbol de intrare.

### PDA (Automat Pushdown)
PDA este un model mai complex care folosește o stivă pentru a gestiona simboluri intermediare, permițând recunoașterea unor limbi mai complexe.

### Automat Pushdown Ipotetic cu Listă (LA)
Această variantă a PDA folosește o listă în locul unei stive tradiționale, oferind o abordare diferită în procesarea simbolurilor și stărilor.

### Jocul Text based cu LA
GameWithLA.py este un joc text-based în care jucătorul explorează diferite camere ale unui castel folosind un LA, interacționând cu mediul prin comenzi simple bazate pe text. Jocul demonstrează utilizarea automatelor într-un context practic și interactiv.
