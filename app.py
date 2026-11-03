import os
import requests
from flask import Flask, render_template_string, request, Response, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_render_siaf'

MEF_BASE_URL = "https://apps2.mef.gob.pe/consulta-vfp-webapp/"
 

@app.route('/')
def index():
    html_interface = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SIAF 2026 - Consulta Rápida</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; padding: 15px; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 90vh; margin: 0; }
            .card { background: #ffffff; padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 360px; }
            h2 { text-align: center; color: #1a1a1a; font-size: 1.3rem; margin: 0 0 5px 0; }
            .subtitle { text-align: center; color: #666; font-size: 0.9rem; margin-bottom: 25px; }
            label { display: block; margin-bottom: 6px; font-weight: 600; color: #333; font-size: 0.9rem; }
            input[type="text"] { width: 100%; padding: 12px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; margin-bottom: 15px; background-color: #f9f9f9; }
            input[type="text"]:focus { border-color: #007bff; background-color: #fff; outline: none; }
            .captcha-area { text-align: center; background: #f8f9fa; padding: 12px; border-radius: 6px; border: 1px dashed #ccc; margin-bottom: 15px; }
            .captcha-img { max-width: 160px; height: 50px; display: block; margin: 0 auto 8px; border-radius: 4px; }
            .refresh-link { font-size: 0.8rem; color: #007bff; text-decoration: none; cursor: pointer; }
            .btn-submit { width: 100%; background-color: #007bff; color: #ffffff; border: none; padding: 14px; border-radius: 6px; font-size: 1rem; font-weight: bold; cursor: pointer; }
            .btn-submit:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
    <div class="card">
        <h2>Consulta de Expediente</h2>
        <div class="subtitle">SIAF Año 2026 | UE: 301250</div>
        
        <form action="/buscar" method="POST">
            <label for="expediente">Número de Expediente</label>
            <input type="text" id="expediente" name="expediente" maxlength="10" placeholder="Ej. 0000456" required autocomplete="off">
            
            <div class="captcha-area">
                <img class="captcha-img" src="/ver-captcha" id="captcha_img">
                <a onclick="document.getElementById('captcha_img').src='/ver-captcha?'+new Date().getTime();" class="refresh-link">Cambiar imagen</a>
            </div>
            
            <label for="j_captcha">Código de la Imagen</label>
            <input type="text" id="j_captcha" name="j_captcha" maxlength="5" placeholder="Ingresa las letras" required autocomplete="off">
            
            <button type="submit" class="btn-submit">Buscar Expediente</button>
        </form>
    </div>
    </body>
    </html>
    """
    return render_template_string(html_interface)

@app.route('/ver-captcha')
def ver_captcha():
    client_session = requests.Session()
    response = client_session.get(f"{MEF_BASE_URL}Captcha.jpg", verify=False)
    session['mef_cookie'] = client_session.cookies.get_dict()
    return Response(response.content, mimetype='image/jpeg')

@app.route('/buscar', methods=['POST'])
def buscar():
    expediente = request.form.get('expediente')
    j_captcha = request.form.get('j_captcha')
    saved_cookies = session.get('mef_cookie', {})
    
    client_session = requests.Session()
    client_session.cookies.update(saved_cookies)
    
    payload = {
        'anoEje': '2026',
        'secEjec': '301250',
        'expediente': expediente,
        'j_captcha': j_captcha
    }
    
    response = client_session.post(f"{MEF_BASE_URL}actionConsultaExpediente.jspx", data=payload, verify=False)
    return response.text

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
