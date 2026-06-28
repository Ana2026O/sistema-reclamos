import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    # Inicializa el navegador Chrome
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_google_title(driver):
    # Abre Google
    driver.get("https://www.google.com")
    # Verifica que el título de la página contenga la palabra "Google"
    assert "Google" in driver.title
