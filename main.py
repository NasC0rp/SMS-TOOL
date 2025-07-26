import os
import time
import hashlib
from colorama import Fore, init

init(autoreset=True)

HISTORIQUE = "envoyes.txt"
LISTE = "liste.txt"

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def center(text, width=80):
    return "\n".join(line.center(width) for line in text.splitlines())

def afficher_logo():
    logo = f"""{Fore.MAGENTA}
  ___ __  __ ___   _____ __   __  _    
 / __|  \/  / __| |_   _/  \ /  \| |   
 \__ \ |\/| \__ \   | || () | () | |__ 
 |___/_|  |_|___/   |_| \__/ \__/|____|
 """
    titre = f"{Fore.YELLOW}SMS SENDER BY N4S"
    clear()
    print(center(logo))
    print(center(titre))
    print("\n")

def menu():
    print(center(f"{Fore.CYAN}{'-'*30} MAIN MENU {'-'*30}"))
    print(center(f"{Fore.GREEN}1. SEND SMS"))
    print(center(f"{Fore.GREEN}2. SEND MULTI SMS"))
    print(center(f"{Fore.RED}0. EXIT"))
    print(center(f"{Fore.CYAN}{'-'*76}"))

def hasher_texte(txt):
    return hashlib.md5(txt.encode()).hexdigest()

def charger_historique():
    if not os.path.exists(HISTORIQUE):
        return set()
    with open(HISTORIQUE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def sauvegarder_envoi(numero, message_hash):
    with open(HISTORIQUE, "a") as f:
        f.write(f"{numero}|{message_hash}\n")

def envoyer_sms(numeros, message, eviter_doublons=True):
    message_hash = hasher_texte(message)
    deja_envoyes = charger_historique() if eviter_doublons else set()
    print(f"\n{Fore.CYAN}📤 Sending SMS (simulation)...\n")
    for numero in set(numeros):
        identifiant = f"{numero}|{message_hash}"
        if identifiant in deja_envoyes:
            print(f"{Fore.YELLOW}⚠️ Already sent to {numero}, skipped.")
            continue
        print(f"{Fore.GREEN}✅ SMS sent to {numero} (simulated)")
        sauvegarder_envoi(numero, message_hash)
        time.sleep(1)
    print(f"\n{Fore.MAGENTA}✔️ Process completed.\n")
    input(f"{Fore.CYAN}Press Enter to return to menu...")

def envoi_manuel():
    message = input(f"{Fore.GREEN}📝 Message to send: ")
    nums = input(f"{Fore.YELLOW}📞 Numbers (comma separated): ")
    numeros = [n.strip() for n in nums.split(",") if n.strip()]
    envoyer_sms(numeros, message, eviter_doublons=False)

def envoi_liste():
    if not os.path.exists(LISTE):
        print(f"{Fore.RED}❌ File liste.txt not found.")
        input("Press Enter to return...")
        return
    with open(LISTE, "r") as f:
        numeros = [line.strip() for line in f if line.strip()]
    if not numeros:
        print(f"{Fore.YELLOW}⚠️ No valid numbers found.")
        input("Press Enter to return...")
        return
    message = input(f"{Fore.GREEN}📝 Message to send to entire list: ")
    envoyer_sms(numeros, message, eviter_doublons=True)

def main():
    while True:
        afficher_logo()
        menu()
        choix = input(f"\n{Fore.BLUE}🎮 Choose an option: ")
        if choix == "1":
            envoi_manuel()
        elif choix == "2":
            envoi_liste()
        elif choix == "0":
            print(f"\n{Fore.RED}👋 Goodbye!")
            break
        else:
            print(f"{Fore.RED}❌ Invalid option.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
