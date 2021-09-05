from selenium import webdriver
from os import path
import time

url = "https://boomkat.com/bestsellers?q[release_date]=last-month"


class BoomkatHandler:
    def __init__(self, driver_path) -> None:
        self.__driver_path = driver_path
        self.__url = url
        try:
            print(path.isfile(self.__driver_path))
        except Exception as e:
            print(f"Driver not in path: {e}")
            raise e

    def get_bestsellers_list(self):
        try:
            driver = webdriver.Chrome(self.__driver_path)
        except Exception as e:
            raise e
        driver.get(self.__url)
        time.sleep(2)
        bestsellers_web_element = driver.find_elements_by_class_name("bestsellers")[
            0
        ].text
        bestsellers_list = bestsellers_web_element.split("\n")
        bestseller_assert = bestsellers_list[0]
        assert "Bestsellers (showing last 30 days in all genres)" in bestseller_assert

        bestsellers_list = [x for x in bestsellers_list if "Play All" not in x]
        offset = bestsellers_list.index("Reset")
        bestsellers_list = bestsellers_list[offset + 1 :]
        x = 0
        bestsellers = []
        for i in range(len(bestsellers_list)):
            if i % 3 == 0:
                bestsellers.append(bestsellers_list[i])
        bestsellers = [" ".join(x.split(" - ")) for x in bestsellers]
        return bestsellers
