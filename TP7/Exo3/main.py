from datetime import datetime
import copy


class ValidationMixin:
    def valider_titre(self, titre):
        if not titre or not titre.strip():
            raise ValueError("Le titre ne peut pas être vide.")
        return titre

class HistoriqueMixin:
    def __init__(self):
        self._historique = []

    def enregistrer_historique(self, ancienne_description):
        self._historique.append({
            "timestamp": datetime.now(),
            "ancienne_description": copy.deepcopy(ancienne_description)
        })

class JournalisationMixin:
    def journaliser(self, message):
        print(f"[Journal] {datetime.now()} - {message}")


class Tache(ValidationMixin, HistoriqueMixin, JournalisationMixin):
    def __init__(self, titre, description):
        HistoriqueMixin.__init__(self)  

        self.titre = self.valider_titre(titre)
        self.description = description
        self.date_creation = datetime.now()

        self.journaliser(f"Tache creee : '{self.titre}'")

    def mettre_a_jour(self, nouvelle_description):
        self.enregistrer_historique(self.description)

        self.description = nouvelle_description

        self.journaliser(f"Mise a jour de la tache '{self.titre}'")

    def afficher_historique(self):
        print("\n=== HISTORIQUE DES MODIFICATIONS ===")
        if not self._historique:
            print("Aucune modification enregistree.")
            return

        for h in self._historique:
            
            print(f"{h['timestamp']}  |  Ancienne description : {h['ancienne_description']}")


if __name__ == "__main__":
    t = Tache("Preparer rapport", "Version initiale du document")

    t.mettre_a_jour("Version 1 : Ajout du plan")
    t.mettre_a_jour("Version 2 : Ajout des explications detaillees")

    t.afficher_historique()
