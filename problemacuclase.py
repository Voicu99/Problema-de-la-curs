import json
import random
from datetime import datetime

class Client:
    """Clasa pentru gestionarea informațiilor despre un client al băncii."""
    
    def __init__(self, id, nume, prenume, iban, sold):
        self.id = id
        self.nume = nume
        self.prenume = prenume
        self.iban = iban
        self.sold = sold
    
    def __str__(self):
        return f"{self.nume} {self.prenume} - Sold: {self.sold} lei"
    
    def to_dict(self):
        """Convertește obiectul Client într-un dicționar pentru serializare JSON."""
        return {
            "id": self.id,
            "nume": self.nume,
            "prenume": self.prenume,
            "iban": self.iban,
            "sold": self.sold
        }
    
    @classmethod
    def from_dict(cls, data):
        """Creează un obiect Client dintr-un dicționar."""
        return cls(
            id=data["id"],
            nume=data["nume"],
            prenume=data["prenume"],
            iban=data["iban"],
            sold=data["sold"]
        )


class BankDatabase:
    """Clasa pentru gestionarea bazei de date a clienților băncii."""
    
    def __init__(self):
        self.clients = []
    
    def add_client(self, client):
        """Adaugă un client în baza de date."""
        self.clients.append(client)
    
    def get_clients(self):
        """Returnează lista de clienți."""
        return self.clients
    
    def get_clients_below_threshold(self, threshold):
        """Returnează clienții cu sold sub pragul specificat."""
        return [client for client in self.clients if client.sold < threshold]
    
    def save_to_json(self, filename="clients_data.json"):
        """Salvează baza de date în format JSON."""
        data = [client.to_dict() for client in self.clients]
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Datele au fost salvate în fișierul {filename}")
    
    def load_from_json(self, filename="clients_data.json"):
        """Încarcă baza de date din format JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.clients = [Client.from_dict(client_data) for client_data in data]
            print(f"Datele au fost încărcate din fișierul {filename}")
        except FileNotFoundError:
            print(f"Fișierul {filename} nu există.")


class ClientGenerator:
    """Clasa pentru generarea aleatorie a clienților."""
    
    FIRST_NAMES = ["Ion", "Maria", "Andrei", "Elena", "Mihai", 
                   "Ana", "George", "Ioana", "Alexandru", "Cristina"]
    LAST_NAMES = ["Popescu", "Ionescu", "Popa", "Dumitrescu", "Stan", 
                  "Dinu", "Georgescu", "Marin", "Stoica", "Florea"]
    
    @classmethod
    def generate_iban(cls):
        """Generează un IBAN aleatoriu pentru România."""
        return f"RO49AAAA{''.join([str(random.randint(0, 9)) for _ in range(16)])}"
    
    @classmethod
    def generate_client(cls, id):
        """Generează un client cu date aleatorii."""
        return Client(
            id=id,
            nume=random.choice(cls.LAST_NAMES),
            prenume=random.choice(cls.FIRST_NAMES),
            iban=cls.generate_iban(),
            sold=round(random.uniform(100, 20000), 2)
        )
    
    @classmethod
    def generate_clients(cls, number_of_clients=50):
        """Generează un număr specificat de clienți aleatori."""
        return [cls.generate_client(i+1) for i in range(number_of_clients)]


class ReportGenerator:
    """Clasa pentru generarea rapoartelor."""
    
    @staticmethod
    def generate_balance_report(clients, threshold=10000, report_filename="report_low_balance.txt"):
        """Generează un raport pentru clienții cu sold sub pragul specificat."""
        low_balance_clients = [client for client in clients if client.sold < threshold]
        
        with open(report_filename, 'w', encoding='utf-8') as file:
            file.write(f"Raport generat la data: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
            file.write(f"Clienți cu sold sub {threshold} lei\n")
            file.write("=" * 80 + "\n\n")
            
            for client in low_balance_clients:
                file.write(f"ID: {client.id}\n")
                file.write(f"Nume complet: {client.nume} {client.prenume}\n")
                file.write(f"IBAN: {client.iban}\n")
                file.write(f"Sold: {client.sold} lei\n")
                file.write("-" * 40 + "\n")
        
        print(f"Raport generat în fișierul {report_filename}")
        print(f"Numărul total de clienți cu sold sub {threshold} lei: {len(low_balance_clients)}")
        
        return low_balance_clients


class BankingApp:
    """Clasa principală a aplicației bancare."""
    
    def __init__(self):
        self.database = BankDatabase()
    
    def generate_test_data(self, number_of_clients=50):
        """Generează date de test pentru aplicație."""
        print(f"Generare date pentru {number_of_clients} clienți ai băncii...")
        clients = ClientGenerator.generate_clients(number_of_clients)
        for client in clients:
            self.database.add_client(client)
    
    def display_clients(self, max_to_display=50):
        """Afișează clienții în consolă."""
        clients = self.database.get_clients()
        
        print("\nPrimii clienți din baza de date:")
        for i, client in enumerate(clients[:max_to_display]):
            print(f"{i+1}. {client}")
        
        if len(clients) > max_to_display:
            print(f"... și încă {len(clients) - max_to_display} clienți.")
    
    def run(self):
        """Rulează aplicația."""
        # Generare date
        self.generate_test_data(50)
        
        # Salvare în JSON
        self.database.save_to_json()
        
        # Afișare clienți
        self.display_clients()
        
        # Generare raport
        ReportGenerator.generate_balance_report(self.database.get_clients())
        
        print("\nRaportul a fost generat cu succes!")


if __name__ == "__main__":
    app = BankingApp()
    app.run()