import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_registrar_reclamo(driver):
    driver.get("http://127.0.0.1:8000/registrar/")

    # Completar formulario
    driver.find_element(By.NAME, "nombre").send_keys("Ana Ortiz")
    driver.find_element(By.NAME, "correo").send_keys("ana@example.com")
    driver.find_element(By.NAME, "telefono").send_keys("2211234567")
    driver.find_element(By.NAME, "categoria").send_keys("Atención al Cliente")
    driver.find_element(By.NAME, "descripcion").send_keys("El servicio no funciona correctamente.")

    # Enviar reclamo
    enviar_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    enviar_btn.click()

    # Esperar confirmación
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'REC-')]"))
    )

    # Crear carpeta si no existe y guardar evidencia
    os.makedirs("QA_Evidencias", exist_ok=True)
    driver.save_screenshot("QA_Evidencias/reclamo_evidencia.png")

    # Validar que aparece el número de reclamo
    assert "N° de Reclamo" in driver.page_source
