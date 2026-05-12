"""
Cliente de consola para interactuar con API PFO 2 Leiva Iván Luis.
Permite registrar usuarios, hacer login y ver la página de tareas.
"""

import requests

URL_BASE = "http://localhost:5000"


def registrar():
    usuario = input("Nombre de usuario: ").strip()
    contrasena = input("Contraseña: ").strip()

    respuesta = requests.post(
        f"{URL_BASE}/registro",
        json={"usuario": usuario, "contraseña": contrasena}
    )
    print(f"\n[Status {respuesta.status_code}] {respuesta.json()}\n")


def login():
    usuario = input("Nombre de usuario: ").strip()
    contrasena = input("Contraseña: ").strip()

    respuesta = requests.post(
        f"{URL_BASE}/login",
        json={"usuario": usuario, "contraseña": contrasena}
    )
    print(f"\n[Status {respuesta.status_code}] {respuesta.json()}\n")


def ver_tareas():
    respuesta = requests.get(f"{URL_BASE}/tareas")
    print(f"\n[Status {respuesta.status_code}]")
    print("HTML recibido del servidor (primeros 300 caracteres):")
    print(respuesta.text[:300] + "...\n")


def menu():
    while True:
        print("=" * 40)
        print(" CLIENTE - Sistema de Gestión de Tareas")
        print("=" * 40)
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver /tareas")
        print("4. Salir")
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            print("Chau!")
            break
        else:
            print("Opción no válida.\n")


if __name__ == "__main__":
    try:
        menu()
    except requests.exceptions.ConnectionError:
        print("\nError: no se pudo conectar al servidor.")
        print("Asegurate de tener corriendo 'python servidor.py' en otra terminal.")
