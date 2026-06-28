import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
def test_login(driver):
    driver.get("http://localhost:8000/login/")

    usuario_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

    usuario_input.send_keys("caro")
    password_input.send_keys("12345")
    password_input.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "button"), "Alta usuarios")
    )
    # Crear carpeta si no existe
    os.makedirs("QA_Evidencias", exist_ok=True)

    # Guardar captura como evidencia
    driver.save_screenshot("QA_Evidencias/test_login_result.png")

    assert "Alta usuarios" in driver.page_source


