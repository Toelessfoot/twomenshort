from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from random import randrange

url = "https://www.ashl.ca/stats-and-schedules/ashl/york-summer/#/schedule?league=6"
#url = "https://www.canadacomputers.com"

with open("path.txt", "r") as f:
    chrome_user_path = f.read()

options = Options()
options.add_argument(f'user-data-dir={chrome_user_path}')

driver = webdriver.Chrome("../chromedriver", options=options)
def goto_whatsapp():
    driver.get("https://web.whatsapp.com/")
    sleep(10)
    elem = driver.find_elements(By.CSS_SELECTOR, ".lhggkp7q.ln8gz9je.rx9719la")
    for i in elem:
        print(i.text)
        if "2 Men Short" in i.text:
            i.click()
            break
    sleep(10)

    while True:
        messages = driver.find_elements(By.CSS_SELECTOR, "._11JPr.selectable-text.copyable-text")
        last = len(messages) - 1
        print(len(messages))
        for i in messages:
            print(i.text)

        print(f"last message: {messages[last].text}")
        if messages[last].text == "/schedule":
            print("dooooo it")
            return messages[last].text
            break
        elif messages[last].text == "/stats":
            print("dooooo it")
            return messages[last].text
            break
        sleep(10)

def get_schedule():
    while True:
        driver.get(url)
        sleep(5)
        elem = driver.find_elements(By.TAG_NAME, 'iframe')
        print(len(elem))
        driver.switch_to.frame(driver.find_element(By.ID, 'sportninja-target'))
        elem = driver.find_elements(By.TAG_NAME, "a")
        print(elem)
        print(len(elem))

        for i in elem:
            print(i.text)

        try:
            elem[3].click()
            break
        except:
            print('click failed')
            sleep(5)
    sleep(5)
    elem = driver.find_elements(By.CSS_SELECTOR, ".css-14oqdsi.ex0kc8o2")
    for i in elem:
        print(i.text)
        if i.text == "2 Men Short":
            i.click()
            break
    sleep(5)
    elem = driver.find_elements(By.CLASS_NAME, "game-list-row")
    games = ''
    for i in elem:
        print(i.text)
        games += i.text
        print("_________________________")
        games += "\n_________________________\n"
    return games

def get_stats():
    while True:
        driver.get(url)
        sleep(5)
        elem = driver.find_elements(By.TAG_NAME, 'iframe')
        print(len(elem))
        driver.switch_to.frame(driver.find_element(By.ID, 'sportninja-target'))
        elem = driver.find_elements(By.TAG_NAME, "a")
        print(elem)
        print(len(elem))

        for i in elem:
            print(i.text)

        try:
            elem[3].click()
            break
        except:
            print('click failed')
            sleep(5)
    sleep(5)
    elem = driver.find_elements(By.CSS_SELECTOR, ".css-14oqdsi.ex0kc8o2")
    for i in elem:
        print(i.text)
        if i.text == "2 Men Short":
            i.click()
            break
    sleep(5)
    elem = driver.find_elements(By.CSS_SELECTOR, ".is-team-or-schedule.css-1exk9nq")[1].click()  #click on stats
    sleep(5)
    players = driver.find_elements(By.CSS_SELECTOR, ".list-row.css-r9opqo.ex0kc8o2")  #gets stats
    rows = [['Player', 'GP', 'G', 'A', 'P', 'PIM', 'PTS/G', 'TOI']]
    output = '```'
    longest_name = 0
    for player in players:
        row = []
        toi = ''
        arr = player.text.split('\n')
        for i in arr:
            row.append(i)
        if arr[0] == "Nicholas Fatsis":
            toi = "3.25 x 10⁵"
        else:
            toi = str(randrange(30, 60))
        row.append(toi)
        len(row)
        rows.append(row)
        if len(arr[0]) > longest_name:
            longest_name = len(arr[0])

    for row in rows:
        output += f"{row[0]:{longest_name}} {row[1]:4} {row[2]:4} {row[3]:4} {row[4]:4} {row[5]:4} {row[6]:6} {row[7]:10}\n"
    output += '```'
    print(output)
    sleep(10)
    return output

def post_whatsapp(content):
    driver.get("https://web.whatsapp.com/")
    sleep(10)
    elem = driver.find_elements(By.CSS_SELECTOR, ".lhggkp7q.ln8gz9je.rx9719la")
    for i in elem:
        print(i.text)
        if "2 Men Short" in i.text:
            i.click()
            break
    sleep(10)
    input_box = driver.find_elements(By.CSS_SELECTOR, ".selectable-text.copyable-text.iq0m558w.g0rxnol2")[1]
    if '\n' in content:
        content_bits = content.split('\n')
        for bit in content_bits:
            input_box.send_keys(bit)
            input_box.send_keys(Keys.SHIFT, Keys.ENTER)
        input_box.send_keys(Keys.ENTER)
    else:
        sleep(10)
        input_box.send_keys(content)
        input_box.send_keys(Keys.ENTER)
    print(content)
    sleep(10)

while True:
    command = goto_whatsapp()
    if command == "/schedule":
        schedule = get_schedule()
        post_whatsapp(schedule)
    elif command == "/stats":
        stats = get_stats()
        post_whatsapp(stats)
    sleep(10)
