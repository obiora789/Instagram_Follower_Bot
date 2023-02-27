from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains, ScrollOrigin
import dotenv
import os
import time
import random

new_file = dotenv.find_dotenv()
dotenv.load_dotenv(new_file)

MY_NAME = os.environ.get("NAME")
INSTAGRAM_URL = "https://www.instagram.com/"
TARGET_ACCOUNT = os.environ.get("CELEBRITY_ACCOUNT")
print(TARGET_ACCOUNT)
CHROME_DRIVER = os.environ.get("CHROME_PATH")
USERNAME = os.environ.get("USER_NAME")
PASSWORD = os.getenv("PASS_WORD")
SERVICE = Service(executable_path=CHROME_DRIVER)
SHORT = 3
DELAY = 5  # delay time
END = 9  # end of random delay
LIMIT = 5  # determines when the program ends
ORIGIN = 0


def generate_random_time(number_of_secs):
    """Generates a random time between 1 and 5 seconds once it receives the number of seconds"""
    return round(random.randint(DELAY, END) / 10, 1) * number_of_secs


class InstaFollower:
    """This class takes care of all """

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values":
                {
                    "geolocation": 1,  # enables location settings
                    'notifications': 0,  # disables notifications
                },
            'profile.managed_default_content_settings':
                {
                    'geolocation': 1  # sets your current location
                }
        }
        self.options.add_experimental_option("prefs", prefs)
        self.options.add_argument("--disable-popup-blocking")  # allows pop-ups to input your gmail login details
        self.driver = webdriver.Chrome(service=SERVICE, options=self.options)
        self.mouse_pointer = ActionChains(self.driver)
        self.follow_buttons = None
        self.account_record_divs = None
        self.unfollow_buttons = None
        self.scroll_window = True

    def login(self):
        """This method handles your Instagram account login processes."""
        self.driver.get(url=INSTAGRAM_URL)  # Loads instagram url
        time.sleep(DELAY)
        WebDriverWait(self.driver, DELAY ** DELAY).until(ec.element_to_be_clickable(self.driver.find_element(By.CLASS_NAME, "_aa4b")))
        login_details = self.driver.find_elements(By.CLASS_NAME, "_aa4b")
        for index in range(len(login_details)):
            self.mouse_pointer.click(on_element=login_details[index]).perform()
            time.sleep(generate_random_time(SHORT))
            login_details[index].clear()
            time.sleep(generate_random_time(SHORT))
            if index == 0:
                login_details[index].send_keys(USERNAME)
            else:
                login_details[index].send_keys(PASSWORD)
            time.sleep(generate_random_time(SHORT))
        WebDriverWait(self.driver, DELAY ** SHORT).until(ec.element_to_be_clickable(self.driver.find_element(By.CLASS_NAME, "_abak")))
        buttons = self.driver.find_elements(By.CLASS_NAME, "_abak")
        for login_button in buttons:
            if login_button.text == "Log in":
                self.mouse_pointer.move_to_element(login_button).click().perform()
                break
        time.sleep(DELAY * SHORT)
        not_now = WebDriverWait(self.driver, DELAY*DELAY).until(ec.element_to_be_clickable(self.driver.find_element(By.CLASS_NAME, "_acao")))
        self.mouse_pointer.move_to_element(not_now).click().perform()  # clicks 'not now' to discard login information
        time.sleep(generate_random_time(DELAY))
        no_notification = self.driver.find_element(By.CLASS_NAME, "_a9_1")
        self.mouse_pointer.move_to_element(no_notification).click().perform()
        time.sleep(generate_random_time(DELAY))

    def scroll_effect(self, button_container: list, follow_method: bool):
        count = 0
        button_count = 0
        follow_string = ""
        for index in range(len(button_container)):
            count += 1
            try:
                print(f"Unfollow Button: {button_container[index].text}")
            except StaleElementReferenceException:
                break
            if follow_method:
                if button_container[index].text == "Follow":
                    self.mouse_pointer.click(on_element=button_container[index]).perform()
                    button_count += 1
                    follow_string = "follow"
                    time.sleep(generate_random_time(DELAY))
                elif button_container[index].text == "Following" or button_container[index].text == "Requested":
                    pass
            else:
                if button_container[index].text == "Following" or button_container[index].text == "Requested":
                    self.driver.execute_script("arguments[0].click();", button_container[index])
                    time.sleep(generate_random_time(DELAY))
                    unfollow_window = WebDriverWait(self.driver, DELAY ** SHORT).until(ec.element_to_be_clickable(self.driver.find_element(By.CLASS_NAME, "_a9-_")))
                    self.mouse_pointer.click(on_element=unfollow_window).perform()
                    button_count += 1
                    follow_string = "unfollow"
                    time.sleep(generate_random_time(DELAY))
                elif button_container[index].text == "Follow":
                    pass
            if count > SHORT:  # Condition to begin scrolling through the list for User experience purposes.
                scroll_from = ScrollOrigin.from_element(button_container[index])
                last_height = self.driver.execute_script("return document.querySelector('._aba8').scrollHeight")
                print(f"Last height: {last_height}")    # height of each follower container in follower list
                if button_count <= SHORT + SHORT:
                    self.mouse_pointer.scroll_from_origin(scroll_from, ORIGIN, last_height + SHORT).perform()
                else:
                    self.mouse_pointer.scroll_from_origin(scroll_from, ORIGIN, last_height).perform()
                time.sleep(generate_random_time(SHORT - 1))
            if button_count >= LIMIT:   # Stops the program once button count reaches or surpasses the limit.
                self.scroll_window = False
                print(f"Good bye, I'm terminating the program after {button_count} {follow_string}s.")
                break

    def find_followers(self):
        """This method loads the target(celebrity) account and clicks their number of followers"""
        self.driver.get(url=TARGET_ACCOUNT)     # the target account
        time.sleep(DELAY)
        self.account_record_divs = self.driver.find_elements(By.CSS_SELECTOR, ".xjbqb8w ._ac2a")
        print(f"Number of followers: {self.account_record_divs}")
        time.sleep(generate_random_time(DELAY))
        follow_divs = self.driver.find_elements(By.CLASS_NAME, "_aacw")
        for div in follow_divs:
            print(f"Follow: {div.text}")
            if div.text == "Follow":        # to follow the target account
                self.mouse_pointer.click(on_element=div).perform()    # click to follow target account
                break
            elif div.text == "Following":
                break
        time.sleep(generate_random_time(DELAY))
        self.driver.execute_script("arguments[0].click();", self.account_record_divs[1])    # clicks followers' list
        time.sleep(generate_random_time(DELAY * SHORT))

    def follow(self):
        """This method generates a list from the 'number of followers' and follows all accounts in that list."""
        while self.scroll_window:  # continue scrolling and loading followers to be unfollowed
            time.sleep(SHORT - 1)
            try:
                self.follow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "._abb0 ._acas ._ab9x")
                test = self.follow_buttons[0]   # list of followers to be followed
                print(f"List of Followers: {self.follow_buttons}")
            except IndexError:
                self.follow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "._abb0 ._acat ._ab9x")
                print(f"List of Followers 2: {self.follow_buttons}")   # list of followers already followed
            self.scroll_effect(button_container=self.follow_buttons, follow_method=True)

    def unfollow(self):
        """This method unfollows all accounts in the list of accounts previously followed."""
        while self.scroll_window:  # continue scrolling and loading followers to be unfollowed
            time.sleep(SHORT - 1)
            try:
                self.unfollow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "._abb0 ._acat ._ab9x")
                print(f"List of Followers 2: {self.unfollow_buttons}")
                self.unfollow_buttons = self.unfollow_buttons[1:]   # list of followers to be unfollowed
                test = self.unfollow_buttons[0]
            except IndexError:
                self.unfollow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "._abb0 ._acas ._ab9x")
                self.unfollow_buttons = self.unfollow_buttons[1:]       # list of followers already unfollowed
                print(f"List of Followers: {self.unfollow_buttons}")
            self.scroll_effect(button_container=self.unfollow_buttons, follow_method=False)


chosen_method = input("Type 'Follow' or 'Unfollow' to follow/unfollow accounts.\n").lower()
print(f"You have chosen to {chosen_method} accounts.")
insta = InstaFollower()
insta.login()
insta.find_followers()
if chosen_method == "follow":
    insta.follow()
elif chosen_method == "unfollow":
    insta.unfollow()
else:
    insta.follow()
