import os
from pathlib import Path
from dotenv import load_dotenv 
import time

# Cargar variables del archivo .env
load_dotenv()

# Obtener la ruta del driver
CHROME_DRIVER_PATH = Path(os.getenv('CHROME_DRIVER_PATH'))

# Validar que la ruta existe
if not CHROME_DRIVER_PATH.exists():
    raise FileNotFoundError(
        f"ChromeDriver no encontrado en: {CHROME_DRIVER_PATH}\n"
        "1. Verifica la ruta en tu archivo .env\n"
        "2. Verifica la version de ChromeDriver compatible Chrome"
    )

LINKEDIN_USER = os.getenv('LINKEDIN_USER')
LINKEDIN_PASSOWRD = os.getenv('LINKEDIN_PASSOWRD')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def getDriver(headless=False):
    options = Options()
    
    if headless:
        options.add_argument("--headless=new")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--start-maximized")
    # options.add_argument("--window-size=1920,1080")

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver




from datetime import datetime
fecha_extraccion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def scroll_hasta_el_final(driver):

    SCROLL_PAUSE_TIME = 1.5
    MAX_SCROLL_INTENTOS = 20

    try:
        ultimo_alto = driver.execute_script("return document.body.scrollHeight")
        intentos = 0

        while intentos < MAX_SCROLL_INTENTOS:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            nuevo_alto = driver.execute_script("return document.body.scrollHeight")

            if nuevo_alto == ultimo_alto:
                break
            ultimo_alto = nuevo_alto
            intentos += 1

    except Exception as e:
        print(f"Error durante el scroll: {e}")