from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com")
print("Page title is:", driver.title)
driver.quit()

#  npm i -g @vue/cli
