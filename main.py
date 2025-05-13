import paramiko
import psutil
import time

# Configuration SSH
ip = "IP_DU_PC2"  # Remplacer par l'IP de la machine distante
username = "ton_utilisateur"
password = "mot_de_passe"

# Initialisation du client SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip, username=username, password=password)

def get_system_resources():
    # Commandes pour récupérer les ressources via SSH
    commands = {
        "CPU": "top -bn1 | head -n 3",  # Utilisation CPU
        "Memory": "free -h",            # Mémoire
        "Disk": "df -h"                 # Disque
    }
    
    print("=== Surveillance des ressources ===")
    for resource, cmd in commands.items():
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().decode()
        print(f">>> {resource}\n{output}")

def manage_services(action, service_name="apache2"):  # Exemple avec Apache
    # Vérifier ou redémarrer un service
    if action == "status":
        cmd = f"systemctl status {service_name}"
    elif action == "restart":
        cmd = f"sudo systemctl restart {service_name}"
    else:
        return
    
    stdin, stdout, stderr = client.exec_command(cmd)
    print(f">>> {action} {service_name}\n{stdout.read().decode()}")

# Exécution
try:
    get_system_resources()
    manage_services("status", "apache2")  # Vérifier l'état du service
    time.sleep(2)
    manage_services("restart", "apache2")  # Redémarrer le service
finally:
    client.close()