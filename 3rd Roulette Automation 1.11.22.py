#ALL THE NECESSARY IMPORTS
import os
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from datetime import datetime,timedelta
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#FUNCTION TO ASSIGN CHROME WEBDRIVER
def create_webdriver_instance():
    driver=webdriver.Chrome(ChromeDriverManager().install())
    return driver

def traverse_to_page(url, driver):
    try:
        driver.get(url)
    except :
        print("Timeout page")
        return driver
    
    return driver

def login(driver,username, password):
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "fn-user-name.username")))
        driver.find_element_by_class_name('fn-user-name.username').send_keys(username)
        driver.find_element_by_class_name('fn-input-type-password').send_keys(password)
        driver.find_element_by_class_name('btn.fn-login-btn.btn_type_popup-login.btn_action_login').click()
        
    except :
        print("Timeout - login")
        return driver
    time.sleep(9)
    return driver




def traverse_to_roulette_1(url,driver):
    try:
        time.sleep(2)
        driver.get(url)
             
    except :
        print("Timeout to traverse to page")
        return driver
    
    return driver
        

def stats_page(driver):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "li")))
        e = driver.find_elements_by_tag_name("li") 
        if(len(e)>0):
            time.sleep(1)
            ActionChains(driver).click(e[4]).perform()
    except :
        print("Timeout - stats-page")
        return driver
    
    return driver


def stats_info(driver):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div[2]/div[11]/div/div[2]/div/div/div/div[1]/div/div[1]/div/div')))
        ele = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/div[2]/div[11]/div/div[2]/div/div/div/div[1]/div/div[1]/div/div')
    except :
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div[2]/div[11]/div/div[2]/div/div/div/div[1]/div/div[1]/div/div')))
            ele = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/div[2]/div[11]/div/div[2]/div/div/div/div[1]/div/div[1]/div/div')
        except:
            print("Timeout - stats info")
            return driver
    
    return ele

def money_details(driver):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "balance__value")))
        balance = driver.find_element_by_class_name('balance__value').text
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "balance__value")))
        bet = driver.find_element_by_class_name('account-panel__value').text
    except :
        balance = 0
        bet = 0
        
    return(balance,bet)

def mail(para):
    fromaddr = para['fromaddr']
    toaddr = para['toaddr']
    sender_pass = para['sender_pass']

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Roulette"
    body = "OOPS SORRY! \n END OF GAME"
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, sender_pass)
    text = msg.as_string()
    #s.sendmail(fromaddr, toaddr, text)
    s.quit()


def main(url,username, password):
    driver = create_webdriver_instance()
    driver = traverse_to_page(url, driver)
    if not driver:
        return (False)
    time.sleep(1)
    driver = login(driver,username, password)
    time.sleep(10)
    url1 = "https://games.mansioncasino.com/live/desktop/bundles/21.12.5.24/?gametype=rol&connection=desktop&physicalnetworkId=-1&protocol=Live2&preferredSeat=undefined&preferedmode=real&mode=real&sessionTimer=null&launcher_time="
    url2 = str(int(time.time()))
    url3 = "&redirect_time=1645551083374&launch_alias=direct_launch_1642&backUrl=https%3A%2F%2Fgames.mansioncasino.com%2Flive%2Fdesktop%2Frol%2F%3Fgametype%3Drol%26connection%3Ddesktop%26tableId%3D1642%26physicalTableId%3D-1%26networkId%3D-1%26protocol%3DLive2%26preferredSeat%3Dundefined%26preferedmode%3Dreal%26mode%3Dreal%26sessionTimer%3Dnull%26"
    url = url1+url2+url3
    driver = traverse_to_roulette_1(url,driver)
    time.sleep(2)
    
    return driver
 
    
