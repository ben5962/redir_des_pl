from selenium import webdriver
import traceback

# pour recuperer les variables login password
import configparser
Config = configparser.ConfigParser()
Config.read("config.ini")
login = Config.get('source','login')
password = Config.get('source', 'password')
redir = Config.get('source', 'recherche_a_redirriger')
url = Config.get('source', 'url')
dest = Config.get('destination','destination')

# pour e timeout
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# pour le clic droit
from selenium.webdriver import ActionChains

# pour la fleche ver le bas
from selenium.webdriver.common.keys import Keys

import time
class Exportateur_Mails(Object):
    def __init__(self):
        

def bricolage_firefox():
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
##        premier bricolage pour les certificats non valides merche pas
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True

##        deuxieme bricolage pour les certificats non valides
    caps = DesiredCapabilities.FIREFOX.copy()
    caps['acceptInsecureCerts'] = True
    binary = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
    browser = webdriver.Firefox(firefox_binary=binary, capabilities=caps, firefox_profile=profile)
    return browser


def envoyer_vers_champ(brouteur,champ,chaine,valider=False):
    elem = brouteur.find_element_by_id(champ)
    elem.send_keys(chaine)
    if valider == True:
        elem.submit()

def cliquer_sur_css(brouteur,css):
    elem = brouteur.find_element_by_css_selector(css)

def cliquer_sur_id(brouteur,the_id):
    elem = brouteur.find_element_by_id(the_id)
    elem.click()
    return elem

def cliquer_sur_xpath(brouteur,xpath):
    elem = brouteur.find_element_by_xpath(xpath)
    time.sleep(2)
    #elem.send_keys(Keys.NULL) #focus
    elem.click()
    return elem



def attendre_maj_page(brouteur,id_attendu):
    timeout = 15
    try:
        element_present = EC.presence_of_element_located((By.ID, id_attendu))
        WebDriverWait(brouteur, timeout).until(element_present)
    except TimeoutException:
       print("Timed out waiting for page to load")
   
def xpath_existe(brouteur,xpath):
    ele = brouteur.find_elements_by_xpath(xpath)
    return len(ele) > 0

def compter_nbre_noeuds(brouteur,xpath):
    ele = brouteur.find_elements_by_xpath(xpath)
    return len(ele)

#####################
# actions specifiques
####################
def charger_mails_planning(brouteur,xpath_de_chargement):
    try:
        cliquer_sur_xpath(brouteur,xpath_de_chargement)
        verite = True
        return verite
    except:
        traceback.print_stack()
        print("pas trouvé planning domo")
        verite = False
        return verite

def focus_sur_premier_mail(brouteur,xpath_premier_mail):
    
    try:
        elem = cliquer_sur_xpath(brouteur,xpath_premier_mail)
        return elem
    except:
        print("pas trouvé premier mail")

def decompte_mails(brouteur,xpath_tous_mails):
    return compter_nbre_noeuds(brouteur,xpath_tous_mails)

def focus_sur_enieme_mail(brouteur,xpath_premier_mail,position_souhaitee):
    ##    ch_xpath_avant_pos1 = xpath_premier_mail[0:xpath_premier_mail.find('1')]
    ##    ch_xpath_apres_pos1 = xpath_premier_mail[xpath_premier_mail.find('1') + 1:]
    ##    xpath_final = ch_xpath_avant_pos1 + str(position_souhaitee) + ch_xpath_apres_pos1
    ##    print(xpath_final)
    xpath_final = ''.join(["//ul[@id='zl__TV-main__rows']/li[",str(position_souhaitee),"]"])
    try:
        elem = cliquer_sur_xpath(brouteur,xpath_final)
        return elem
    except ValueError:
        print("pas trouve position : {}", position_souhaitee)

def rediriger_mail(browser,numero_mail):

    try:
        time.sleep(2)
        elem = focus_sur_enieme_mail(browser,"//ul[@id='zl__TV-main__rows']/li[1]",numero_mail)
        ##        time.sleep(2)
        ##        elemaction = cliquer_sur_xpath(browser,'//div[@id="zb__TV-main__ACTIONS_MENU"]')
        ##        time.sleep(1)
        ##        elemvalider = cliquer_sur_xpath(browser,"//div[@id='zmi__TV-main__REDIRECT']")
        ##        envoyer_vers_champ(browser,"RedirectDialog_to_control",dest)
        ##        okcliquer = cliquer_sur_xpath(browser,"//*[@id='RedirectDialog_button2']")
        ##        attendre_maj_page(browser,'zl__TV-main__rows')
        return True
    except:
        traceback.print_stack()
        return False

    
