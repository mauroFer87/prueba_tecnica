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
from config import getDriver, normalizar, LINKEDIN_USER, LINKEDIN_PASSOWRD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



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





#codigo

driver = getDriver()
#login(driver)
driver.get("file:///C:/Users/mauro/OneDrive/Desktop/prueba_tecnica/prueba.html")

container = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'jobs-search__job-details--wrapper')))


def obtener_info_trabajo(fecha_extraccion, url,container):

    try:
        titulo_puesto = container.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-title').text
    except NoSuchElementException:                  
        titulo_puesto = None

    try:
        empresa = container.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__company-name').text
    except NoSuchElementException:
        empresa = None


    try:
        li_element = container.find_element(By.CSS_SELECTOR, "li.job-details-jobs-unified-top-card__job-insight--highlight")
        spans = li_element.find_elements(By.CSS_SELECTOR, "span[dir='ltr']")

        modalidad = spans[0].text if len(spans) > 0 else None
        jornada = spans[1].text if len(spans) > 1 else None
        nivel_experiencia = spans[2].text if len(spans) > 2 else None

    except NoSuchElementException:
        modalidad = None
        jornada = None
        nivel_experiencia = None

    try:
        container = container.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__primary-description-container")
        info_div = container.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__tertiary-description-container")
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
        descripcion_div = container.find_element(By.CSS_SELECTOR, "div.jobs-box__html-content.jobs-description-content__text--stretch")
        descripcion_breve = descripcion_div.text.strip()[:250]
    except NoSuchElementException:
        descripcion_breve = None



    return [titulo_puesto, empresa, ubicacion, modalidad, jornada, nivel_experiencia, fecha_publicacion, fecha_extraccion, descripcion_breve, beneficios_incluidos]






def recolector(driver, keyword):
    # Ir a la página de búsqueda de empleos
    driver.get("https://www.linkedin.com/jobs/search")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'global-nav__content')))

    # Buscar el input de keywords
    keyword_input = driver.find_element(By.CSS_SELECTOR, "input.jobs-search-box__text-input")
    keyword_input.clear()
    keyword_input.send_keys(keyword)
    time.sleep(1)

    # Clic en el botón buscar
    search_button = driver.find_element(By.CLASS_NAME, "jobs-search-box__submit-button")
    search_button.click()

    # Esperar a que aparezcan resultados
    WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.CLASS_NAME, "sjCsNciMqiXHNpjJpaLxUeOQNHEDCqNApPOU")))

    # Obtener contenedor scrollable
    scrollable_div = driver.find_element(By.CLASS_NAME, "sjCsNciMqiXHNpjJpaLxUeOQNHEDCqNApPOU")


    

    # Scroll suave
    for i in range(0, 3000, 100):
        driver.execute_script("arguments[0].scrollTop = arguments[1];", scrollable_div, i)
        time.sleep(0.2)

    # Obtener los títulos de trabajos
    job_cards = scrollable_div.find_elements(By.CLASS_NAME, "job-card-container__link")
    for job in job_cards:
        title = job.get_attribute("aria-label")
        print(title)






#recolector(driver,"Desarrollador Python")

info = obtener_info_trabajo(fecha_extraccion,url,container)
print(info)
time.sleep(20)


