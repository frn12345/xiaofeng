import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

# 大麦网主页
damai_url = "https://www.damai.cn/"
# 登录页
login_url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
# 抢票目标页
target_url = 'https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_2.591b23e1HR8K6w&id=762298097902'

class Concert:
    def __init__(self):
        self.status = 0         # 状态,表示如今进行到何种程度
        self.login_method = 1   # {0:模拟登录,1:Cookie登录}
        edge_driver_path = 'D:\MyDownload\PyCharm\edgeriver\msedgedriver.exe'  # Edge WebDriver的路径
        service = Service(edge_driver_path)
        self.driver = webdriver.Edge(service=service)

    def set_cookie(self):
        self.driver.get(damai_url)
        print("###请点击登录###")
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            time.sleep(1)
        print('###请扫码登录###')

        while self.driver.title != '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
            time.sleep(1)
        print("###扫码成功###")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")
        self.driver.get(target_url)

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',
                    'name': cookie.get('name'),
                    'value': cookie.get('value')
                }
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

    def login(self):
        if self.login_method == 0:
            self.driver.get(login_url)
            print('###开始登录###')

        elif self.login_method == 1:
            if not os.path.exists('cookies.pkl'):
                self.set_cookie()
            else:
                self.driver.get(target_url)
                self.get_cookie()

    def enter_concert(self):
        print('###打开浏览器，进入大麦网###')
        self.driver.maximize_window()
        self.login()
        self.status = 2
        print("###登录成功###")

    def choose_ticket(self):
        if self.status == 2:
            print("="*30)
            print("###检查是否开始售票###")
            while not self.isElementExistByClass('buy-link'):
                self.driver.refresh()
                print("###售票尚未开始,刷新等待开始###")
            self.driver.find_element(By.CLASS_NAME, 'buy-link').click()
            time.sleep(1.5)
            self.check_order()

    def check_order(self):
        if self.status == 2:
            print('###开始确认订单###')
            if self.driver.title == '订单确认页':
                print('###检查是否需要填写观影人')
                if self.isElementExistByXPath('//*[@id="dmViewerBlock_DmViewerBlock"]'):
                    self.driver.find_element(By.XPATH,
                                             '//*[@id="dmViewerBlock_DmViewerBlock"]/div[2]/div/div').click()
                    time.sleep(0.5)
                print('###跳转支付选择界面###')
                self.driver.find_element(By.XPATH,
                                         '//*[@id="dmOrderSubmitBlock_DmOrderSubmitBlock"]/div[2]/div/div[2]/div['
                                         '2]/div[2]').click()
                time.sleep(2)
                self.pay_order()

    def pay_order(self):
        if self.driver.title == "支付宝付款":
            print('###支付订单###')
            if self.isElementExistByXPath('//*[@id="app"]/div[3]/div[1]/button[2]'):
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[1]/button[2]').click()
                print('###跳转至浏览器支付###')
                time.sleep(1.5)
                # 输入支付宝账号和密码等后续操作...
                # 注意：此处应避免存储或硬编码敏感信息
                # 通常，支付环节应由用户手动完成

    def isElementExistByClass(self, class_name):
        try:
            self.driver.find_element(By.CLASS_NAME, class_name)
            return True
        except:
            return False

    def isElementExistByXPath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False

    def finish(self):
        self.driver.quit()

if __name__ == '__main__':
    try:
        con = Concert()
        con.enter_concert()
        con.choose_ticket()

    except Exception as e:
        print(e)
        con.finish()