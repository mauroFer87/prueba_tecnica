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
from config import getDriver, fecha_extraccion, LINKEDIN_USER, LINKEDIN_PASSWORD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException,NoSuchElementException, WebDriverException, TimeoutException



# Función para iniciar sesión en LinkedIn
def login(driver):
    try:
        # Ir a la página de inicio de sesión
        driver.get("https://www.linkedin.com/login")

        # Esperar hasta que el campo de usuario esté presente (máximo 15 segundos)
        wait = WebDriverWait(driver, 15)
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))

        # Completar credenciales 
        username.send_keys(LINKEDIN_USER)
        password.send_keys(LINKEDIN_PASSWORD)

        # Esperar y hacer clic en el botón de login
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
        login_button.click()

        # Esperar unos segundos para que cargue la página
        time.sleep(20)

    except TimeoutException:
        print("[ERROR] Timeout: Un elemento no se cargó a tiempo. Posible conexión lenta o cambios en el sitio.")
    except NoSuchElementException:
        print("[ERROR] Elemento no encontrado: Es posible que la estructura HTML haya cambiado.")
    except WebDriverException as e:
        print(f"[ERROR] Problema con el WebDriver o la conexión: {e}")
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")









# Función para buscar trabajos en LinkedIn
def buscador(driver, trabajoBusqueda):
    try:
        # Cargar la página de búsqueda de empleos
        driver.get("https://www.linkedin.com/jobs/search/")

        # Esperar que se cargue un elemento clave del menú superior (15s máximo)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'global-nav__content'))
        )

        # Buscar el input del buscador de palabras clave
        keyword_input = driver.find_element(By.CSS_SELECTOR, "input.jobs-search-box__text-input")
        keyword_input.clear()  # Limpiar el input
        keyword_input.send_keys(trabajoBusqueda)  # Escribir el término de búsqueda
        time.sleep(1)

        # Hacer clic en el botón de búsqueda
        search_button = driver.find_element(By.CLASS_NAME, "jobs-search-box__submit-button")
        search_button.click()
        time.sleep(6)

        # Verificación opcional por si aparece un captcha o bloqueo
        if "captcha" in driver.page_source.lower():
            print("[ADVERTENCIA] Captcha detectado tras buscar trabajo. Podría tratarse de un bloqueo temporal.")

    except TimeoutException:
        print("[ERROR] Timeout: Algún elemento no cargó a tiempo. Puede deberse a lentitud o cambios en LinkedIn.")
    except NoSuchElementException:
        print("[ERROR] Elemento no encontrado: Es posible que LinkedIn haya cambiado su estructura HTML.")
    except WebDriverException as e:
        print(f"[ERROR] Problema de conectividad o WebDriver: {e}")
    except Exception as e:
        print(f"[ERROR] Ocurrió un error inesperado: {e}")









