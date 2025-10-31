#  Escáner de Puertos Local (Python + Nmap)
  
Herramienta simple en Python para escanear puertos en una IP o dominio local, listar su estado, detectar el servicio y la versión cuando es posible. Pensado como proyecto educativo para practicar redes y técnicas básicas de ciberseguridad.

**Nota:** **¡** Este proyecto es **educativo**. No escanees equipos o redes que no te pertenezcan o para los que no tengas permiso explícito **!**

---

##  Características
- Validación básica de IP/domino y del rango/lista de puertos.
- Escaneo con `nmap` usando la opción `-sV` (detección de servicios/versión).
- Salida en consola con colores para facilitar lectura.
- Informes básicos por puerto (estado, servicio, versión).

---

##  Tecnologías
- Python 3.8+
- `python-nmap` (wrapper de Nmap)
- `colorama` (colores en consola)

---

##  Instalación (recomendada: entorno virtual)
1. Si quieres clonar el repositorio:
```bash
git clone https://github.com/sRichi18/port_scanner.git