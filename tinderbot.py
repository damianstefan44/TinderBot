import urllib
from datetime import datetime
import json
import unicodedata
import re
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import email, password, api_key

url = 'https://tinder.com'


def get_current_timestamp():
    return str(int(datetime.now().timestamp()))


def remove_emojis(data):
    emoji = re.compile("["
                       u"\U00002700-\U000027BF"  # Dingbats
                       u"\U0001F600-\U0001F64F"  # Emoticons
                       u"\U00002600-\U000026FF"  # Miscellaneous Symbols
                       u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
                       u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                       u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                       u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
                       u"[\U00010000-\U0010ffff]"  # Rectangular signs
                       "]+", re.UNICODE)
    return re.sub(emoji, '', data)


class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def accept_conditions(self):

        try:
            cookies_accept_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//div[text()='Wyrażam zgodę']")))
            cookies_accept_button.click()

        except:
            print('nothing to accept')
        sleep(5)

    def close_tinder_on_desktop(self):
        try:
            desktop_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//div[text()='Nie interesuje mnie to']")))
            desktop_button.click()

        except:
            print('nothing to accept')
        sleep(5)

    def close_cookies(self):

        try:
            cookies_accept_button = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//button[text()='Zezwól na wszystkie pliki cookie']")))
            cookies_accept_button.click()

        except:
            print('no cookies to close')
        sleep(5)

    def click_login(self):
        login_button = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Zaloguj")]')))
        login_button.click()
        sleep(5)

    def accept_location_again(self):
        try:
            allow_location_button_again = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type="button" and @class="c1p6lbu0 W(100%)"]')))
            allow_location_button_again.click()
        except:
            print('no location popup')

    def accept_location(self):
        try:
            notifications_button = self.driver.find_element('xpath',
                                                            '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
            notifications_button.click()
        except:
            print('no notification popup')

        try:
            enable_button = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Korzystaj")]')))
            enable_button.click()
        except:
            print('no popup enable')

        try:
            enable_button = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Nie interesuje")]')))
            enable_button.click()
        except:
            print('no popup enable')

    def allow_notification(self, decision: bool):
        if decision:
            try:
                notifications_button = self.driver.find_element('xpath',
                                                                '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
                notifications_button.click()
            except:
                print('no notification popup')
        else:
            try:
                notifications_button = self.driver.find_element('xpath',
                                                                '/html/body/div[2]/main/div/div/div/div[3]/button[3]')
                notifications_button.click()
            except:
                print('no notification popup')

    def open_tinder(self):
        sleep(2)
        self.driver.get(url)
        self.accept_conditions()
        sleep(2)
        self.click_login()
        self.facebook_login()
        sleep(6)

    def facebook_login(self):
        # find and click FB login button
        login_with_facebook = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Facebook")]')))
        login_with_facebook.click()
        # save references to main and FB windows
        sleep(2)
        base_window = self.driver.window_handles[0]
        fb_popup_window = self.driver.window_handles[1]
        # switch to FB window
        self.driver.switch_to.window(fb_popup_window)

        self.close_cookies()

        email_field = self.driver.find_element(By.NAME, 'email')
        pw_field = self.driver.find_element(By.NAME, 'pass')
        login_button = self.driver.find_element(By.NAME, 'login')
        email_field.send_keys(email)
        pw_field.send_keys(password)
        login_button.click()
        self.driver.switch_to.window(base_window)
        sleep(10)
        self.accept_location()

    def right_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_RIGHT)

    def left_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_UP)
        ts = get_current_timestamp()

        try:
            img_element = self.driver.find_element('xpath', '//div[@class="profileCard__slider__img Z(-1)"]')
            style = img_element.get_attribute('style')
            positions = [pos for pos, char in enumerate(style) if char == '"']
            img_name = "data/final_test_photos/" + ts + ".png"
            img_source = str(style)[positions[0] + 1:positions[1]]
            urllib.request.urlretrieve(img_source, img_name)
        except:
            print("couldnt find photo")

        doc.send_keys(Keys.SPACE)

        # USER NAME

        try:
            user_name_element = self.driver.find_element('xpath', '//div[@class="Ov(h) Ws(nw) Ell"]')
            user_name = unicodedata.normalize('NFKD', user_name_element.text.replace("ł", "l").replace("Ł","L")).encode('ascii', 'ignore').decode('utf-8')
        except:
            user_name = "null"

        # USER AGE

        try:
            user_age_element = self.driver.find_element('xpath', '//span[@class="Whs(nw) Typs(display-2-strong)"]')
            user_age = user_age_element.text
        except:
            user_age = "null"

        # USER KILOMETERS AWAY

        try:
            user_km_element = self.driver.find_element(By.XPATH, '//div[contains(text(), "kilometr")]')
            if user_km_element.text.split(" ")[0].isnumeric():
                user_km = user_km_element.text.split(" ")[0]
            else:
                user_km = "0"
        except:
            user_km = "null"

        #USER VERIFICATION CHECK

        try:
            _ = self.driver.find_element('xpath', '//div[@class="D(ib) Lh(0) Sq(30px) Mstart(4px) As(c)"]')
            user_verified = "yes"
        except:
            user_verified = "no"

        # USER LOCATION

        try:
            user_location_element = self.driver.find_element(By.XPATH, '//div[contains(text(), "Mieszka w")]')
            user_location = unicodedata.normalize('NFKD',user_location_element.text[10:].replace("ł", "l").replace("Ł","L")).encode('ascii', 'ignore').decode('utf-8')
        except:
            user_location = "null"

        # USER SMOKING HABIT

        try:
            user_smoking_element = self.driver.find_element(By.XPATH, '//div[contains(text(), "alę")]')
            switch = {
                "Nie palę": "don't smoke",
                "Palę": "smoke",
                "Palę tylko dla towarzystwa": "smoke for company",
                "Palę do alkoholu": "smoke while drinking",
            }
            user_smoking = switch.get(user_smoking_element.text, "null")
        except:
            try:
                user_smoking_element = self.driver.find_element(By.XPATH, '//div[contains(text(), "Próbuję rzucić")]')
                user_smoking = "trying to quit smoking"
            except:
                user_smoking = "null"

        # USER DRINKING HABIT

        try:
            _ = self.driver.find_element(By.XPATH, '//div[contains(text(), "To nie dla mnie")]')
            user_drinking = "no"
        except:
            try:
                _ = self.driver.find_element(By.XPATH, '//div[contains(text(), "Już nie piję")]')
                user_drinking = "no"
            except:
                try:
                    _ = self.driver.find_element(By.XPATH, '//div[contains(text(), "Próbuję ograniczać")]')
                    user_drinking = "sometimes"
                except:
                    try:
                        _ = self.driver.find_element(By.XPATH, '//div[contains(text(), "Tylko okazjonalnie")]')
                        user_drinking = "sometimes"
                    except:
                        try:
                            _ = self.driver.find_element(By.XPATH, '//div[contains(text(), "Towarzysko w weekendy")]')
                            user_drinking = "sometimes"
                        except:
                            try:
                                _ = self.driver.find_element(By.XPATH, '//div[contains(text(), "Prawie co wieczór")]')
                                user_drinking = "a lot"
                            except:
                                user_drinking = "null"

        # USER KID STATUS

        try:
            user_kid_element = self.driver.find_element(By.XPATH, '//div[contains(text(), "dzieci")]')

            switch = {
                "Chcę mieć dzieci": "don't have kids",
                "Nie chcę mieć dzieci": "don't have kids",
                "Mam dzieci i chcę więcej": "have kids",
                "Mam dzieci, nie chcę więcej": "have kids",
            }
            user_kid = switch.get(user_kid_element.text, "null")

        except:
            user_kid = "null"

        # USER DESCRIPTION

        try:
            user_description_element = self.driver.find_element('xpath','//div[@class="react-aspect-ratio-placeholder"]')
            user_description_element2 = user_description_element.find_element('xpath', '..')
            user_description_element3 = user_description_element2.find_elements(By.XPATH, '*')[1]
            user_description_element4 = user_description_element3.find_elements(By.XPATH, '*')[2]
            user_description_element5 = user_description_element4.find_elements(By.XPATH, '*')[0]
            user_description = unicodedata.normalize('NFKD', remove_emojis(user_description_element5.text).replace("ł", "l").replace("Ł","L").replace("\n"," ")).encode('ascii', 'ignore').decode('utf-8')
        except:
            user_description = "null"

        # USER INTERESTS

        try:
            user_interest_element = self.driver.find_element('xpath', "//h2[text()='Zainteresowania']")
            user_interest_element2 = user_interest_element.find_element('xpath', '..')
            user_interest_element3 = user_interest_element2.find_elements(By.XPATH, '*')[1]
            user_interest_element4 = user_interest_element3.find_elements(By.XPATH, '*')[0]
            user_interests = user_interest_element4.find_elements(By.XPATH, '*')
            user_interests_number = len(user_interests)
            user_interest_list = [unicodedata.normalize('NFKD', interest.text.replace("ł", "l").replace("Ł", "L")).encode('ascii', 'ignore').decode('utf-8') for interest in user_interests]
            for _ in range(5 - user_interests_number):
                user_interest_list.append("null")

            user_interest1 = user_interest_list[0]
            user_interest2 = user_interest_list[1]
            user_interest3 = user_interest_list[2]
            user_interest4 = user_interest_list[3]
            user_interest5 = user_interest_list[4]
        except:
            user_interest1 = "null"
            user_interest2 = "null"
            user_interest3 = "null"
            user_interest4 = "null"
            user_interest5 = "null"

        with open(users_path) as fp:
            users_list = json.load(fp)
        users_list.append({
            "id": ts,
            "name": user_name,
            "age": user_age,
            "kilometers": user_km,
            "verified": user_verified,
            "location": user_location,
            "smoking": user_smoking,
            "drinking": user_drinking,
            "kids": user_kid,
            "interest1": user_interest1,
            "interest2": user_interest2,
            "interest3": user_interest3,
            "interest4": user_interest4,
            "interest5": user_interest5,
            "description": user_description
        })
        with open(users_path, 'w') as json_file:
            json.dump(users_list, json_file, ensure_ascii=False,
                      indent=4,
                      separators=(',', ': '))

        doc.send_keys(Keys.ARROW_LEFT)

        sleep(1)

    def auto_swipe(self):
        while True:
            sleep(2)
            try:
                self.right_swipe()
            except:
                print("couldn't swipe right")


if __name__ == "__main__":
    bot = TinderBot()
    bot.open_tinder()
    counter = 0

    for i in range(6):
        bot.left_swipe()

    bot.close_tinder_on_desktop()

    while True:
        bot.left_swipe()
