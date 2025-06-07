# URL Base: https://listado.mercadolibre.com.ar/
# Producto sugerido: Notebooks, smartphones, o electrodomésticos
# Desafíos técnicos:
# o Detección básica de bots
# o Paginación con JavaScript
# o Múltiples layouts de productos
# o Rate limiting moderado



import time
import random
from config import getDriver, fecha_extraccion
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

import logging
from config import configurar_logging

configurar_logging()
logger = logging.getLogger(__name__)  # logger para este archivo específico







def scroll_hasta_el_final(driver):
    """
    Realiza scroll hacia abajo hasta el final de la página web para
    cargar contenido dinámico (ejemplo: productos que se cargan al hacer scroll).

    Parámetros:
        driver: instancia de Selenium WebDriver.

    Comportamiento:
        Hace scroll hasta que la altura de la página no cambie después de
        un intento (o se llegue al máximo de intentos permitidos).
    """

    SCROLL_PAUSE_TIME = 1.5  # Tiempo en segundos para esperar tras cada scroll
    MAX_SCROLL_INTENTOS = 20  # Máximo número de scrolls para evitar loops infinitos

    try:
        logger.info("Inicio scroll hasta el final de la página")
        
        # Obtener altura inicial del documento
        ultimo_alto = driver.execute_script("return document.body.scrollHeight")
        intentos = 0

        while intentos < MAX_SCROLL_INTENTOS:
            # Hacer scroll hasta el final de la página
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Esperar un tiempo para que la página cargue contenido nuevo
            time.sleep(SCROLL_PAUSE_TIME)

            # Obtener la nueva altura después del scroll
            nuevo_alto = driver.execute_script("return document.body.scrollHeight")

            # Si la altura no cambió, significa que no hay más contenido para cargar
            if nuevo_alto == ultimo_alto:
                break

            # Actualizar la altura para el siguiente ciclo
            ultimo_alto = nuevo_alto
            intentos += 1

        logger.info(f"Scroll finalizado después de {intentos} intentos")

    except Exception as e:
        logger.error(f"Error durante el scroll: {e}")










def extraer_datos_productos(url, busqueda, fecha_extraccion, driver):
    """
    Extrae datos de productos desde una página de listado de MercadoLibre.
    Retorna una lista de diccionarios con la información obtenida.
    
    Maneja errores comunes: timeout, captcha, cambios de estructura, etc.
    """

    productos = []
    urlCompleta = url + busqueda

    try:
        driver.get(urlCompleta)

        if "Verificación" in driver.title or "reCAPTCHA" in driver.page_source.lower():
            logger.warning("Captcha detectado o bloqueo temporal en URL: %s", urlCompleta)
            return []

        # Espera hasta que los productos sean visibles (máx. 10s)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-result__wrapper"))
        )

        # Hacer scroll hasta el final de la página para cargar todos los productos
        scroll_hasta_el_final(driver)

        todosElementosProductos = driver.find_elements(By.CSS_SELECTOR, ".ui-search-result__wrapper")

        for i, elemento in enumerate(todosElementosProductos):
            try:
                producto = elemento.find_element(By.CLASS_NAME, "poly-component__title-wrapper").text
            except NoSuchElementException:
                producto = None

            try:
                precioTexto = elemento.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction").text.replace('.', '')
                precio = int(precioTexto) if precioTexto.isdigit() and int(precioTexto) > 0 else None
            except NoSuchElementException:
                precio = None

            try:
                vendedor = elemento.find_element(By.CSS_SELECTOR, ".poly-component__seller").text
            except NoSuchElementException:
                vendedor = None

            try:
                ubicacion = elemento.find_element(By.CSS_SELECTOR, ".ui-search-item__location").text
            except NoSuchElementException:
                ubicacion = None

            try:
                reputacion_vendedor = elemento.find_element(By.CSS_SELECTOR, ".poly-reviews__rating").text
            except NoSuchElementException:
                reputacion_vendedor = None

            try:
                url_producto = elemento.find_element(By.CSS_SELECTOR, ".poly-component__title-wrapper a").get_attribute("href")
                if not url_producto.startswith("http"):
                    url_producto = None
                    
            except NoSuchElementException:
                url_producto = None

            try:
                envio_texto = elemento.find_element(By.CSS_SELECTOR, ".poly-component__shipping").text.strip().lower()
                envio_gratis = envio_texto == 'envío gratis' or envio_texto.startswith('llega gratis')
            except NoSuchElementException:
                envio_gratis = None

            productoInfo = {
                "id": i,
                "producto": producto,
                "precio": precio,
                "ubicacion": ubicacion,
                "vendedor": vendedor,
                "reputacion_vendedor": reputacion_vendedor,
                "fecha_extraccion": fecha_extraccion,
                "url_producto": url_producto,
                "envio_gratis": envio_gratis,
                "categoria": busqueda
            }

            productos.append(productoInfo)

    except TimeoutException:
        logger.error("Timeout: No se cargaron los productos a tiempo para URL: %s", urlCompleta)
    except WebDriverException as e:
        logger.error("Error de conectividad o carga de página: %s", str(e))
    except Exception as e:
        logger.error("Error inesperado: %s", str(e))

    return productos
     










url = 'https://listado.mercadolibre.com.ar/'

driver = getDriver()

productosABuscar = ["notebooks", "smartphones", "electrodomesticos"]



producto = extraer_datos_productos(url,'notebooks', fecha_extraccion, driver)
for p in producto:
    print(p)
