import requests

def detectar_cloudflare(url):
    try:
        response = requests.get(url, timeout=5)
        server = response.headers.get("Server", "").lower()
        if "cloudflare" in server or "__cfduid" in response.cookies:
            return True
        return False
    except requests.RequestException as e:
        print(f"[!] Error al conectar con {url}: {e}")
        return None

def generar_headers_ninja():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept-Language": "es-MX,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive"
    }

# Ejemplo de uso
if __name__ == "__main__":
    prueba_url = "https://example.com"  # Cambia esto por el sitio que quieras analizar
    resultado = detectar_cloudflare(prueba_url)
    if resultado is True:
        print("[✓] El sitio está protegido por Cloudflare")
        print("[>] Headers sugeridos para evasión:")
        print(generar_headers_ninja())
    elif resultado is False:
        print("[✓] El sitio NO usa Cloudflare")
    else:
        print("[✗] No se pudo analizar el sitio")
