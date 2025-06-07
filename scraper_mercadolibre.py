# URL Base: https://listado.mercadolibre.com.ar/
# Producto sugerido: Notebooks, smartphones, o electrodomésticos
# Desafíos técnicos:
# o Detección básica de bots
# o Paginación con JavaScript
# o Múltiples layouts de productos
# o Rate limiting moderado



import time
from config import getDriver, fecha_extraccion, scroll_hasta_el_final
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException





url = 'https://listado.mercadolibre.com.ar/'

driver = getDriver()

productosABuscar = ["notebooks", "smartphones", "electrodomesticos"]


#esta funcion entra a una url de listado.mercadolibre y retorna la informacion de los productos en una lista
def extraer_datos_productos(url, busqueda, fecha_extraccion, driver):

    urlCompleta = url + busqueda
    driver.get(urlCompleta)
    scroll_hasta_el_final(driver)

    productos = []
    

    WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-result__wrapper"))
    )
    
    # Localizar todos los productos en la página
    todosElementosProductos = driver.find_elements(By.CSS_SELECTOR, ".ui-search-result__wrapper")


    for i, elemento in enumerate(todosElementosProductos):

        try:
            producto = elemento.find_element(By.CLASS_NAME, "poly-component__title-wrapper").text
        except NoSuchElementException:
            producto = None

        try:
            precio = int(elemento.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction").text.replace('.', ''))
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
        except NoSuchElementException:
            url_producto = None


        try:
            envio_texto = elemento.find_element(By.CSS_SELECTOR, ".poly-component__shipping").text.strip().lower()
            if envio_texto == 'envío gratis' or envio_texto.startswith('llega gratis'):
                envio_gratis = True
            else:
                envio_gratis = False
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

    return productos       










# producto = extraer_datos_productos(url,'notebooks', fecha_extraccion, driver)
# for p in producto:
#     print(p)
