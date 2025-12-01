from ia import IA;
from os import path


dossier_eval = path.join(".", "dataset", "eval")
dossier_train = path.join(".", "dataset", "train")
dossier_sauvegarde = path.join("ia_model", "gab_ai.pt")
ia = IA(dossier_sauvegarde, False)


#ia.entrainer(dossier_train)
ia.evaluer(dossier_eval)

print("fin")