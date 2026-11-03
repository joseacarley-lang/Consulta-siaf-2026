import requests
from flask import Flask, render_template_string, request, Response, session

app = Flask(__name__)
# Una clave secreta obligatoria para que Flask pueda recordar la sesión (cookies) del usuario
app.secret_key = 'clave_secreta_para_el_siaf_mef'

# Dirección base del sistema de consultas del MEF (reemplazar por la URL real si varía)
MEF_BASE_URL = "https://mef.gob.pe" 

# 1. Pantalla principal que ve tu personal en su celular
@app.route('/')
def index():
    # Diseño HTML simple y optimizado para celulares
    html_interface = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Consulta Rápida SIAF 2026</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background-color: #f4f7f6; }
            .container { max-width: 400px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h2 { color: #333; text-align: center; font-size: 1.2rem; }
            label { display: block; margin: 10px 0 5px; font-weight: bold; color: #555; }
            input[type="text"] { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; }
            .captcha-box { text-align: center; margin: 15px 0; }
            .captcha-img { border: 1px solid #ddd; border-radius: 4px; max-width: 150px; }
            .btn { width: 100%; background-color: #007bff; color: white; border: none; padding: 12px; border-radius: 4px; cursor: pointer; font-size: 1rem; }
            .btn:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Consulta de Expediente (UE: 301250)</h2>
            <form action="/buscar" method="POST">
                <label>Número de Expediente:</label>
                <input type="text" name="expediente" maxlength="10" placeholder="Ej. 0000234" required>
                
                <div class="captcha-box">
                    <!-- Forzamos que cargue el captcha de la sesión actual llamando a nuestra propia ruta -->
                    <img class="captcha-img" src="/ver-captcha" id="img_captcha"><br>
                    <a href="javascript:location.reload();" style="font-size: 0.8rem; color: #007bff;">Cambiar imagen</a>
                </div>
                
                <label>Código de la imagen:</label>
                <input type="text" name="j_captcha" maxlength="5" placeholder="Ingresa letras/números" required autocomplete="off">
                <br><br>
                <button type="submit" class="btn">Buscar Expediente</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_interface)

# 2. Ruta intermedia que descarga el Captcha del MEF y se lo entrega al navegador del usuario
@app.route('/ver-captcha')
def ver_captcha():
    # Creamos una sesión de navegación persistente en el servidor para simular un usuario real
    client_session = requests.Session()
    
    # Intentamos obtener la imagen desde el servidor del MEF
    mef_captcha_url = f"{MEF_BASE_URL}Captcha.jpg"
    response = client_session.get(mef_captcha_url, verify=False)
    
    # Guardamos la cookie que nos dio el MEF en la sesión de Flask para recordar quién es este usuario
    session['mef_cookie'] = client_session.cookies.get_dict()
    
    # Devolvemos la imagen original del MEF para que se dibuje en la pantalla del celular
    return Response(response.content, mimetype='image/jpeg')

# 3. Ruta que procesa la búsqueda inyectando los datos fijos del 2026 y la UE
@app.route('/buscar', methods=['POST'])
def buscar():
    expediente = request.form.get('expediente')
    j_captcha = request.form.get('j_captcha')
    
    # Recuperamos la cookie original que el MEF asignó a este usuario al ver el captcha
    saved_cookies = session.get('mef_cookie', {})
    
    # Reconstruimos la sesión con esa cookie específica
    client_session = requests.Session()
    client_session.cookies.update(saved_cookies)
    
    # Armando el paquete de datos técnicos requeridos que descubrimos en el HTML original
    payload = {
        'anoEje': '2026',        # Fijo automatizado
        'secEjec': '301250',    # Fijo automatizado
        'expediente': expediente,
        'j_captcha': j_captcha
    }
    
    mef_action_url = f"{MEF_BASE_URL}actionConsultaExpediente.jspx"
    
    # Enviamos los datos en formato POST al MEF
    response = client_session.post(mef_action_url, data=payload, verify=False)
    
    # Devolvemos la respuesta que nos da el MEF (aquí se requerirá posteriormente "limpiar" el HTML del resultado)
    return response.text
