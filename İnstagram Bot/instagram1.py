from selenium import webdriver
from userİnfo import username, password,aradiginusername
from selenium.webdriver.common.keys import Keys
import time

class Instagram:


    def __init__(self, username, password,aradiginusername):
        self.username = username
        self.password = password
        self.aradiginusername=aradiginusername
        self.followers = []
        self.browserProfile = webdriver.ChromeOptions()
        #butonlari kontrol etmek icin dili ing ayarlama
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages':'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)

        
    #hesaba giris yapma
    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        usernameInput = self.browser.find_element_by_name('username')
        passwordInput = self.browser.find_element_by_name('password')

        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)

        passwordInput.send_keys(Keys.ENTER)

        time.sleep(4)

        
    #arasigin hesabın followelarını alma
    def getFollowers(self, max):
        self.browser.get(f"https://www.instagram.com/{self.aradiginusername}")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(2)
        modal=self.browser.find_element_by_css_selector("div[role=dialog] ul")
        count=len(modal.find_elements_by_css_selector("li"))
        print(f"ilk sayi:{count}")
        action=webdriver.ActionChains(self.browser)

        while count<max:
            modal.click()

            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)

            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)

            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)

            newCount = len(modal.find_elements_by_tag_name("li"))

            if count != newCount:
                count = newCount
                print(f"takipçi sayısı: {count}")
                time.sleep(1)
            else:
                break

        i = 0
        followers = modal.find_elements_by_tag_name("li")
        for user in followers:
            link = user.find_element_by_tag_name("a").get_attribute("href")
            self.followers.append(link)
            i += 1
            if i == max:
                break

        self.saveToFile(self.followers)
    #followeları dosyaya kaydetme
    def saveToFile(self, followers):
        with open("followers.txt", "w", encoding="UTF-8") as file:
            for user in followers:
                file.write(user + "\n")
    #otomatik takip
    def followUser(self, username):
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(1)

        followButton = self.browser.find_element_by_tag_name("button")

        if followButton.text == "Follow" or followButton.text == "Follow":
            followButton.click()
            time.sleep(2)
        else:
            print(f"{username} sayfasını zaten takip ediyorsunuz.")

    def followUsers(self, users):
        for user in users:
            self.followUser(user)
    #otomatik unfollow
    def unFollowUser(self, username):
        self.browser.get(f"https://www.instagram.com/{username}/")

        btn = self.browser.find_element_by_tag_name('button')

        if btn.text == "Message":
            self.browser.find_elements_by_tag_name('button')[1].click()
            time.sleep(2)

            self.browser.find_element_by_css_selector('div[role=dialog] button').click()
        else:
            print(f"{username} sayfasını zaten takip etmiyorsunuz.")

    def unFollowUsers(self, users):
        for user in users:
            self.unFollowUser(user)

    def __del__(self):
        time.sleep(10)
        self.browser.close()

app = Instagram(username, password,aradiginusername)

app.signIn()    
app.followUsers(["zeynouzmez"])
app.unFollowUsers(["zeynouzmez"])
app.getFollowers(50)