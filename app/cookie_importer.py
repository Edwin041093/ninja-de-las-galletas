import json
from app.cookie_classifier import clasificar_cookies

def cargar_cookies_archivo(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
        try:
            cookies = json.loads(contenido)
        except json.JSONDecodeError:
            cookies = []
            for linea in contenido.splitlines():
                if "=" in linea:
                    nombre, valor = linea.strip().split("=", 1)
                    cookies.append({"name": nombre, "value": valor})
        return cookies

def exportar_a_navegador(cookies):
    formato = []
    for c in cookies:
        formato.append({
            "name": c["name"],
            "value": c["value"],
            "domain": c.get("domain", ".example.com"),
            "path": "/",
            "secure": False,
            "httpOnly": False,
            "tipo": c.get("tipo", "desconocido")  # ahora incluye tipo
        })
    with open("cookies_ninja_export.json", "w", encoding='utf-8') as f:
        json.dump(formato, f, indent=4, ensure_ascii=False)
    print("[✓] Cookies clasificadas y exportadas exitosamente")

# Ejemplo de uso
if __name__ == "__main__":
    ruta = "sample_cookie.json"
    cookies = cargar_cookies_archivo(ruta)
    cookies_clasificadas = clasificar_cookies(cookies)
    exportar_a_navegador(cookies_clasificadas)