def getdecompte(browser):
    elem = focus_sur_premier_mail(browser,"//ul[@id='zl__TV-main__rows']/li[1]")
    # hypothese chargement par paquet de 100:
    attendre_maj_page(browser,'zl__TV-main__rows')
    time.sleep(2)
    decompte = decompte_mails(browser, "//ul[@id='zl__TV-main__rows']/li")
    print("premier decompte: {}".format(decompte))
    # magic: un temps d'attente.
    attendre_maj_page(browser,'zl__TV-main__rows')
    time.sleep(3)
    elem = focus_sur_enieme_mail(browser,"//ul[@id='zl__TV-main__rows']/li[1]",decompte)
    # nouvelle valeur de decompte
    attendre_maj_page(browser,'zl__TV-main__rows')
    decompte = decompte_mails(browser, "//ul[@id='zl__TV-main__rows']/li")
    print("deuxieme decompte: {}".format(decompte))
    return decompte
    
def section_commentee():
    elem = focus_sur_enieme_mail(browser,"//ul[@id='zl__TV-main__rows']/li[1]",1)
    elemaction = cliquer_sur_xpath(browser,'//div[@id="zb__TV-main__ACTIONS_MENU"]')
    elemvalider = cliquer_sur_xpath(browser,"//div[@id='zmi__TV-main__REDIRECT']")
    envoyer_vers_champ(browser,"RedirectDialog_to_control",dest)
    #okcliquer = cliquer_sur_xpath(browser,"//*[@id='OK_DWT93']")
    #le bouton ok est devenu 'OK_DWT112' on va pas jouer au chat et à la souris.
    # je prends l id en dessous:
    okcliquer = cliquer_sur_xpath(browser,"//*[@id='RedirectDialog_button2']")

def descendre(browser,elem):
    actionChains = ActionChains(browser)
    ##    actionChains.context_click(elem)
    ##    actionChains.perform()
    ##    actionChains = ActionChains(browser)
    ##    actionChains.send_keys('Keys.LEFT')
    actionChains.send_keys('Keys.DOWN')
    ##    actionChains.send_keys('Keys.DOWN')
    ##    actionChains.send_keys('Keys.DOWN')
    ##    actionChains.send_keys('Keys.LEFT')
    ##    actionChains.send_keys('Keys.DOWN')
    ##    actionChains.send_keys('Keys.DOWN')
    ##    actionChains.send_keys('Keys.DOWN')
    ##    actionChains.send_keys('Keys.ENTER')
    actionChains.perform()
    

#################


def run(url=url,b='notfirefox'):
    if b == 'firefox':
        browser = bricolage_firefox()
    else:
        browser = webdriver.Chrome()
    browser.get(url)
    envoyer_vers_champ(browser,'username',login)
    envoyer_vers_champ(browser,'password', password,valider=True)
    ##    >>> mon_xpath3 = "//td[contains(.,'Recherches')]"
    ##    >>> eee = browser.find_element_by_xpath(mon_xpath3)
    ##    >>> eee.get_attribute('id')
    ##    'ztih__main_Mail__SEARCH_textCell'
    time.sleep(2)
    attendre_maj_page(browser,'zl__TV-main__rows')
    time.sleep(7)
    charger_mails_planning(browser,"//td[contains(.,'"+redir+"')]")
    #magic: laisser chat se charger...
    ##    time.sleep(3)
    ##    attendre_maj_page(browser,'zl__TV-main__rows')
    ##
    ##    decompte = getdecompte(browser)
    # essai redir
    ##    time.sleep(2)
    ##    elem = focus_sur_enieme_mail(browser,"//ul[@id='zl__TV-main__rows']/li[1]",1)
##    for i in range(1,decompte):
##        descendre(browser)
     
    
    if charger_mails_planning(browser,"//td[contains(.,'"+redir+"')]"):
        time.sleep(3)
        cpt = 1
        while(rediriger_mail(browser,cpt)):
            cpt = cpt + 1
        


    
    
    
    
    
    
    
    


    
    
        
    

    
    

if __name__ == '__main__':
    run()
