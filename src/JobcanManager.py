import os
import datetime
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from dotenv import load_dotenv
import jpholiday


# ベースディレクトリ
BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..")
# ブラウザ用ドライバ用パス
GECKODRIVER_PATH = os.path.join(
    os.path.join(BASE_DIR, "driver"), "geckodriver")
# ログイン用URL
LOGIN_URL = f'https://id.jobcan.jp/users/sign_in?app_key=atd'


class JobcanManager:

    def __init__(self) -> None:
        load_dotenv()
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        self.wait_sec = int(os.getenv('WAIT_SEC'))
        self.start_time = self._create_random_time(base_time=os.getenv('START_TIME'))
        self.end_time = self._create_random_time(base_time=os.getenv('END_TIME'))

    def _destroy(self) -> None:
        self.driver.close()

    def _create_random_time(self, base_time: str) -> str:
        time_obj = datetime.datetime.strptime(base_time, "%H:%M")
        random_minutes = random.randint(0, 8)
        new_time_obj = time_obj + datetime.timedelta(minutes=random_minutes)
        return new_time_obj.strftime("%H:%M")

    def _config_driver(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)


    def _login(self) -> None:
        self.driver.get(LOGIN_URL)
        # それぞれの情報を取得
        user_email_element = self.driver.find_element(By.ID, 'user_email')
        user_email_element.send_keys(self.email)
        user_password_element = self.driver.find_element(By.ID, 'user_password')
        user_password_element.send_keys(self.password)
        # ログインボタン押下
        login_button_element = self.driver.find_element(By.ID, 'login_button')
        login_button_element.send_keys(Keys.ENTER)
        # ページ遷移待機時間
        time.sleep(self.wait_sec)

    
    def _is_workday(self, now: datetime.datetime) -> bool:
        return (now.weekday() in [0, 1, 2, 3, 4]) and not (jpholiday.is_holiday(now))
    
    
    def _is_time_stamp_datetime(self, now: datetime.datetime) -> bool:
        now_string = now.strftime("%H:%M")
        return (now_string == self.start_time) or (now_string == self.end_time)


    def _time_stamp(self) -> None:
        # 「在宅」を選択
        selection_element = self.driver.find_element(By.ID, 'new_selection')
        select = Select(selection_element)
        select.select_by_index(1)
        # 打刻
        push_button_element = self.driver.find_element(By.ID, 'adit-button-push')
        push_button_element.send_keys(Keys.ENTER)


    def execute(self) -> None:
        print("--- start process ---")
        now = datetime.datetime.now()
        print('now: {}'.format(now.strftime("%Y/%m/%d %H:%M:%S")))
        if self._is_workday(now=now) and self._is_time_stamp_datetime(now=now):
            print('execute time stamp: {}'.format(now.strftime("%H:%M")))
            self._config_driver()
            # ログイン
            self._login()
            # 打刻
            self._time_stamp()
            self._destroy()
            print('completed.')
        else:
            print('not working datetime')
        print("--- end process ---")


if __name__ == '__main__':
    jobcan_manager = JobcanManager()
    jobcan_manager.execute()
