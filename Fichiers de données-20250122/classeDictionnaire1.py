import asyncio
import msvcrt
import os
import pathlib
import sys
import threading
import time


class DictionnaireV1:

    raw_text = "Nothing was inputed"
    isprocessed = False
    useV2 = False

    dictionnaire_counted = {}
    dictionnaire_ordered = {}

    ordered = []  # for v2 only

    verbose = False

    def __init__(self, text=None):
        self.raw_text = text

    def processe(self, text=None):
        self.isprocessed = False

        if text == None or len(text) == 0:
            text = self.raw_text
            self.raw_text = text

        self.text_to_counted(self, text)
        if self.useV2:
            self.counted_to_orderedv2(self)
        else:
            self.counted_to_ordered(self)
        if self.verbose:
            print("Counted : ")
            print(self.dictionnaire_counted)
            print("Ordered : ")
            print(self.dictionnaire_ordered)
        self.isprocessed = True

    def text_to_counted(self, text):
        splitInput = text.split()

        for item in splitInput:
            if self.dictionnaire_counted.__contains__(item):
                self.dictionnaire_counted[item] = self.dictionnaire_counted[item] + 1
            else:
                self.dictionnaire_counted[item] = 1

    def counted_to_ordered(self):
        counted = list(self.dictionnaire_counted.keys())
        ordered = []

        if self.verbose:
            print("Early counted:")
            print(counted)

        for word in counted:
            inserted = False

            for idx, current in enumerate(ordered):
                if word < current:
                    ordered.insert(idx, word)
                    inserted = True
                    break
            if not inserted:
                ordered.append(word)

        self.dictionnaire_ordered = ordered

        return

    def counted_to_orderedv2(self):

        dict1 = {
            k: self.dictionnaire_counted[k]
            for i, k in enumerate(self.dictionnaire_counted)
            if i % 2 == 0
        }
        dict2 = {
            k: self.dictionnaire_counted[k]
            for i, k in enumerate(self.dictionnaire_counted)
            if i % 2 != 0
        }

        t1 = threading.Thread(target=self.orderThread, args=(self, dict1))
        t2 = threading.Thread(target=self.orderThread, args=(self, dict2))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        self.dictionnaire_ordered = self.ordered

        return

    def orderThread(self, dict_counted):

        counted = list(dict_counted.keys())

        if self.verbose:
            print("Early counted:")
            print(counted)

        for word in counted:
            inserted = False

            for idx, current in enumerate(self.ordered):
                if word < current:
                    self.ordered.insert(idx, word)
                    inserted = True
                    break
            if not inserted:
                self.ordered.append(word)

        return


