from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import accountInfoGenerator as account
import getVerifCode as verifiCode
from selenium import webdriver
import fakeMail as email
import time
import argparse
# system libraries
import os
import urllib

# recaptcha libraries
import pydub
import speech_recognition as sr
# selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# custom patch libraries
import patch


def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--firefox", action="store_true",
                   help="Use Firefox - geckodriver")
group.add_argument("--chrome", action="store_true",
                   help="Use Chrome - chromedriver")

args = parser.parse_args()
ua = UserAgent()
userAgent = ua.random
print(userAgent)

if args.firefox:
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.ovrride", userAgent)
    driver = webdriver.Firefox(
        firefox_profile=profile, executable_path=r"./geckodriver")

if args.chrome:
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("start-maximized")
    #options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

driver.get("https://www.instagram.com/accounts/emailsignup/")
time.sleep(8)
try:
    cookie = driver.find_element_by_xpath(
        '/html/body/div[2]/div/div/div/div[2]/button[1]').click()
except:
    pass
name = account.username()

# Fill the email value
email_field = driver.find_element_by_name('emailOrPhone')
fake_email = email.getFakeMail()
email_field.send_keys(fake_email)
print(fake_email)

# Fill the fullname value
fullname_field = driver.find_element_by_name('fullName')
fullname_field.send_keys(account.generatingName())
print(account.generatingName())
# Fill username value
username_field = driver.find_element_by_name('username')
username_field.send_keys(name)
print(name)
# Fill password value
password_field = driver.find_element_by_name('password')
# You can determine another password here.
password_field.send_keys(account.generatePassword())
print(account.generatePassword())
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/form/div[7]/div/button"))).click()

time.sleep(8)

# Birthday verification
driver.find_element_by_xpath(
    "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select").click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                            "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select/option[4]"))).click()

driver.find_element_by_xpath(
    "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select").click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                            "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select/option[10]"))).click()

driver.find_element_by_xpath(
    "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select").click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                            "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select/option[27]"))).click()

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[6]/button"))).click()
time.sleep(3)
#
fMail = fake_email[0].split("@")
mailName = fMail[0]
domain = fMail[1]
instCode = verifiCode.getInstVeriCode(mailName, domain, driver)
driver.find_element_by_name(
    'email_confirmation_code').send_keys(instCode, Keys.ENTER)
time.sleep(10)
try:
    not_valid = driver.find_element_by_xpath(
        '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[4]/div')
    if (not_valid.text == 'That code isn\'t valid. You can request a new one.'):
        time.sleep(1)
        driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div/div[1]/div[1]/div[2]/div/button').click()
        time.sleep(10)
        instCodeNew = verifiCode.getInstVeriCodeDouble(
            mailName, domain, driver, instCode)
        confInput = driver.find_element_by_name('email_confirmation_code')
        confInput.send_keys(Keys.CONTROL + "a")
        confInput.send_keys(Keys.DELETE)
        confInput.send_keys(instCodeNew, Keys.ENTER)
except:
    pass

frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()
driver.find_element_by_class_name(
    "recaptcha-checkbox-border").click()

# switch to recaptcha audio control frame
driver.switch_to.default_content()
frames = driver.find_element_by_xpath(
    "/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()

# click on audio challenge
driver.find_element_by_id("recaptcha-audio-button").click()

# switch to recaptcha audio challenge frame
driver.switch_to.default_content()
frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[-1])
delay()

# get the mp3 audio file
src = driver.find_element_by_id("audio-source").get_attribute("src")
print("[INFO] Audio src: %s" % src)

# download the mp3 audio file from the source
urllib.request.urlretrieve(
    src, os.path.normpath(os.getcwd() + "\\sample.mp3"))
delay()

# load downloaded mp3 audio file as .wav
try:
    sound = pydub.AudioSegment.from_mp3(
        os.path.normpath(os.getcwd() + "\\sample.mp3"))
    sound.export(os.path.normpath(
        os.getcwd() + "\\sample.wav"), format="wav")
    sample_audio = sr.AudioFile(
        os.path.normpath(os.getcwd() + "\\sample.wav"))
except Exception:
    print("[ERR] Please run program as administrator or download ffmpeg manually, "
          "http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/")

# translate audio to text with google voice recognition
r = sr.Recognizer()
with sample_audio as source:
    audio = r.record(source)
key = r.recognize_google(audio)
print("[INFO] Recaptcha Passcode: %s" % key)

# key in results and submit
driver.find_element_by_id("audio-response").send_keys(key.lower())
driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
driver.switch_to.default_content()
delay()
driver.find_element_by_id("recaptcha-demo-submit").click()
delay()
