import os
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
from config import email, password
from urllib.request import urlopen
from shutil import copyfileobj

url = 'https://tinder.com'
data_dir = 'data'
user_data_json_path = "data/users.json"
user_photo_dir = "data/photos/"


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


def create_necessary_directories():
    if not os.path.exists(data_dir):
        try:
            os.mkdir(data_dir)
            print(f"created {data_dir}")
        except:
            raise ValueError(f"couldn't create {data_dir} directory")
    if not os.path.exists(user_photo_dir):
        try:
            os.mkdir(user_photo_dir)
            print(f"created {user_photo_dir}")
        except:
            raise ValueError(f"couldn't create {user_photo_dir} directory")
    if not os.path.exists(user_data_json_path):
        try:
            with open(user_data_json_path, 'w') as file:
                file.write("[]")
                print(f"created {user_data_json_path}")
        except:
            raise ValueError(f"couldn't create {user_data_json_path} file")
    if os.path.exists(user_data_json_path):
        try:
            file_size = os.stat(user_data_json_path).st_size
            if file_size == 0:
                with open(user_data_json_path, 'w') as file:
                    file.write("[]")
        except:
            raise ValueError(f"couldn't open or write to {user_data_json_path} file")


class TinderBot:
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
        cookies_accept_button = self.driver.find_element('xpath',
                                                         '/html/body/div[2]/div[2]/div/div/div/div/div[3]/div['
                                                         '2]/div/div[2]/div[1]/div/div[1]/div/span/span')
        cookies_accept_button.click()

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

    def accept_popup(self):
        try:
            not_interested_button = self.driver.find_element('xpath',
                                                             '/html/body/div[2]/div/div/div/div/div[3]/button[2]/div['
                                                             '2]/div[2]/div')
            not_interested_button.click()
        except:
            print('no popup')

    def accept_location(self):
        try:
            notifications_button = self.driver.find_element('xpath',
                                                            '/html/body/div[2]/div/div/div/div/div[3]/button[1]/div[2]/div[2]')
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
        sleep(1)
        self.close_cookies()
        sleep(1)
        email_field = self.driver.find_element(By.NAME, 'email')
        pw_field = self.driver.find_element(By.NAME, 'pass')
        login_button = self.driver.find_element(By.NAME, 'login')
        email_field.send_keys(email)
        pw_field.send_keys(password)
        login_button.click()
        self.driver.switch_to.window(base_window)
        sleep(6)
        self.accept_location()
        sleep(2)
        self.accept_popup()

    def right_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_RIGHT)

    def left_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_UP)
        ts = get_current_timestamp()

        try:
            img_element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="profileCard__slider__img Z(-1)"]')))
            style = img_element.get_attribute('style')
            positions = [pos for pos, char in enumerate(style) if char == '"']
            img_name = user_photo_dir + ts + ".png"
            img_source = str(style)[positions[0] + 1:positions[1]]
            with urlopen(img_source) as in_stream, open(img_name, 'wb') as out_file:
                copyfileobj(in_stream, out_file)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            print("couldnt find photo")

        doc.send_keys(Keys.SPACE)

        # USER NAME

        try:
            user_name_element = self.driver.find_element('xpath', '//div[@class="Ov(h) Ws(nw) Ell"]')
            user_name = unicodedata.normalize('NFKD',
                                              user_name_element.text.replace("ł", "l").replace("Ł", "L")).encode(
                'ascii', 'ignore').decode('utf-8')
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

        # USER VERIFICATION CHECK

        try:
            _ = self.driver.find_element('xpath', '//div[@class="D(ib) Lh(0) Sq(30px) Mstart(4px) As(c)"]')
            user_verified = "yes"
        except:
            user_verified = "no"

        # USER LOCATION

        try:
            user_location_element = self.driver.find_element(By.XPATH, '//div[contains(text(), "Mieszka w")]')
            user_location = unicodedata.normalize('NFKD', user_location_element.text[10:].replace("ł", "l").replace("Ł",
                                                                                                                    "L")).encode(
                'ascii', 'ignore').decode('utf-8')
        except:
            user_location = "null"

        # USER SMOKING HABIT

        try:
            user_smoking_element = self.driver.find_element(By.XPATH,
                                                            '//div[contains(text(), "alę") or contains(text(), '
                                                            '"Próbuję rzucić")]')
            switch = {
                "Nie palę": "don't smoke",
                "Palę": "smoke",
                "Palę tylko dla towarzystwa": "smoke for company",
                "Palę do alkoholu": "smoke while drinking",
                "Próbuję rzucić": "trying to quit smoking"
            }
            user_smoking = switch.get(user_smoking_element.text, "null")
        except:
            user_smoking = "null"

        # USER DRINKING HABIT

        xpaths = [
            ('//div[contains(text(), "To nie dla mnie")]', "no"),
            ('//div[contains(text(), "Już nie piję")]', "no"),
            ('//div[contains(text(), "Próbuję ograniczać")]', "sometimes"),
            ('//div[contains(text(), "Tylko okazjonalnie")]', "sometimes"),
            ('//div[contains(text(), "Towarzysko w weekendy")]', "sometimes"),
            ('//div[contains(text(), "Prawie co wieczór")]', "a lot")
        ]

        user_drinking = "null"
        for xpath, value in xpaths:
            try:
                _ = self.driver.find_element(By.XPATH, xpath)
                user_drinking = value
                break
            except:
                continue

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
            user_description_element = self.driver.find_element('xpath',
            '//div[@class="react-aspect-ratio-placeholder"]').find_element('xpath',
            '..').find_elements(By.XPATH, '*')[1].find_elements(By.XPATH,
            '*')[2].find_elements(By.XPATH, '*')[0].text
            user_description = unicodedata.normalize('NFKD', remove_emojis(user_description_element)
                                                     .replace("ł", "l").replace("Ł", "L")
                                                     .replace("\n", " ")).encode('ascii', 'ignore').decode('utf-8')
        except:
            user_description = "null"

        # USER INTERESTS

        try:
            user_interest_element = self.driver.find_element('xpath', "//h2[text()='Zainteresowania']").find_element(
                'xpath', '..')
            user_interests = user_interest_element.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[
                0].find_elements(By.XPATH, '*')

            user_interest_list = [unicodedata.normalize('NFKD', interest.text
                                                        .replace("ł", "l").replace("Ł", "L"))
                                  .encode('ascii', 'ignore')
                                  .decode('utf-8') for interest in user_interests]

            user_interest_list += ["null"] * (5 - len(user_interest_list))
        except:
            user_interest_list = ["null"] * 5

        with open(user_data_json_path) as fp:
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
            "interests": user_interest_list[:5],
            "description": user_description
        })
        with open(user_data_json_path, 'w') as json_file:
            json.dump(users_list, json_file, ensure_ascii=False,
                      indent=4,
                      separators=(',', ': '))

        doc.send_keys(Keys.ARROW_LEFT)

    def auto_swipe(self):
        while True:
            sleep(2)
            try:
                self.right_swipe()
            except:
                print("couldn't swipe right")


if __name__ == "__main__":
    create_necessary_directories()
    bot = TinderBot()
    bot.open_tinder()
    for i in range(6):
        bot.left_swipe()
    bot.close_tinder_on_desktop()
    while True:
        bot.left_swipe()
