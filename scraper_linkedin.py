# 2. LinkedIn Jobs
# URL Base: https://www.linkedin.com/jobs/search/
# Búsqueda sugerida: Desarrollador Python, Data Analyst, o similar
# Desafíos técnicos:
# o Autenticación requerida
# o Scroll infinito
# o Elementos con carga diferida
# o Anti-bot sofisticado

# titulo_puesto, empresa, ubicacion, modalidad, nivel_experiencia,
# fecha_publicacion, fecha_extraccion, url_empleo, descripcion_breve,
# salario_estimado

import time
from config import getDriver, fecha_extraccion, normalizar, LINKEDIN_USER, LINKEDIN_PASSOWRD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException,NoSuchElementException



def login(driver):
    # Ir a la página de login
    driver.get("https://www.linkedin.com/login")

    wait = WebDriverWait(driver, 15)
    # Ingresar usuario y contraseña
    username = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password = wait.until(EC.presence_of_element_located((By.ID, "password")))

    username.send_keys(LINKEDIN_USER)
    password.send_keys(LINKEDIN_PASSOWRD)

    # Click en el botón de login

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    login_button.click()
    time.sleep(20)



def obtener_info_trabajo(titulo_puesto,url_empleo,fecha_extraccion,driver):

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__job-details--container"))
    )
    contenedorDerecha = driver.find_element(By.CLASS_NAME, "jobs-search__job-details--container")
        
     #Div derecho, descripcion de trabajos
    contenedorDerecha = driver.find_element(By.CLASS_NAME,"jobs-search__job-details--container") 


    try:
        empresa = contenedorDerecha.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__company-name').text
    except NoSuchElementException:
        empresa = None

    
    
    try: #modalidad, jornada y nivel_experiencia estan dentro del mismo elemento
        li_element = contenedorDerecha.find_element(By.CSS_SELECTOR, "li.job-details-jobs-unified-top-card__job-insight--highlight")
        spans = li_element.find_elements(By.CSS_SELECTOR, "span[dir='ltr']")

        modalidad = spans[0].text if len(spans) > 0 else None
        jornada = spans[1].text if len(spans) > 1 else None
        nivel_experiencia = spans[2].text if len(spans) > 2 else None

    except NoSuchElementException:
        modalidad = None
        jornada = None
        nivel_experiencia = None


    try:  #ubicacion y fecha_publicacion estan dentro del mismo elemento
        container = contenedorDerecha.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__primary-description-container")
        info_div = contenedorDerecha.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__tertiary-description-container")
        spans = info_div.find_elements(By.CSS_SELECTOR, "span.tvm__text.tvm__text--low-emphasis")

        ubicacion = None
        fecha_publicacion = None

        for span in spans:
            texto = span.text.strip()
            if texto and texto != '·':
                ubicacion = texto
                break

        for span in spans:
            texto = span.text.strip()
            if texto.startswith("hace"):
                fecha_publicacion = texto
                break

    except NoSuchElementException:
        ubicacion = None
        fecha_publicacion = None




    try:
        descripcion_div = contenedorDerecha.find_element(By.CSS_SELECTOR, "div.jobs-box__html-content.jobs-description-content__text--stretch")
        descripcion_breve = descripcion_div.text.strip()[:250]
    except NoSuchElementException:
        descripcion_breve = None



    return [titulo_puesto, empresa, ubicacion, modalidad, nivel_experiencia, fecha_publicacion, fecha_extraccion, url_empleo, descripcion_breve]



def buscador(driver, keyword):
    # Setup Selenium
    driver.get("https://www.linkedin.com/jobs/search/")

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'global-nav__content')))

    # Buscar el input de keywords
    keyword_input = driver.find_element(By.CSS_SELECTOR, "input.jobs-search-box__text-input")
    keyword_input.clear()
    keyword_input.send_keys(keyword)
    time.sleep(1)

    # Clic en el botón buscar
    search_button = driver.find_element(By.CLASS_NAME, "jobs-search-box__submit-button")
    search_button.click()


def recolector(fecha_extraccion, driver):
    driver.get('file:///C:/Users/mauro/OneDrive/Desktop/prueba_tecnica/prueba.html') # funcion usada para construir el codigo

    #driver.get('https://www.linkedin.com/jobs/search/') # funcion real de linkedin
    

    WebDriverWait(driver, 13).until(
        EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__content--list-detail")) #UL
    )

    # Obtener contenedor principal, donde apararece toda la informacion necesaria
    contenedorPrincipal = driver.find_element(By.CLASS_NAME, "scaffold-layout__content--list-detail")

    # Div principal, donde aparecen los trabajos
    scroll_area = contenedorPrincipal.find_element(By.CLASS_NAME, "OCuhggDIOYsAstCSULrRCUjZucFwhcvBANI") #clase dinamica

    #Ul de trabajos
    contenedorIzquierda = contenedorPrincipal.find_element(By.CLASS_NAME, "UqvsszlKcsHVxKPENVjvrBhRdSmTopYxAtIreCY") #clase dinamica



    # Scroll suave
    for i in range(0, 3000, 100):
        driver.execute_script("arguments[0].scrollTop = arguments[1];", scroll_area, i)
        time.sleep(0.2)

    
    # Obtener los títulos y Links de los trabajos. Luego entrar a estos
    jobCards = contenedorIzquierda.find_elements(By.CLASS_NAME, "job-card-list__title--link")

    listaInfoTrabajos = []

    for job in jobCards:
        infoTrabajo = []
        try:
            titulo_puesto = job.get_attribute("aria-label")
        except NoSuchElementException:                  
            titulo_puesto = None

        try:
            url_empleo = job.get_attribute('href')
        except NoSuchElementException:                  
            url_empleo = None

        infoTrabajo.append(titulo_puesto)
        infoTrabajo.append(url_empleo)
        #job.click()
        
        trabajo = obtener_info_trabajo(titulo_puesto, url_empleo, fecha_extraccion, driver)
        infoTrabajo = infoTrabajo + trabajo
        for info in infoTrabajo:
            print(info)

        break
        listaInfoTrabajos.append(infoTrabajo)

        




driver = getDriver()
#login(driver)
# buscador(driver, "desarrollador python")
recolector(fecha_extraccion, driver)