def bet_creator(driver, bet_limit , parameter,total_bet,para):
    
    limit_left = str((total_bet-bet_limit)+1)
    
    try:
        e = driver.find_elements_by_tag_name("li")
        ActionChains(driver).click(e[7]).perform()
    except :
        pass
    
    try:
        e = driver.find_elements_by_class_name("favourite-bet__name-text")
        for j,i in enumerate(e):
            try:
                click_ele_text = i.get_attribute("innerText")
                check = limit_left+' '+parameter
                zero_check = limit_left+' Zero'
                if(click_ele_text == check):
                    time.sleep(0.5)
                    e[j].click()
                    print(click_ele_text)
                if(click_ele_text == zero_check):
                    time.sleep(0.5)
                    e[j].click()
                    print(click_ele_text)
            except:
                try:
                    click_ele_text = i.get_attribute("innerText")
                    check = limit_left+' '+parameter
                    zero_check = limit_left+' Zero'
                    if(click_ele_text == check):
                        time.sleep(0.5)
                        e[j].click()
                        print(click_ele_text)
                    if(click_ele_text == zero_check):
                        time.sleep(0.5)
                        e[j].click()
                        print(click_ele_text)
                except:
                    pass
                
    except:
        pass
            
    try:
        e = driver.find_elements_by_tag_name("li")
        ActionChains(driver).click(e[7]).perform() 
    except :
        pass
    
    balance,bet = money_details(driver)
    if(int(float(balance.replace(",","").split(" ")[-1]))==0):
        mail(para)
        time.sleep(1)
        sys.exit("Game Over")
        
    print("\nBalance = ", balance)
    print("Bet = ", bet)
    
    return
def continuity_check(continuity,driver,output,parameter):
    time.sleep(0.5)
    
    if driver:
        statistics = stats_info(driver)
    else:
        return

    if statistics:
        arr = statistics.find_elements_by_tag_name('div')

    green = 'rgba(18, 149, 18, 1)'
    black = 'rgba(255, 255, 255, 1)'
    red = 'rgba(255, 0, 0, 1)'

    result = []

    for i in range(0,last_num*4,4):
        temp = []
        try:
            temp.append(int(arr[i].get_attribute("innerText")))
            temp.append(arr[i].value_of_css_property('color'))
            result.append(temp)
        except:
            pass 
    
    if(result!=output and len(result) == last_num):
        if(parameter == "1-18"):
            if(result[0][0]<19 or result[0][0]==0) : 
                return (False)

        if(parameter == "19-36"):
            if(result[0][0]>18 or result[0][0]==0) : 
                return (False)


        if(parameter == "Red"):
            if(result[0][1] != 'rgba(255, 255, 255, 1)'  or result[0][0] == 0 ) : 
                return (False)


        if(parameter == "Black"):
            if(result[0][1] != 'rgba(255, 0, 0, 1)' or result[0][0] == 0 ) :
                return (False)


        if(parameter == "Odd"):
            if(result[0][0]%2 != 0 or result[0][0] == 0 ) : 
                return (False)


        if(parameter == "Even"):
            if(result[0][0]%2 == 0 or result[0][0] == 0 ) :
                return (False)

        continuity = continuity_check(continuity,driver,result,parameter)

    else:
        time.sleep(1)
        continuity = continuity_check(continuity,driver,result,parameter)
    

def bet_check(driver,output,parameter,limit,para):
    
    time.sleep(2)
    
    if(limit==0):
        continuity = True
        while (continuity):
            continuity = continuity_check(continuity,driver,output,parameter)
        return

    if driver:
        statistics = stats_info(driver)
    else:
        return

    if statistics:
        arr = statistics.find_elements_by_tag_name('div')

    green = 'rgba(18, 149, 18, 1)'
    black = 'rgba(255, 255, 255, 1)'
    red = 'rgba(255, 0, 0, 1)'

    result = []

    for i in range(0,last_num*4,4):
        temp = []
        try:
            arr[i].get_attribute("innerText")
            temp.append(int(arr[i].get_attribute("innerText")))

            colour = arr[i].value_of_css_property('color')
            temp.append(colour)
            result.append(temp)
        except:
            pass 
        
    
    
    if(result!=output and len(result) == last_num):
        output = result
        if(parameter == "1-18"):
            if(result[0][0]<19 or result[0][0] == 0 ) : 
                print("\nYOU WON ")
                return
            else:
                bet_creator(driver, limit , parameter,total_bet,para)
                bet_check(driver,result,parameter,limit-1,para)
                return
        
        if(parameter == "19-36"):
            if(result[0][0]>18 or result[0][0] == 0 ) : 
                print("\nYOU WON")
                return
            else:
                bet_creator(driver, limit , parameter,total_bet,para)
                bet_check(driver,result,parameter,limit-1,para)
                return
        
        if(parameter == "Red"):
            if(result[0][1] == 'rgba(255, 0, 0, 1)' or result[0][0] == 0 ) : 
                print("\nYOU WON")
                return
            else:
                bet_creator(driver, limit , parameter,total_bet,para)
                bet_check(driver,result,parameter,limit-1,para)
                return
        
        if(parameter == "Black"):
            if(result[0][1] == 'rgba(255, 255, 255, 1)' or result[0][0] == 0 ) : 
                print("\nYOU WON")
                return
            else:
                bet_creator(driver, limit , parameter,total_bet,para)
                bet_check(driver,result,parameter,limit-1,para)
                return
        
        if(parameter == "Odd"):
            if(result[0][0]%2 != 0 or result[0][0] == 0 ) : 
                print("\nYOU WON")
                return
            else:
                bet_creator(driver, limit , parameter,total_bet,para)
                bet_check(driver,result,parameter,limit-1,para)
                return
        
        if(parameter == "Even"):
            if(result[0][0]%2 == 0 or result[0][0] == 0 ) : 
                print("\nYOU WON")
                return
            else:
                bet_creator(driver, limit , parameter,total_bet,para)
                bet_check(driver,result,parameter,limit-1,para)
                return
    else:
        bet_check(driver,output,parameter,limit,para)
        return
    


    
