import os
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime



# Cargar variables de entorno desde el archivo .env
try:
    load_dotenv()
except Exception as e:
    print(f"⚠️ Error cargando archivo .env: {e}")




# Obtener la ruta del ChromeDriver desde variable de entorno
CHROME_DRIVER_PATH = Path(os.getenv('CHROME_DRIVER_PATH', ''))

# Validar que la ruta existe y es un archivo válido
if not CHROME_DRIVER_PATH.exists() or not CHROME_DRIVER_PATH.is_file():
    raise FileNotFoundError(
        f"ChromeDriver no encontrado en: {CHROME_DRIVER_PATH}\n"
        "1. Verifica la ruta en tu archivo .env\n"
        "2. Asegúrate de que la versión de ChromeDriver sea compatible con tu navegador Chrome"
    )




# Leer credenciales de LinkedIn 
LINKEDIN_USER = os.getenv('LINKEDIN_USER')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')

if not LINKEDIN_USER or not LINKEDIN_PASSWORD:
    print("⚠️ Advertencia: Usuario o contraseña de LinkedIn no configurados en .env")




def getDriver(headless=False):
    """
    Inicializa y retorna un driver de Chrome para Selenium.

    Parámetros:
        headless (bool): Ejecuta Chrome en modo headless (sin interfaz gráfica) si es True.

    Retorna:
        driver: instancia de Selenium WebDriver para Chrome.
    """
    options = Options()

    if headless:
        # Modo headless, versión nueva
        options.add_argument("--headless=new")

    # Opciones adicionales que pueden ser útiles para entornos con recursos limitados
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--start-maximized")
    # options.add_argument("--window-size=1920,1080")

    try:
        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"❌ Error al inicializar el driver de Chrome: {e}")
        raise

    return driver




# Fecha de extracción actual en formato legible
fecha_extraccion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
