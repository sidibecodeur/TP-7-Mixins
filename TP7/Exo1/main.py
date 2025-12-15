from datetime import datetime
import json
from abc import ABC, abstractmethod

class Horodatable:
    def horodatage(self):
        print(f"[LOG] Action a {datetime.now()}")

class Validable:
    def valider(self):
        if not getattr(self, "titre", None):
            raise ValueError("Titre manquant")
        print("Validation OK")

class Serializable:
    def to_json(self):
        def convert(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, list):
                return [convert(i) for i in obj]
            elif isinstance(obj, tuple):
                return tuple(convert(i) for i in obj)
            else:
                return obj
        dict_serializable = {k: convert(v) for k, v in self.__dict__.items()}
        return json.dumps(dict_serializable, indent=4, ensure_ascii=True)

class Historisable:
    def __init__(self, *args, **kwargs):
        self._historique = []
        super().__init__(*args, **kwargs)

    def add_history(self, action):
        self._historique.append((datetime.now(), action))

    def show_history(self):
        for date, action in self._historique:
            print(f"{date} | {action}")

class ObligatoireTitre(ABC):
    @abstractmethod
    def get_titre(self):
        pass

class Document(Horodatable, Validable, Serializable, Historisable, ObligatoireTitre):
    def __init__(self, titre, contenu):
        super().__init__()
        self.titre = titre
        self.contenu = contenu

    def get_titre(self):
        return self.titre

    def sauvegarder(self):
        self.horodatage()
        self.add_history("Horodatage effectue")
        self.valider()
        self.add_history("Validation effectuee")
        print(f"Document '{self.titre}' sauvegarde.")
        self.add_history(f"Document '{self.titre}' sauvegarde")

if __name__ == "__main__":
    doc = Document("Rapport", "Contenu important")
    doc.sauvegarder()
    print("\n=== JSON ===")
    print(doc.to_json())
    print("\n=== HISTORIQUE ===")
    doc.show_history()
