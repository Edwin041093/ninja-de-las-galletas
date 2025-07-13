import requests
import time

def resolver_captcha(api_key, site_key, url_objetivo):
    print("[>] Enviando solicitud a 2Captcha...")

    payload = {
        "key": api_key,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": url_objetivo,
        "json": 1
    }

    respuesta = requests.post("http://2captcha.com/in.php", data=payload).json()

    if respuesta.get("status") != 1:
        print("[✗] Error en la solicitud a 2Captcha:", respuesta.get("request"))
        return {
            "captcha_token": None,
            "captcha_status": "Solicitud a 2Captcha fallida"
        }

    captcha_id = respuesta.get("request")
    time.sleep(5)  # espera inicial

    for intento in range(30):  # hasta ~60 segundos con sleep(2)
        print(f"[...] Esperando ({intento+1}/30)")
        time.sleep(2)

        result = requests.get("http://2captcha.com/res.php", params={
            "key": api_key,
            "action": "get",
            "id": captcha_id,
            "json": 1
        }).json()

        if result.get("status") == 1:
            print("[✓] CAPTCHA resuelto")
            return {
                "captcha_token": result.get("request"),
                "captcha_status": "Resuelto exitosamente"
            }

    print("[✗] No se resolvió el CAPTCHA a tiempo")
    return {
        "captcha_token": None,
        "captcha_status": "No se resolvió el CAPTCHA a tiempo"
    }
