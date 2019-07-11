# pip install selenium
# https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu

from selenium import webdriver
browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title