# Función para extraer información de un empleo desde la vista detallada del panel derecho
def obtener_info_trabajo(id, titulo_puesto, url_empleo, fecha_extraccion, driver):

    try:
        # Espera hasta que el contenedor derecho esté cargado (donde se encuentra la descripción del empleo)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__job-details--container"))
        )

        # Obtener el contenedor con los detalles del empleo
        contenedorDerecha = driver.find_element(By.CLASS_NAME, "jobs-search__job-details--container")

        # =================== Empresa ===================
        try:
            empresa = contenedorDerecha.find_element(
                By.CLASS_NAME, 'job-details-jobs-unified-top-card__company-name'
            ).text
        except NoSuchElementException:
            empresa = None

        # =================== Modalidad, Jornada, Nivel de experiencia ===================
        try:
            li_element = contenedorDerecha.find_element(
                By.CSS_SELECTOR, "li.job-details-jobs-unified-top-card__job-insight--highlight"
            )
            spans = li_element.find_elements(By.CSS_SELECTOR, "span[dir='ltr']")
            modalidad = spans[0].text if len(spans) > 0 else None
            jornada = spans[1].text if len(spans) > 1 else None
            nivel_experiencia = spans[2].text if len(spans) > 2 else None
        except NoSuchElementException:
            modalidad = jornada = nivel_experiencia = None

        # =================== Ubicación y Fecha de publicación ===================
        try:
            info_div = contenedorDerecha.find_element(
                By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__tertiary-description-container"
            )
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
            ubicacion = fecha_publicacion = None

        # =================== Descripción breve del empleo ===================
        try:
            descripcion_div = contenedorDerecha.find_element(
                By.CSS_SELECTOR, "div.jobs-box__html-content.jobs-description-content__text--stretch"
            )
            descripcion_breve = descripcion_div.text.strip()[:250]
        except NoSuchElementException:
            descripcion_breve = None

        # =================== Retornar resultados ===================
        return {
            "id": id,
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

    except TimeoutException:
        print(f"[ERROR] Timeout: No se cargaron los detalles del empleo para el ID {id}.")
    except NoSuchElementException:
        print(f"[ERROR] Elemento no encontrado: Puede que LinkedIn haya cambiado su estructura para el ID {id}.")
    except WebDriverException as e:
        print(f"[ERROR] WebDriver o red: {e}")
    except Exception as e:
        print(f"[ERROR] Error inesperado al obtener detalles del trabajo (ID {id}): {e}")
    
    # Si ocurre un error y no se retorna nada, devolvemos valores nulos para no romper el flujo
    return {
        "id": id,
        "titulo_puesto": titulo_puesto,
        "empresa": None,
        "ubicacion": None,
        "modalidad": None,
        "nivel_experiencia": None,
        "fecha_publicacion": None,
        "fecha_extraccion": fecha_extraccion,
        "url_empleo": url_empleo,
        "descripcion_breve": None
    }





def recolector(fecha_extraccion, driver):
    try:
        # Esperar que aparezca el contenedor principal de la lista de trabajos
        WebDriverWait(driver, 13).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__content--list-detail"))
        )

        # Obtener contenedor principal
        contenedorPrincipal = driver.find_element(By.CLASS_NAME, "scaffold-layout__content--list-detail")

        # Área con scroll (lado izquierdo de los trabajos)
        scroll_area = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div')

        # Realizar scroll para que se carguen más trabajos (ajustar si necesario)
        for i in range(0, 5000, 100):
            driver.execute_script("arguments[0].scrollTop = arguments[1];", scroll_area, i)
            time.sleep(0.1)

        # UL que contiene los jobs
        contenedorIzquierda = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/ul')

        # Obtener los enlaces a los trabajos
        jobCards = contenedorIzquierda.find_elements(By.CLASS_NAME, "job-card-list__title--link")

        listaInfoTrabajos = []

        for i, job in enumerate(jobCards):
            try:
                # Obtener datos preliminares
                titulo_puesto = job.get_attribute("aria-label")
                url_empleo = job.get_attribute("href")

                # Scroll al elemento para asegurar clic válido
                driver.execute_script("arguments[0].scrollIntoView(true);", job)
                time.sleep(0.2)

                job.click()
                time.sleep(1)  # esperar a que cargue la descripción

                trabajo = obtener_info_trabajo(i, titulo_puesto, url_empleo, fecha_extraccion, driver)

                listaInfoTrabajos.append(trabajo)

            except (NoSuchElementException, TimeoutException, WebDriverException) as e:
                print(f"[ERROR] No se pudo procesar job {i}: {e}")
                continue  # Saltar al siguiente job si uno falla

        return listaInfoTrabajos

    except Exception as e:
        print(f"[ERROR] Falló el recolector: {e}")
        return []


















driver = getDriver()
login(driver)
buscador(driver, "desarrollador python")
listaInfoTrabajos = recolector(fecha_extraccion, driver)

for t in listaInfoTrabajos:
    print(t)