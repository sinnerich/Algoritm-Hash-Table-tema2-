import pandas as pd
import random
import hashlib
from collections import defaultdict

# Dicționar de nume masculine și feminine
nume_masculine = ["Andrei", "Mihai", "Gabriel", "Alexandru", "Cristian"]
nume_feminine = ["Maria", "Elena", "Ioana", "Andreea", "Gabriela"]

# Distribuția județelor (simplificată pentru exemplu)
judete = [f"{i:02d}" for i in range(1, 53)]  # Coduri județe 01-52
populatie_judete = [random.randint(1, 100) for _ in judete]  # Distribuție simplă

# Funcție pentru generarea unui CNP valid
def genereaza_cnp():
    sex = random.choice([1, 2])  # 1: Bărbat, 2: Femeie
    anul_nasterii = random.randint(1900, 2022)
    secol = 1 if anul_nasterii < 2000 else 2
    sex += (secol - 1) * 2

    aa = f"{anul_nasterii % 100:02d}"  # Anul nașterii
    ll = f"{random.randint(1, 12):02d}"  # Luna nașterii
    zile_in_luna = [31, 29 if int(aa) % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    zz = f"{random.randint(1, zile_in_luna[int(ll) - 1]):02d}"  # Ziua nașterii

    judet = random.choices(judete, weights=populatie_judete, k=1)[0]  # Județ
    nnn = f"{random.randint(0, 999):03d}"  # Număr unic

    cnp_fara_c = f"{sex}{aa}{ll}{zz}{judet}{nnn}"  # Fără cifra de control
    cifre_control = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    suma_control = sum(int(cnp_fara_c[i]) * cifre_control[i] for i in range(12))
    c = suma_control % 11
    if c == 10:
        c = 1

    return cnp_fara_c + str(c)

# Generare 10.000 de CNP-uri și asocierea de nume (redus pentru performanță)
cnp_nume = []
for _ in range(10_000):
    cnp = genereaza_cnp()
    sex = int(cnp[0])
    nume = random.choice(nume_masculine if sex in [1, 3, 5, 7] else nume_feminine)
    cnp_nume.append((cnp, nume))

# Crearea structurii hash
hash_table = defaultdict(list)

# Funcție de hashing (SHA-256, cu index maxim 1000)
def hash_function(cnp):
    return int(hashlib.sha256(cnp.encode()).hexdigest(), 16) % 1000

# Popularea structurii hash
for cnp, nume in cnp_nume:
    index = hash_function(cnp)
    hash_table[index].append((cnp, nume))

# Căutare a 1.000 de CNP-uri
cnp_de_cautat = random.sample(cnp_nume, 1000)  # Selectăm 1.000 de CNP-uri
rezultate_cautare = []

for cnp, nume in cnp_de_cautat:
    index = hash_function(cnp)
    lista = hash_table[index]
    iteratii = 0
    for item in lista:
        iteratii += 1
        if item[0] == cnp:
            rezultate_cautare.append({"CNP": cnp, "Nume": nume, "Iteratii": iteratii})
            break

# Creare tabel Pandas
df_rezultate = pd.DataFrame(rezultate_cautare)

# Salvăm tabelul într-un fișier Excel
df_rezultate.to_excel("rezultate_cnp.xlsx", index=False)
print("Rezultatele au fost salvate în fișierul 'rezultate_cnp.xlsx'.")
