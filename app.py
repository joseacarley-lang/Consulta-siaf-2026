import os
from flask import Flask, render_template_string

app = Flask(__name__)
app.secret_key = 'solucion_definitiva_siaf_2026'

@app.route('/')
def index():
    # El truco consiste en cargar la interfaz del MEF de manera sutil e inyectar el código 
    # mediante una ventana incrustada controlada por JavaScript
    html_interface = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SIAF 2026 - Consulta Directa</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; padding: 10px; background-color: #f0f2f5; margin: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
            .card { background: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 360px; margin-top: 20px; box-sizing: border-box; }
            h2 { text-align: center; color: #1a1a1a; font-size: 1.2rem; margin: 0 0 5px 0; }
            .subtitle { text-align: center; color: #666; font-size: 0.85rem; margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; font-size: 0.85rem; }
            input[type="text"] { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; margin-bottom: 12px; background-color: #f9f9f9; }
            .btn-submit { width: 100%; background-color: #25D366; color: #ffffff; border: none; padding: 12px; border-radius: 6px; font-size: 1rem; font-weight: bold; cursor: pointer; margin-top: 5px; }
            .btn-submit:hover { background-color: #128C7E; }
            .mef-frame { width: 100%; height: 260px; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 12px; background-color: #fff; }
            .steps { font-size: 0.8rem; color: #555; background: #fff3cd; padding: 10px; border-radius: 6px; margin-bottom: 12px; border: 1px solid #ffeeba; }
        </style>
    </head>
    <body>

    <div class="card">
        <h2>Consulta Rápida MEF</h2>
        <div class="subtitle">SIAF Año 2026 | UE: 301250</div>
        
        <div class="steps">
            <strong>Instrucciones para el personal:</strong><br>
            1. Escribe abajo el número de expediente.<br>
            2. Copia el captcha tal como aparece en el cuadro inferior.<br>
            3. Haz clic en Buscar.
        </div>

        <form action="https://mef.gob.pe" method="POST" target="_blank">
            <!-- Parámetros fijos ocultos automatizados por debajo -->
            <input type="hidden" name="anoEje" value="2026">
            <input type="hidden" name="secEjec" value="301250">
            
            <label for="expediente">Número de Expediente</label>
            <input type="text" id="expediente" name="expediente" maxlength="10" placeholder="Ej. 0000456" required autocomplete="off">
            
            <label for="j_captcha">Código de la Imagen</label>
            <input type="text" id="j_captcha" name="j_captcha" maxlength="5" placeholder="Ingresa las letras" required autocomplete="off">
            
            <button type="submit" class="btn-submit">Buscar Expediente</button>
        </form>
    </div>

    <div class="card" style="margin-top: 15px; padding: 12px;">
        <label>Área de Seguridad (Validación MEF)</label>
        <!-- Incrustamos la web original para heredar de manera segura la IP del celular y cargar el captcha -->
        <iframe class="mef-frame" src="https://apps2.mef.gob.pe/consulta-vfp-webapp/consultaExpediente.jspx" scrolling="no"></iframe>
    </div>

    </body>
    </html>
    """
    return render_template_string(html_interface)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
