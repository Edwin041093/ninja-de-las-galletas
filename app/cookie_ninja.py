from flask import jsonify
from app.cookie_importer import cargar_cookies_archivo, exportar_a_navegador
from app.cookie_classifier import clasificar_cookies
from app.cloudflare_bypass import detectar_cloudflare, generar_headers_ninja
from app.captcha_solver import resolver_captcha

def ejecutar_desde_web(data):
    ruta_archivo = data.get("ruta_archivo")
    url_objetivo = data.get("url_objetivo")
    sitekey = data.get("sitekey")
    usar_captcha = data.get("usar_captcha")

    resultado = {}

    cookies = cargar_cookies_archivo(ruta_archivo)
    resultado["cookies_cargadas"] = len(cookies)

    clasificadas = clasificar_cookies(cookies)
    resultado["clasificacion"] = True

    protegido = detectar_cloudflare(url_objetivo)
    resultado["cloudflare"] = protegido

    if usar_captcha == "Sí" and sitekey:
        captcha_resultado = resolver_captcha(data.get("api_key"), sitekey, url_objetivo)
        resultado["captcha_token"] = captcha_resultado.get("captcha_token")
        resultado["captcha_status"] = captcha_resultado.get("captcha_status")

    resultado["headers"] = generar_headers_ninja()
    exportar_a_navegador(clasificadas)

    return jsonify(resultado)

def flujo_ninja():
    print("\n⚔️ Iniciando Cookie Ninja...\n")

    ruta_archivo = input("📥 Ruta del archivo de cookies (ej. sample_cookie.json): ").strip()
    url_objetivo = input("🌐 URL del sitio objetivo: ").strip()
    usar_captcha = input("🔐 ¿Deseas resolver CAPTCHA si existe? (s/n): ").strip().lower()

    resultado = {}

    cookies = cargar_cookies_archivo(ruta_archivo)
    print(f"[✓] Se cargaron {len(cookies)} cookies")

    cookies_clasificadas = clasificar_cookies(cookies)
    print("[✓] Clasificación completada")

    protegido = detectar_cloudflare(url_objetivo)
    if protegido:
        print("[🛡️] El sitio usa Cloudflare")
        resultado["cloudflare"] = True
        headers = generar_headers_ninja()
        print(f"[🧠] Headers ninja preparados: {headers}")
        resultado["headers"] = headers

        if usar_captcha == "s":
            site_key = input("🔑 Clave pública del CAPTCHA (sitekey): ").strip()
            api_key = input("🔐 Clave API de 2Captcha: ").strip()
            captcha_resultado = resolver_captcha(api_key, site_key, url_objetivo)
            resultado["captcha_token"] = captcha_resultado.get("captcha_token")
            resultado["captcha_status"] = captcha_resultado.get("captcha_status")
            print(f"[📋] Estado CAPTCHA: {resultado['captcha_status']}")
            if resultado["captcha_token"]:
                print(f"[✓] Token recibido: {resultado['captcha_token']}")
    elif protegido is False:
        print("[✅] El sitio no usa protección Cloudflare")
    else:
        print("[✗] No se pudo detectar protección en el sitio")

    exportar_a_navegador(cookies_clasificadas)
    print("\n🎯 Flujo ninja completado")

if __name__ == "__main__":
    flujo_ninja()
