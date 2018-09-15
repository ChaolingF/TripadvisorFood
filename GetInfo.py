from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import csv
import time

style = input("Please let me know which type you're interested in: \n"
              "a) Restaurants \n"
              "b) Dessert \n"
              "c) Coffee and Tea \n"
              "d) Bakeries\n"
              "e) Bars and Pubs \n"
              "Please let me know which type you're interested in: ")
driver = webdriver.Chrome()
#website = input("Please paste the website that you wanna collect: ")
website = "https://www.tripadvisor.com.tw/Restaurants-g60745-Boston_Massachusetts.html"

driver.get(website)

style_xpath = {
    'a' : "//*[@id='jfy_filter_bar_establishmentTypeFilters']/div[2]/div[1]",
    'b' : "//*[@id='jfy_filter_bar_establishmentTypeFilters']/div[2]/div[2]",
    'c' : "//*[@id='jfy_filter_bar_establishmentTypeFilters']/div[2]/div[3]",
    'd' : "//*[@id='jfy_filter_bar_establishmentTypeFilters']/div[2]/div[4]",
    'e' : "//*[@id='jfy_filter_bar_establishmentTypeFilters']/div[2]/div[5]"
}
if(style != 'a'):
    driver.find_element_by_xpath("//*[@id='jfy_filter_bar_establishmentTypeFilters']/div[2]/div[6]").click()
    driver.find_element_by_xpath(style_xpath[style]).click()
    time.sleep(2)

else:
    pass

# Get 30 restaurants

#wait = WebDriverWait(driver,3).until(
#    EC.presence_of_element_located((By.CLASS_NAME,"label filterName"))
#)

restaurants = driver.find_elements_by_class_name("property_title")
newfile = True

for restaurant in restaurants:
    restaurant.click()
    handle = driver.window_handles
    driver.switch_to_window(handle[1])
    title = driver.find_element_by_class_name("heading_title").text
    street = driver.find_element_by_class_name("street-address").text
    locality = driver.find_element_by_class_name("locality").text
    address = street + "," + locality
    review = driver.find_element_by_xpath("//*[@id='taplc_location_detail_header_restaurants_0']/div[1]/span[1]/div/div/span")
    star = review.get_attribute("content")
    rank = driver.find_element_by_css_selector("#taplc_location_detail_header_restaurants_0 > div.rating_and_popularity > span:nth-child(2) > div > span > b > span").text

    try:
        price = driver.find_element_by_css_selector("#taplc_location_detail_header_restaurants_0 > div.rating_and_popularity > span.header_tags.rating_and_popularity").text
    except:
        price = ""
    try:
        style = driver.find_element_by_css_selector("#taplc_location_detail_header_restaurants_0 > div.rating_and_popularity > span.header_links.rating_and_popularity").text
    except:
        style = ""
    with open('restaurant_info.txt', 'a', newline='') as csvfile:
        fieldnames = ['Title', 'Address', 'Review', 'Rank', 'Price', 'Style']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter = '|')
        if (newfile == True):
            writer.writeheader()
        writer.writerow(
            {
                'Title': title,
                'Address': address,
                'Review': star,
                'Rank': rank,
                'Price': price,
                'Style': style
            }
        )
    newfile = False
    driver.close()
    driver.switch_to_window(handle[0])

print("Got 30 data!")
driver.quit()
