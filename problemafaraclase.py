import json
import random
from datetime import datetime

# Crearea datelor pentru clienți
def generate_clients(number_of_clients=50):
    clients = []
    first_names = ["Ion", "Maria", "Andrei", "Elena", "Mihai", "Ana", "George", "Ioana", "Alexandru", "Cristina"]
    last_names = ["Popescu", "Ionescu", "Popa", "Dumitrescu", "Stan", "Dinu", "Georgescu", "Marin", "Stoica", "Florea"]
    
    for i in range(number_of_clients):
        client = {
            "id": i + 1,
            "nume": random.choice(last_names),
            "prenume": random.choice(first_names),
            "iban": f"RO49AAAA{''.join([str(random.randint(0, 9)) for _ in range(16)])}",
            "sold": round(random.uniform(100, 20000), 2)
        }
        clients.append(client)
    
    return clients

# Salvarea datelor în fișier JSON
def save_to_json(clients, filename="clients_data.json"):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(clients, file, indent=4, ensure_ascii=False)
    print(f"Datele au fost salvate în fișierul {filename}")

# Generarea raportului pentru clienții cu sold sub 10.000 lei
def generate_report(clients, threshold=10000, report_filename="report_low_balance.txt"):
    low_balance_clients = [client for client in clients if client["sold"] < threshold]
    
    with open(report_filename, 'w', encoding='utf-8') as file:
        file.write(f"Raport generat la data: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
        file.write(f"Clienți cu sold sub {threshold} lei\n")
        file.write("=" * 80 + "\n\n")
        
        for client in low_balance_clients:
            file.write(f"ID: {client['id']}\n")
            file.write(f"Nume complet: {client['nume']} {client['prenume']}\n")
            file.write(f"IBAN: {client['iban']}\n")
            file.write(f"Sold: {client['sold']} lei\n")
            file.write("-" * 40 + "\n")
    
    print(f"Raport generat în fișierul {report_filename}")
    print(f"Numărul total de clienți cu sold sub {threshold} lei: {len(low_balance_clients)}")
    
    return low_balance_clients

# Funcție pentru afișarea clienților în consolă
def display_clients(clients, max_to_display=50):
    print("\nPrimii clienți din baza de date:")
    for i, client in enumerate(clients[:max_to_display]):
        print(f"{i+1}. {client['nume']} {client['prenume']} - Sold: {client['sold']} lei")
    
    if len(clients) > max_to_display:
        print(f"... și încă {len(clients) - max_to_display} clienți.")

# Rularea programului
if __name__ == "__main__":
    print("Generare date pentru clienții băncii...")
    clients_data = generate_clients(50)  # Generăm 50 de clienți aleatori
    
    # Salvarea în JSON
    save_to_json(clients_data)
    
    # Afișarea câtorva clienți
    display_clients(clients_data)
    
    # Generarea raportului
    low_balance_clients = generate_report(clients_data)
    
    print("\nRaportul a fost generat cu succes!")