if __name__ == '__main__':
    
    mail_info = pd.read_excel('mailing_info.xlsx')
    from_address = mail_info["from"][0]
    to_address = mail_info["to"][0]
    sender_password = mail_info["password"][0]
    
    para = {'fromaddr': from_address, 'toaddr': to_address, 'sender_pass':sender_password}
    
    url = 'https://play.mansioncasino.com/login/'
    username='abhijeetpanda'
    password='bapuji@hariom'
    
    driver = main(url,username, password)
    time.sleep(20)
    exit = 3
    strike = 20
    total_bet = 3
    last_num = 15

    limit = total_bet
    exit_limit = 0
    
    green = 'rgba(18, 149, 18, 1)'
    black = 'rgba(255, 255, 255, 1)'
    red = 'rgba(255, 0, 0, 1)'

    start_time = datetime.now()
    
    if driver:
        driver = stats_page(driver)

    time.sleep(2)

    if driver:
        statistics = stats_info(driver)
    
    while True:
        
        print ("\n ----------RUNNING EXIT CODE-------- \n")
        
        while (exit_limit == 0):            

            if statistics:
                arr = statistics.find_elements_by_tag_name('div')
            result = []

            for i in range(0,exit*4,4):
                temp = []
                try:
                    arr[i].get_attribute("innerText")
                    temp.append(int(arr[i].get_attribute("innerText")))
                    colour = arr[i].value_of_css_property('color')

                    temp.append(colour)
                    result.append(temp)
                except:
                    pass

            print(result)

            df = pd.DataFrame(result)

            if( len(df)==exit and 0 not in df[0].tolist() ):

                if( all(df[0][:]>18) ):
                    continuity = True
                    while (continuity):
                        continuity = continuity_check(continuity,driver,result,"1-18")
                    exit_limit = 1
                    continue

                elif( all(df[0][:]<19) ):
                    continuity = True
                    while (continuity):
                        continuity = continuity_check(continuity,driver,result,"19-36")
                    exit_limit = 1
                    continue

                else:
                    if( all(df[1][:]==black) ):
                        continuity = True
                        while (continuity):
                            continuity = continuity_check(continuity,driver,result,"Red")
                        exit_limit = 1
                        continue

                    elif( all(df[1][:]==red) ):
                        continuity = True
                        while (continuity):
                            continuity = continuity_check(continuity,driver,result,"Black")
                        exit_limit = 1
                        continue
                    else:
                        if( all(df[0]%2==0) ):
                            continuity = True
                            while (continuity):
                                continuity = continuity_check(continuity,driver,result,"Odd")
                            exit_limit = 1
                            continue
                        elif( all(df[0]%2!=0) ):
                            continuity = True
                            while (continuity):
                                continuity = continuity_check(continuity,driver,result,"Even")
                            exit_limit = 1
                            continue  


            time.sleep(1)
            end_time = datetime.now()

            cont_playing = driver.find_elements_by_tag_name("button")
            for cont_playing_idx in cont_playing:
                if(cont_playing_idx.text == "Continue playing"):
                    cont_playing_idx.click()

            if((end_time - start_time) > timedelta(minutes = 18) ):
                url1 = "https://games.mansioncasino.com/live/desktop/bundles/21.12.5.24/?gametype=rol&connection=desktop&physicalnetworkId=-1&protocol=Live2&preferredSeat=undefined&preferedmode=real&mode=real&sessionTimer=null&launcher_time="
                url2 = str(int(time.time()))
                url3 = "&redirect_time=1645551083374&launch_alias=direct_launch_1642&backUrl=https%3A%2F%2Fgames.mansioncasino.com%2Flive%2Fdesktop%2Frol%2F%3Fgametype%3Drol%26connection%3Ddesktop%26tableId%3D1642%26physicalTableId%3D-1%26networkId%3D-1%26protocol%3DLive2%26preferredSeat%3Dundefined%26preferedmode%3Dreal%26mode%3Dreal%26sessionTimer%3Dnull%26"
                url = url1+url2+url3
                driver = traverse_to_roulette_1(url,driver)
                time.sleep(20)
                if driver:
                    driver = stats_page(driver)

                time.sleep(2)

                if driver:
                    statistics = stats_info(driver)

                start_time = datetime.now()
            
        exit_limit = 0
        
        
        strike_limit = strike
    
        print ("\n ----------RUNNING STRIKE CODE-------- \n")
        
        while (strike_limit != 0):
            
            if statistics:
                arr = statistics.find_elements_by_tag_name('div')
            result = []

            for i in range(0,last_num*4,4):
                temp = []
                try:
                    arr[i].get_attribute("innerText")
                    temp.append(int(arr[i].get_attribute("innerText")))
                    colour = arr[i].value_of_css_property('color')

                    temp.append(colour)
                    result.append(temp)
                except:
                    pass

            print(result)

            df = pd.DataFrame(result)

            if( len(df)==last_num and 0 not in df[0].tolist() ):

                if( all(df[0][:]>18) ):
                    bet_creator(driver, limit , "1-18",total_bet,para)
                    bet_check(driver,result,"1-18",limit-1,para)
                    strike_limit = strike_limit - 1
                    continue
                elif( all(df[0][:]<19) ):
                    bet_creator(driver, limit , "19-36",total_bet,para)
                    bet_check(driver,result,"19-36",limit-1,para)
                    strike_limit = strike_limit - 1
                    continue
                else:
                    if( all(df[1][:]==black) ):
                        bet_creator(driver, limit , "Red",total_bet,para)
                        bet_check(driver,result,"Red",limit-1,para)
                        strike_limit = strike_limit - 1
                        continue
                    elif( all(df[1][:]==red) ):
                        bet_creator(driver, limit , "Black",total_bet,para)
                        bet_check(driver,result,"Black",limit-1,para)
                        strike_limit = strike_limit - 1
                        continue
                    else:
                        if( all(df[0]%2==0) ):
                            bet_creator(driver, limit , "Odd",total_bet,para)
                            bet_check(driver,result,"Odd",limit-1,para)
                            strike_limit = strike_limit - 1
                            continue
                        elif( all(df[0]%2!=0) ):
                            bet_creator(driver, limit , "Even",total_bet,para)                    
                            bet_check(driver,result,"Even",limit-1,para)
                            strike_limit = strike_limit - 1
                            continue  


            time.sleep(1)
            end_time = datetime.now()

            cont_playing = driver.find_elements_by_tag_name("button")
            for cont_playing_idx in cont_playing:
                if(cont_playing_idx.text == "Continue playing"):
                    cont_playing_idx.click()

            if((end_time - start_time) > timedelta(minutes = 18) ):
                url1 = "https://games.mansioncasino.com/live/desktop/bundles/21.12.5.24/?gametype=rol&connection=desktop&physicalnetworkId=-1&protocol=Live2&preferredSeat=undefined&preferedmode=real&mode=real&sessionTimer=null&launcher_time="
                url2 = str(int(time.time()))
                url3 = "&redirect_time=1645551083374&launch_alias=direct_launch_1642&backUrl=https%3A%2F%2Fgames.mansioncasino.com%2Flive%2Fdesktop%2Frol%2F%3Fgametype%3Drol%26connection%3Ddesktop%26tableId%3D1642%26physicalTableId%3D-1%26networkId%3D-1%26protocol%3DLive2%26preferredSeat%3Dundefined%26preferedmode%3Dreal%26mode%3Dreal%26sessionTimer%3Dnull%26"
                url = url1+url2+url3
                driver = traverse_to_roulette_1(url,driver)
                time.sleep(20)
                if driver:
                    driver = stats_page(driver)

                time.sleep(2)

                if driver:
                    statistics = stats_info(driver)

                start_time = datetime.now()
                
       
    
        
    