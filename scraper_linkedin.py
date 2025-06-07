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
from config import getDriver, fecha_extraccion, LINKEDIN_USER, LINKEDIN_PASSOWRD, scroll_hasta_el_final
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException,NoSuchElementException




#Funcion para loguiarse en linkedin
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


#funcion para buscar los trabajos
def buscador(driver, trabajoBusqueda):

    driver.get("https://www.linkedin.com/jobs/search/")

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'global-nav__content')))

    # Buscar el input del buscador
    keyword_input = driver.find_element(By.CSS_SELECTOR, "input.jobs-search-box__text-input")
    keyword_input.clear()
    keyword_input.send_keys(trabajoBusqueda)
    time.sleep(1)

    # Clic en el botón buscar
    search_button = driver.find_element(By.CLASS_NAME, "jobs-search-box__submit-button")
    search_button.click()
    time.sleep(6)


def obtener_info_trabajo(id, titulo_puesto,url_empleo,fecha_extraccion,driver):

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__job-details--container"))
    )
        
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
            if texto and texto != '·' and not ubicacion:
                ubicacion = texto
            if texto.startswith("hace") and not fecha_publicacion:
                fecha_publicacion = texto

    except NoSuchElementException:
        ubicacion = None
        fecha_publicacion = None




    try:
        descripcion_div = contenedorDerecha.find_element(By.CSS_SELECTOR, "div.jobs-box__html-content.jobs-description-content__text--stretch")
        descripcion_breve = descripcion_div.text.strip()[:250]
    except NoSuchElementException:
        descripcion_breve = None



    return {
            "id" : id,
            "titulo_puesto": titulo_puesto,
            "empresa": empresa,
            "ubicacion": ubicacion,
            "modalidad": modalidad,
            "nivel_experiencia": nivel_experiencia,
            "fecha_publicacion": fecha_publicacion,
            "fecha_extraccion": fecha_extraccion,
            "url_empleo": url_empleo,
            "descripcion_breve": descripcion_breve
        }





def recolector(fecha_extraccion, driver):
    #driver.get('file:///C:/Users/mauro/OneDrive/Desktop/prueba_tecnica/prueba.html') # funcion usada para construir el codigo
   
    WebDriverWait(driver, 13).until(
        EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__content--list-detail")) #UL
    )

    # Obtener contenedor principal, donde apararece toda la informacion necesaria
    contenedorPrincipal = driver.find_element(By.CLASS_NAME, "scaffold-layout__content--list-detail")

    
    # Div principal, donde aparecen los trabajos
    #scroll_area = contenedorPrincipal.find_element(By.CLASS_NAME, "tSivhBFvtczkIEFnsGKTrWShmUuVkbSQ") #clase dinamica   
    scroll_area = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div')

    # Scroll suave
    for i in range(0, 3000, 100):
        driver.execute_script("arguments[0].scrollTop = arguments[1];", scroll_area, i)
        time.sleep(0.2)

    #Ul de trabajos
    #contenedorIzquierda = contenedorPrincipal.find_element(By.CLASS_NAME, "UREiBoDFpFNCTlovSdZOWyybRiVqOHE") #clase dinamica
    contenedorIzquierda = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/ul')

    
    # Obtener los títulos y Links de los trabajos. Luego entrar a estos
    jobCards = contenedorIzquierda.find_elements(By.CLASS_NAME, "job-card-list__title--link")

    listaInfoTrabajos = []

    for i, job in enumerate(jobCards):
        try:
            titulo_puesto = job.get_attribute("aria-label")
        except NoSuchElementException:                  
            titulo_puesto = None

        try:
            url_empleo = job.get_attribute('href')
        except NoSuchElementException:                  
            url_empleo = None

        job.click()
        
        trabajo = obtener_info_trabajo(i, titulo_puesto, url_empleo, fecha_extraccion, driver)
        
        listaInfoTrabajos.append(trabajo)

    return listaInfoTrabajos
        




driver = getDriver()
login(driver)
buscador(driver, "desarrollador python")
listaInfoTrabajos = recolector(fecha_extraccion, driver)

for t in listaInfoTrabajos:
    print(t)