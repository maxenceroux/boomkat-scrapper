from selenium import webdriver

import time

driver = webdriver.Chrome("/users/maxence.roux/Documents/drivers/chromedriver")
driver.get("https://boomkat.com/bestsellers")

# time.sleep(2)  # Let the user actually see something!

bestsellers_web_element = driver.find_elements_by_class_name("bestsellers")[0].text
bestseller_assert = bestsellers_web_element.split("\n")[0]
assert "Bestsellers (showing last 7 days in all genres)" in bestseller_assert
