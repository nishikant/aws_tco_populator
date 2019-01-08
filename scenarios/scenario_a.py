#!/usr/bin/env python

import unittest
import time

from selenium import webdriver
from ddt import ddt, data, unpack
from selenium.webdriver.common.action_chains import ActionChains

from library.get_data import get_csv_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

@ddt
class TestScenarioA(unittest.TestCase):
    """ inheriting the TestCase class"""
    j = 2
    @classmethod
    def update(cls, value):
        cls.j += value

    @classmethod
    def setUpClass(cls):
        """test preparation"""
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()
        cls.driver.get("https://calculator.s3.amazonaws.com/index.html")

    @classmethod
    def scroll_shim(self, passed_in_driver, object):
        x = object.location['x']
        y = object.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (
            x,
            y
        )
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        passed_in_driver.execute_script(scroll_by_coord)
        passed_in_driver.execute_script(scroll_nav_out_of_way)

    @data(*get_csv_data('./data/m2a_cpu_all.csv'))
    @unpack
    def test_search(self, counter, instance_type, instance_count, instance_util,disk_size, instance_memory, core_count):
        """test case for scenario a"""
        driver = self.driver
        #driver.set_window_size(2280, 2500)

        if 'db' in instance_type:
            k = driver.find_element_by_xpath("//*[text()='Amazon RDS']").click()
            btn_elem = driver.find_element_by_xpath("//*[@class='gwt-HTML TABLE_COMMON_ADD_MORE']//preceding::img[1]")
            hover = ActionChains(driver).move_to_element(btn_elem).perform()
            btn_elem.click()
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")

            instance_elem = driver.find_elements_by_xpath("//*[@class='RDSOnDemandRow itemsTableDataRow table']")

            #Description
            j = instance_elem[int(counter)-1].find_elements_by_xpath("//*[@class='SF_RDS_INSTANCE_FIELD_DESCRIPTION field textField']")
            action = ActionChains(driver).move_to_element(j[int(counter)-1]).perform()
            j[int(counter)-1].click()
            k=j[int(counter)-1].find_elements_by_xpath("//*[@class='gwt-TextBox input']")[int(counter)-1]
            #k.clear()
            k.send_keys(instance_type)
 
            #Instance_count
            j = instance_elem[int(counter)-1].find_elements_by_xpath("//*[@class='SF_RDS_INSTANCE_FIELD_INSTANCES field integerNumericField']")
            action = ActionChains(driver).move_to_element(j[int(counter)-1]).perform()
            j[int(counter)-1].click()
            k=j[int(counter)-1].find_elements_by_xpath(".//*[@class='gwt-TextBox numericTextBox input']")[0]
            #k.clear()
            k.send_keys(Keys.CONTROL + 'a')
            k.send_keys(instance_count)
 
            #Instance_Usage
            j = instance_elem[int(counter)-1].find_elements_by_xpath("//*[@class='SF_RDS_INSTANCE_FIELD_USAGE field usageField']")
            action = ActionChains(driver).move_to_element(j[int(counter)-1]).perform()
            k=j[int(counter)-1].find_elements_by_xpath(".//*[@class='gwt-TextBox numericTextBox input']")[0]
            k.click()
            k.send_keys(Keys.CONTROL + 'a')
            k.send_keys(instance_util)


            #Instance Engine
            j = instance_elem[int(counter)-1].find_elements_by_xpath("//*[@class='SF_RDS_INSTANCE_FIELD_ENGINE field enumField']")
            action = ActionChains(driver).move_to_element(j[int(counter)-1])
            k=j[int(counter)-1].find_elements_by_xpath(".//*[@class='gwt-ListBox listBox']")[0]
            k.click()

            k = instance_elem[int(counter)-1].find_element_by_xpath(".//*[text()='SQL Server (Standard License Included)']")
            self.scroll_shim(driver, k)
            action = ActionChains(driver).move_to_element(k).perform()
            k.click()

            #Instance Class
            core,aws_opt,aws_mac=instance_type.split('.')
            aws_type='db.' + aws_opt + '.' + aws_mac
            string = ".//*[text()='" + aws_type + "']"
            print(string)

            j = instance_elem[int(counter)-1].find_elements_by_xpath("//*[@class='SF_RDS_INSTANCE_FIELD_CLASS field typeField enumField']")
            action = ActionChains(driver).move_to_element(j[int(counter)-1])
            k=j[int(counter)-1].find_elements_by_xpath(".//*[@class='gwt-ListBox listBox']")[0]
            k.click()

            k = instance_elem[int(counter)-1].find_element_by_xpath(string)
            self.scroll_shim(driver, k)
            action = ActionChains(driver).move_to_element(k).perform()
            k.click()

            #Storage
            j = instance_elem[int(counter)-1].find_elements_by_xpath("//*[@class='SF_RDS_INSTANCE_FIELD_STORAGE field integerNumericField']")
            action = ActionChains(driver).move_to_element(j[int(counter)-1]).perform()
            k=j[int(counter)-1].find_elements_by_xpath(".//*[@class='gwt-TextBox numericTextBox input']")[0]
            k.click()
            k.send_keys(Keys.CONTROL + 'a')
            k.send_keys(disk_size)

        else:

            cnt = int(counter) + 1

            btn_elem = driver.find_element_by_xpath("//*[@id='aws-calculator']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[" + str(cnt) +"]/td[1]/div/img")
            self.scroll_shim(driver, btn_elem)
            hover = ActionChains(driver).move_to_element(btn_elem).perform()
            btn_elem.click()

            #Description
            j = driver.find_element_by_xpath("//*[@id='aws-calculator']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[" + str(cnt) + "]/td[2]/table/tbody/tr/td[2]/input")
            self.scroll_shim(driver, j)
            action = ActionChains(driver).move_to_element(j).perform
            j.click()
            j.send_keys(Keys.CONTROL + 'a')
            j.send_keys(instance_type)

            #Number of instances
            j = driver.find_element_by_xpath("//*[@id='aws-calculator']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[" + str(cnt) + "]/td[3]/table/tbody/tr/td[2]/input")
            action = ActionChains(driver).move_to_element(j).perform()
            j.click()
            j.send_keys(Keys.CONTROL + 'a')
            j.send_keys(instance_count)
             
            #utilization
            j = driver.find_element_by_xpath("//*[@id='aws-calculator']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[" + str(cnt) + "]/td[4]/table/tbody/tr/td[2]/input")
            action = ActionChains(driver).move_to_element(j).perform()
            j.click()
            j.send_keys(Keys.CONTROL + 'a')
            j.send_keys(instance_util)
            #time.sleep(3) # needed if connection is slow. The list of server type takes sometime to load.. 

            #EC2 server type
            j = driver.find_element_by_xpath("//*[@id='aws-calculator']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[" + str(cnt) + "]/td[5]/table/tbody/tr/td[2]/div/img")
            action = ActionChains(driver).move_to_element(j).perform()
            j.click()
            k = driver.find_element_by_xpath(".//*[text()='Windows']").click()

            instance_elem1 = driver.find_element_by_xpath("//*[@class='gwt-DialogBox InstanceTypeSelectorDialog Dialog']")

            core,aws_opt,aws_mac=instance_type.split('.')
            aws_type=aws_opt + '.' + aws_mac
            string = ".//*[text()='" + aws_type + "']//preceding::input[1]"
            print(string)

            k = instance_elem1.find_element_by_xpath(string)
            driver.execute_script("return arguments[0].scrollIntoView(true);", k)
            k.click()

            j = driver.find_element_by_xpath("//*[text()='Close and Save']")
            j.click()
            
            #EBS section

            cnt = int(counter) + 1
            btn_elem = driver.find_element_by_xpath("//*[@id='aws-calculator']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/div/div[3]/table/tbody/tr[" + str(cnt) + "]/td[1]/div/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", btn_elem)
            hover = ActionChains(driver).move_to_element(btn_elem).perform()
            btn_elem.click()

            #Description
            j = btn_elem.find_element_by_xpath("//*[@id='aws-calculator']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/div/div[3]/table/tbody/tr[" + str(cnt) + "]/td[2]/table/tbody/tr/td/input")
            driver.execute_script("return arguments[0].scrollIntoView(true);", j)
            hover = ActionChains(driver).move_to_element(j).perform()
            j.click()
            j.send_keys(instance_type)

            #Number of Volume
            j = btn_elem.find_element_by_xpath("//*[@id='aws-calculator']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/div/div[3]/table/tbody/tr[" + str(cnt) + "]/td[3]/table/tbody/tr/td/input")
            driver.execute_script("return arguments[0].scrollIntoView(true);", j)
            hover = ActionChains(driver).move_to_element(j).perform()
            j.click()
            j.send_keys(Keys.CONTROL + 'a')
            j.send_keys(instance_count)

            #Number of Volume
            j = btn_elem.find_element_by_xpath("//*[@id='aws-calculator']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/div/div[3]/table/tbody/tr[" + str(cnt) + "]/td[5]/table/tbody/tr/td/input")
            driver.execute_script("return arguments[0].scrollIntoView(true);", j)
            hover = ActionChains(driver).move_to_element(j).perform()
            j.click()
            j.send_keys(Keys.CONTROL + 'a')
            j.send_keys(disk_size)

    @classmethod
    def tearDownClass(cls):
        """clean up"""
        #cls.driver.close() #do not close the window.
