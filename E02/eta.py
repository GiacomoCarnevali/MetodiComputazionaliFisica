import datetime
from datetime import datetime, timedelta
data = input("Inserisci la tua data di nascita ")
datenow = datetime.now()
mydate = datetime.strptime(data, "%d-%m-%Y")
timediff = datenow - mydate
timediff_year = datenow.year - mydate.year
timediff_sec = timediff.total_seconds()
age_secs = int(timediff_sec)
age_days = int(timediff_sec/(60*60*24))
print("Diff anni {:}".format(timediff_year))
print("Diff giorni {:}".format(age_days))
print("Diff secondi {:} ".format(timediff_sec))
