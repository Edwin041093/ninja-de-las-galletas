def clasificar_cookie(cookie):
    nombre = cookie["name"].lower()
    if "sess" in nombre or "sid" in nombre:
        return "sesión"
    elif "auth" in nombre or "token" in nombre:
        return "autenticación"
    elif "track" in nombre or "ga" in nombre or "_fbp" in nombre:
        return "rastreo"
    else:
        return "técnica"

def clasificar_cookies(lista_cookies):
    clasificadas = []
    for c in lista_cookies:
        tipo = clasificar_cookie(c)
        c["tipo"] = tipo
        clasificadas.append(c)
    return clasificadas
