settimana = ["Lunedi","Martedi","Mercoledi","Giovedi","Venerdi","Sabato","Domenica"]
ottobre = settimana[1:]+settimana*3+settimana[:4]
print(ottobre)
dict_ottobre = {}
for i in range(len(ottobre)):
    dict_ottobre.update({ i+1: ottobre[i] })

print()
print('Dizionario ', dict_ottobre)

