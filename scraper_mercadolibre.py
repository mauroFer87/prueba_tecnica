# URL Base: https://listado.mercadolibre.com.ar/
# Producto sugerido: Notebooks, smartphones, o electrodomésticos
# Desafíos técnicos:
# o Detección básica de bots
# o Paginación con JavaScript
# o Múltiples layouts de productos
# o Rate limiting moderado


# producto, precio, vendedor, ubicacion, reputacion_vendedor,
# fecha_extraccion ,url _producto ,disponible ,envio_gratis, categoria
import time
from config import getDriver, normalizar,fechaExtraccion
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


url = 'https://listado.mercadolibre.com.ar/'

driver = getDriver()
wait = WebDriverWait(driver, 10)

# Keywords normalizadas (en minúsculas y sin tildes)
keywords = ["notebooks", "smartphones", "electrodomesticos"]

urls = list(map(lambda k: url + k, keywords))




driver.get('https://listado.mercadolibre.com.ar/notebooks')


def scroll_hasta_el_final(driver):
    SCROLL_PAUSE_TIME = 1.5  # Ajustá este tiempo si la conexión es lenta
    MAX_SCROLL_INTENTOS = 20

    ultimo_alto = driver.execute_script("return document.body.scrollHeight")
    
    intentos = 0
    while intentos < MAX_SCROLL_INTENTOS:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        nuevo_alto = driver.execute_script("return document.body.scrollHeight")
        if nuevo_alto == ultimo_alto:
            break  # No hay más productos para cargar
        ultimo_alto = nuevo_alto
        intentos += 1


def extraer_datos_productos(driver):


    scroll_hasta_el_final(driver)  # 👉 Forzamos a cargar todos los productos


    productos = []
    
    # Esperar a que los productos estén cargados
    WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-result__wrapper"))
    )
    
    # Localizar todos los productos en la página
    elementos_productos = driver.find_elements(By.CSS_SELECTOR, ".ui-search-result__wrapper")
    print(f"Se encontraron {len(elementos_productos)} productos.")

    for i, producto in enumerate(elementos_productos):

        try:
            nombre = producto.find_element(By.CLASS_NAME, "poly-component__title-wrapper").text
        except:
            nombre = None

        try:
            precio_actual = producto.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction").text
        except:
            precio_actual = None

        try:
            vendedor = producto.find_element(By.CSS_SELECTOR, ".poly-component__seller").text
        except:
            vendedor = None

        try:
            ubicacion = producto.find_element(By.CSS_SELECTOR, ".ui-search-item__location").text
        except:
            ubicacion = None

        try:
            envio = producto.find_element(By.CSS_SELECTOR, ".poly-component__shipping span").text
        except:
            envio = None

        productos.append({
            "id": i,
            "nombre": nombre,
            "precio": precio_actual,
            "vendedor": vendedor,
            "envio": envio,
            "ubicacion": ubicacion
        })

    return productos       







def paginacion():
    try:
        # Esperar y cerrar cookies si aparecen
        try:
            boton_aceptar_cookies = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cookie-consent-banner-opt-out__action--key-accept"))
            )
            boton_aceptar_cookies.click()
            print("Banner de cookies cerrado.")
        except:
            print("No apareció el banner de cookies.")

        # Esperar que el botón de "Siguiente" esté presente y sea clickeable
        boton_siguiente = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".andes-pagination__button--next a"))
        )

        driver.execute_script("arguments[0].click();", boton_siguiente)
        print("Pasaste a la siguiente página")
        time.sleep(5)

    except Exception as e:
        print("No se pudo avanzar a la siguiente página:", str(e))





producto = extraer_datos_productos(driver)
print(producto)
