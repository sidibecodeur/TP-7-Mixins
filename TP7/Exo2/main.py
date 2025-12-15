import json
import csv
from datetime import datetime

class Serializable:
    def to_json(self):
        def convert(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, list):
                return [convert(i) for i in obj]
            elif isinstance(obj, tuple):
                return tuple(convert(i) for i in obj)
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            else:
                return obj
        dict_serializable = {k: convert(v) for k, v in self.__dict__.items()}
        return json.dumps(dict_serializable, ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls, json_str):
        return cls(**json.loads(json_str))

class Historisable:
    def __init__(self, *args, **kwargs):
        self.historique = []
        super().__init__(*args, **kwargs)

    def enregistrer_etat(self):
        self.historique.append((datetime.now(), self.__dict__.copy()))

class Journalisable:
    def journaliser(self, message):
        print(f"[Journal] {datetime.now()}: {message}")

class Horodatable:
    def horodatage(self):
        print(f"[Horodatage] {datetime.now()}")

class CsvExportable:
    def to_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.__dict__.keys())
            writer.writerow(self.__dict__.values())

class XmlExportable:
    def to_xml(self):
        xml = "<objet>\n"
        for k, v in self.__dict__.items():
            xml += f"  <{k}>{v}</{k}>\n"
        xml += "</objet>"
        return xml

class Contrat(Serializable, Historisable, Journalisable, Horodatable, CsvExportable, XmlExportable):
    def __init__(self, id, description):
        super().__init__()
        self.id = id
        self.description = description

    def modifier(self, nouvelle_desc):
        self.journaliser(f"Modification du contrat {self.id}")
        self.enregistrer_etat()
        self.description = nouvelle_desc

if __name__ == "__main__":
    c = Contrat(1, "Initial")
    c.horodatage()
    c.modifier("Révisé")

    print("\n=== JSON ===")
    print(c.to_json())

    print("\n=== XML ===")
    print(c.to_xml())

    print("\n=== Export CSV ===")
    c.to_csv("contrat.csv")
    print("Fichier CSV créé : contrat.csv")

    print("\n=== HISTORIQUE ===")
    for moment, etat in c.historique:
        print(f"{moment} → {etat}")