class Menu:

    MyDict = DictionnaireV1
    is_loading = False
    time1 = 0

    def __init__(self):
        self.MainMenu()

    def MainMenu(self):
        os.system("cls")

        print("1: load dictionnaire")
        print("2: load dictionnaire v2")
        print("3: afficher dictionnaire")
        print("4: recherche dun mot")
        print("5: quitter")

        valinput = chr(msvcrt.getch()[0])  # comme readkey

        if self.is_loading:
            print("Chargement en cours, attendez svp")
            while self.is_loading:
                time.sleep(0.5)

            input(
                "Chargement terminer en " + str(time.time() - self.time1) + " secondes"
            )

        if valinput == "1":
            self.ReadData()
        elif valinput == "3":
            self.AfficherDictionnaire()
        elif valinput == "4":
            self.RechercheMot()
        elif valinput == "5":
            exit()
        elif valinput == "2":
            self.ReadDataV2()
        else:
            print("Error pas compris")
            input("OK")
            self.MainMenu()

    def ReadDataV2(self):
        os.system("cls")

        self.MyDict.useV2 = True

        if self.is_loading:
            input("Chargement en cours, attendez svp")
            self.MainMenu()

        self.is_loading = True

        valinput = input("Nom du dictionnaire: ")

        t1 = threading.Thread(target=self.__LoadData, args=(valinput,))

        t1.start()

        # je join pas apres pcq aussinon sa fais pas en background

        input("Chargement du fichier en arrière-plan...")

        self.MainMenu()

    def ReadData(self):
        os.system("cls")

        self.MyDict.useV2 = False

        if self.is_loading:
            input("Chargement en cours, attendez svp")
            self.MainMenu()

        self.is_loading = True

        valinput = input("Nom du dictionnaire: ")

        t1 = threading.Thread(target=self.__LoadData, args=(valinput,))

        t1.start()

        # je join pas apres pcq aussinon sa fais pas en background

        input("Chargement du fichier en arrière-plan...")

        self.MainMenu()

    def __LoadData(self, path):  # execute as a thread
        if len(path.strip()) == 0:
            path = "corbeau.txt"  # default

        self.time1 = time.time()

        file_path = os.path.join(pathlib.Path(__file__).parent.resolve(), path)

        try:
            f = open(file_path, mode="r", encoding="utf-8")
            self.MyDict.raw_text = f.read()
            self.MyDict.processe(self.MyDict)
        except:
            input("Peu pas lire le fichier")  # je sais sa execute pas
        finally:
            self.is_loading = False

    def AfficherDictionnaire(self):
        if self.MyDict.isprocessed and self.is_loading == False:
            os.system("cls")
            self.__PrintDict(
                self.MyDict.dictionnaire_ordered, self.MyDict.dictionnaire_counted
            )
            self.MainMenu()
            pass
        else:
            input(
                "Dictionnaire nest toujour pas loader completement, reessayer plus tard"
            )
            self.MainMenu()

    def __PrintDict(self, textarray, countDict):
        CHECKLEN = 20

        if len(textarray) == 0:
            input("Text array is empty")
            return
        if len(countDict) == 0:
            input("Text dict is empty")
            return

        for i in range(len(textarray)):
            if i % CHECKLEN == CHECKLEN - 1:
                self.AskIfContinueShowing(False)
            print(
                "no:",
                i + 1,
                "est",
                textarray[i].ljust(20),
                "et apparait",
                countDict[textarray[i]],
                "nb de fois",
            )
        input("Done")

    def AskIfContinueShowing(self, rightAway):
        if rightAway:
            return
        print("Continue y:n")
        response = chr(msvcrt.getch()[0])
        if response == "y":
            return
        elif response == "n":
            self.MainMenu()
        else:
            self.AskIfContinueShowing(False)

    def RechercheMot(self):
        if self.MyDict.isprocessed and self.is_loading == False:
            os.system("cls")
            searchVal = input("la valure est: ")

            self.__PrintDict(
                [
                    x
                    for x in self.MyDict.dictionnaire_ordered
                    if x.find(searchVal) != -1
                ],
                {
                    key: value
                    for key, value in self.MyDict.dictionnaire_counted.items()
                    if key.find(searchVal) != -1
                },
            )
            self.MainMenu()
        else:
            input(
                "Dictionnaire nest toujour pas loader completement, reessayer plus tard"
            )
            self.MainMenu()


class testWrapper:

    myDict = DictionnaireV1

    def __init__(self):
        self.myDict.verbose = True
        self.myDict.processe(
            self.myDict,
            "Maitre Renard, par l'odeur alleche, Lui tint a peu pres ce langage : Maitre Corbeau, sur un arbre perche,Tenait en son bec un fromage.",
        )


Menu = Menu()

# test = testWrapper()

print()
print()
print("pas senser etre ici...")


# Est-ce que le nombre de mots et le nombre total d’occurrences sont les mêmes qu’avec un seul fil? Pourquoi?

# oui, le texte de depart est le meme donc sa ne peu pas changer, si sa change cest a cause dune erreure dans le code

# Quel problème survient avec l’utilisation de deux fils? Comment doit-on faire pour le corriger?

# en utulisant 2 fils on peu parfois pas avoir les valeures a la bonne place,ou si on lock pas asser, mais si on lock trop on sa ne sert plus a rien dudtuliser des thread different

# Est-ce que le temps total de traitement est plus rapide avec deux fils? Pourquoi?

# senser etre oui, pcq faire les > est fais en parralelle, moi sa change juste de 3-4 scondes parcontre
