# URL Base: https://listado.mercadolibre.com.ar/
# Producto sugerido: Notebooks, smartphones, o electrodomésticos
# Desafíos técnicos:
# o Detección básica de bots
# o Paginación con JavaScript
# o Múltiples layouts de productos
# o Rate limiting moderado



import time
from config import getDriver, fecha_extraccion
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


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



url = 'https://listado.mercadolibre.com.ar/'

driver = getDriver()

productos = ["notebooks", "smartphones", "electrodomesticos"]



def extraer_datos_productos(url, producto, fecha_extraccion, driver):

    urlCompleta = url + producto
    driver.get(urlCompleta)

    productos = []
    

    WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-result__wrapper"))
    )
    
    # Localizar todos los productos en la página
    todosElementosProductos = driver.find_elements(By.CSS_SELECTOR, ".ui-search-result__wrapper")

    # Scroll suave
    for i in range(0, 3000, 100):
        driver.execute_script("window.scrollBy(0, 100);")
        time.sleep(0.2)

    for i, producto in enumerate(todosElementosProductos):

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










producto = extraer_datos_productos(url,'notebooks', fecha_extraccion, driver)
print(producto)
