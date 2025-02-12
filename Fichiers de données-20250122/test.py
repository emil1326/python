thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}
import time
import threading

temps = time.perf_counter()

print(temps)

print(thisdict["brand"])

thisdict = {}

myinput = "bonjour, cesi est une entrer et cesi est la meme entrer"

splitInput = myinput.split()

for item in splitInput:
    if thisdict.__contains__(item):
        thisdict[item] = thisdict[item] + 1
    else:
        thisdict[item] = 1
        
print(thisdict)


