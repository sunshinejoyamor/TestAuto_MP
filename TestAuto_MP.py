from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("--disable-notifications")
option.add_argument("start-maximized")
option.add_argument("--window-size=2560,1440")

### Function that adds items from the Home page
def add_to_cart_from_items_on_landing(driver, product_index):
    driver.get('https://www.jbhifi.com.au/')
    product_div = driver.find_elements(By.XPATH, '//div[@class="ProductCard_content _10ipotx1 _10ipotx0 _10ipotx4"]')
    product_name = driver.find_elements(By.XPATH, '//div[@class="_10ipotx9 _10ipotx8 _10ipotxb"]')
    time.sleep(5)
    driver.execute_script("arguments[0].scrollIntoView()", product_div[product_index])
    
    product_name_str = product_name[product_index].text

    time.sleep(5)
    product_name[product_index].click()
    time.sleep(5)

    assert product_name_str+' - JB Hi-Fi' == driver.title 

    add_to_cart = driver.find_element(By.XPATH, '//div[@id="pdp-addtocart-cta"]')
    add_to_cart.click()

    return product_name_str

### Function that adds items from the selected Category page
def add_to_cart_from_category(driver, category_index, product_index):
    driver.get('https://www.jbhifi.com.au/')
    shop_by_category_div = driver.find_elements(By.XPATH, '//div[@class="x0hzjo0"]')
    categories_div = driver.find_elements(By.XPATH, '//div[@class="_1lvqxxb1 _1lvqxxb2"]')
    time.sleep(5)
    driver.execute_script("arguments[0].scrollIntoView()", shop_by_category_div[0])

    time.sleep(5)
    categories_div[category_index].click()
    print("User is in the Category page: ", driver.title)

    category_div = driver.find_elements(By.XPATH, '//div[@class="_1cefwo81"]')
    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView()", category_div[0])

    category_product = driver.find_elements(By.XPATH, '//div[@class="_10ipotx9 _10ipotx8 _10ipotxb"]')
    add_to_cart = driver.find_elements(By.XPATH, '//button[@data-testid="product-card-actions"]')
    
    time.sleep(2)
    add_to_cart[product_index].click()

    return category_product[product_index].text

if __name__ == '__main__':
    driver = webdriver.Chrome(
        options=option
    )

    expected_product_list = set()
    expected_product_list.add(add_to_cart_from_items_on_landing(driver, 0))
    expected_product_list.add(add_to_cart_from_items_on_landing(driver, 1))
    expected_product_list.add(add_to_cart_from_category(driver,1,1))

    print(expected_product_list)

    time.sleep(5)
    
    button = driver.find_element(By.XPATH, '//span[@class="Button_labelVariants_button__ickenod" and text()="Checkout"]')

    button.click() 
    
    
    checkout = driver.find_elements(By.XPATH, '//div[@role="cell"]/div[@class="_1fragemos _1fragemox _1fragemp7 _1fragemp2 _1fragem1y _1fragemlj dDm6x"]/p')

    actual_product_list = []

    ### Convert webitem into text
    for item in checkout:
        if item.text != '':
            actual_product_list.append(item.text)

    assert len(actual_product_list) == len(set(actual_product_list))  #Check if there were duplicate items in the checkout items
    assert expected_product_list == set(actual_product_list)    #Check if items that were added are in the checkout items

    driver.close()
