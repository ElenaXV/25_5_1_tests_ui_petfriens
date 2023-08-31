import pytest
from selenium import webdriver
from setting import valid_email, valid_password
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def driver():
   driver = webdriver.Firefox()
   # Переходим на страницу авторизации
   driver.get('https://petfriends.skillfactory.ru/login')

   yield driver

   driver.quit()

@pytest.fixture
def go_to_my_pets(driver):

   # Вводим email
   # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
   driver.find_element(By.ID, 'email').send_keys(valid_email)

   # Вводим пароль
   # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
   driver.find_element(By.ID, 'pass').send_keys(valid_password)

   # Нажимаем на кнопку входа в аккаунт
   element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # Нажимаем на ссылку "Мои питомцы"
   element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
   driver.find_element(By.LINK_TEXT, "Мои питомцы").click()


