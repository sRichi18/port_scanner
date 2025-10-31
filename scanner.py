import nmap
import re
from colorama import Fore, Style, init

init(autoreset=True)

#Verificar si la IP o dominio es valida
def valid_ip(ip):
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        return True
    if re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", ip):
        return True
    return False


#Verifica si el rango de puertos esta dento del limite 1-65535
def valid_ports(ports):
    if not ports:
        return False
    
    parts = re.split(r'[-,\s]+', ports)
    
    for part in parts:
        if not part.isdigit(): #Diferenciando si es un solo puerto o un rango de puertos
            try:
                port_num = int(part)
                if not (1 <= port_num <= 65535):
                    return False
            except ValueError:
                return False
            
    return True
            
            
#Estructura para escanear los puertos
def scan_target(ip: str, ports: str):
    nm = nmap.PortScanner()
    
    print(Fore.CYAN + f"\n Escaneando IP: {ip} en los puertos {ports}... \n")
    print(Fore.CYAN + " (Esto puede tardar un poco)")
    
    try:
        nm.scan(ip, ports, arguments='-sV')
    except nmap.PortScannerError as e:
        print(Fore.RED + f"Error de nmap {e}")
        return
    except Exception as e:
        print(Fore.RED + f"Error al escanear {e}")
        return
        
    for host in nm.all_hosts():
        print(Fore.MAGENTA + "=" * 50)
        print(Fore.MAGENTA + f"Host: {host} ({nm[host].hostname()})")
        print(Fore.BLUE + f"Estado: {nm[host].state()}")
        print("=" * 50)
        
        for proto in nm[host].all_protocols():
            print(Fore.YELLOW + f"\nProtocolo: {proto.upper()}")
            ports_list = nm[host][proto].keys()
            
            for port in sorted(ports_list):
                port_info = nm[host][proto][port]
                state = port_info["state"]
                
                service = port_info.get("name", "Desconocido")
                version = port_info.get("product", "")
                
                #Para resaltar los puertos abiertos
                if state == "open":
                    output_color = Fore.GREEN
                else:
                    output_color = Fore.WHITE + Style.DIM
                    
                print(output_color + f" -> Puerto {port}/{proto} esta {state}")
                
                if state == "open" or (version and state != "closed"):
                    print(Fore.CYAN + f"  [INFO] Servicio:{service.strip()} | Versión: {version.strip()}")
    
    print(Fore.CYAN + "\n Escaneo Completado. \n")
    
    

if __name__ == "__main__":
    print(Fore.YELLOW + "==== Ecaner de Puertos Local ====")
    target_ip = input("Introduce la direccion IP o dominio a escanear: ").strip()
    port_range = input("Introduce el rango de puertos (ejemplo 20-80): ").strip()
    
    #Validación de datos correctos
    if not valid_ip(target_ip):
        print(Fore.RED + "Error: La IP o Dominio ingresado no parece ser válido.")
    elif not valid_ports(port_range):
        print(Fore.RED + "Error: El rango/lista de puertos no es válido (debe ser entre 1 y 65535).")
    else:
        scan_target(target_ip, port_range)