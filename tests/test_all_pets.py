import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from setting import valid_email, valid_password


def test_show_my_pets(driver):
   '''проверяем что мы оказались на странице "мои питомцы"'''

   # Вводим email
   element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
   driver.find_element(By.ID, 'email').send_keys(valid_email)

   # Вводим пароль
   element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
   driver.find_element(By.ID, 'pass').send_keys(valid_password)

   # Нажимаем на кнопку входа в аккаунт
   element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # Нажимаем на ссылку "Мои питомцы"
   element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
   driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
   assert driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'



def test_show_all_my_pets(driver):
    '''Проверяем, что на странице присутствуют все питомцы'''

    driver.find_element(By.ID, 'email').send_keys(valid_email)
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    # сохраняем в переменную статистику
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    statistic = driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

    # сохраняем в переменную карточки питомцев
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    pets = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    assert number == len(pets)


def test_foto_my_pets(driver):
    '''Проверяем, что хотя бы у половины питомцев есть фото.'''

    driver.find_element(By.ID, 'email').send_keys(valid_email)
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    # сохраняем в переменную статистику
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    statistic = driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

    # сохраняем в переменную карточки питомцев
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover img')))
    images = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

    # количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    # Находим половину от количества питомцев
    half = number // 2

    # Находим количество питомцев с фотографией
    number_all_photos = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_all_photos += 1

    # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
    assert number_all_photos >= half
    print(f'количество фото: {number_all_photos}')
    print(f'Половина от числа питомцев: {half}')


def test_my_pets_name_age_gender(driver):
    '''У всех питомцев есть имя, возраст и порода.'''

    driver.find_element(By.ID, 'email').send_keys(valid_email)
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    # images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_all_pets_have_different_names(driver):
    '''Поверяем что на странице со списком моих питомцев, у всех питомцев разные имена'''

    driver.find_element(By.ID, 'email').send_keys(valid_email)
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()


    # сохраняем в переменную карточки питомцев
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    data_pets = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Перебираем данные, оставляем имя, возраст, и породу остальное меняем на пустую строку
   # и разделяем пробелом. Выбераем имена и добавляем их в список.
    pets_name = []
    for i in range(len(data_pets)):
        data_pet = data_pets[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        pets_name.append(split_data_pet[0])

   # Перебираем имена и если имя повторяется то прибавляем к счетчику r единицу.
   # Проверяем, если r == 0 то повторяющихся имен нет.
    r = 0
    for i in range(len(pets_name)):
        if pets_name.count(pets_name[i]) > 1:
            r += 1
    assert r == 0
    print(r)
    print(pets_name)



def test_all_pets_have_different_names_agea_gender(driver):
    '''В списке нет повторяющихся питомцев.'''

    driver.find_element(By.ID, 'email').send_keys(valid_email)
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    # Устанавливаем явное ожидание
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # сохраняем в переменную карточки питомцев
    data_pets = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Перебираем данные, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем пробелом. Выбераем имена и добавляем их в список.
    list_data = []
    for i in range(len(data_pets)):
        data_pet = data_pets[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)

    # Склеиваем имя, возраст и породу, получившиеся склееные слова добавляем в строку
    # и между ними вставляем пробел
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '

    # Получаем список из строки line
    list_line = line.split(' ')

    # Превращаем список в множество
    set_list_line = set(list_line)

    # Находим количество элементов списка и множества
    a = len(list_line)
    b = len(set_list_line)

    # Из количества элементов списка вычитаем количество элементов множества
    result = a - b

    # Если количество элементов == 0 значит карточки с одинаковыми данными отсутствуют
    assert result == 0