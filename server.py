import http.server
import socketserver
import os
import webbrowser
import threading
import time

# Configuración del servidor
PORT = 3001
HOST = "0.0.0.0"  # Permitir conexiones desde cualquier IP

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Agregar headers para evitar problemas de CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Si solicitan la raíz, servir index.html
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def open_browser():
    """Abrir el navegador después de un pequeño delay"""
    time.sleep(1.5)
    webbrowser.open(f'http://localhost:{PORT}')

def get_external_ip():
    """Obtener la IP externa del servidor"""
    import socket
    try:
        # Crear un socket para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "IP_NO_DISPONIBLE"

def main():
    try:
        # Verificar si existe index.html
        if not os.path.exists('index.html'):
            print("❌ Error: No se encontró el archivo 'index.html' en el directorio actual.")
            print("📁 Asegúrate de que el archivo HTML esté en la misma carpeta que este script.")
            return
        
        # Configurar el servidor
        with socketserver.TCPServer((HOST, PORT), CustomHTTPRequestHandler) as httpd:
            print("🚀 Iniciando servidor UPN Travel...")
            print(f"📍 Servidor local: http://localhost:{PORT}")
            print(f"📍 Servidor externo: http://{get_external_ip()}:{PORT}")
            print(f"📁 Sirviendo archivos desde: {os.getcwd()}")
            print("🌐 Abriendo navegador local...")
            print("\n💡 Para detener el servidor, presiona Ctrl+C")
            print("=" * 50)
            
            # Abrir navegador en un hilo separado
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # Iniciar servidor
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Error: El puerto {PORT} ya está en uso.")
            print("💡 Intenta con un puerto diferente o cierra el proceso que lo está usando.")
        else:
            print(f"❌ Error del sistema: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()