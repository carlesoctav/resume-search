from collections import defaultdict



adik = {
    "saya": 1, 
    "babi": "ayam",
    "sys": ['ayam'],
}

dik = defaultdict(lambda: "", adik)

print(dik["babi"])
print(dik["konci"])
print(dik["sys"])
print(dik["sys"]["Cin"])
adik["wah"]