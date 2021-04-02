# Upnext BETA by hbk Pancakes
# Upnext is a YouTube playlist generator, which will remove old
# videos and add new videos to a specified playlist, based on 
# channel subscription choices that you specify.

# to do:
# add error names to try/except blocks where missing
# more error handling
# additional features (remove videos from playlist only?)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
import time
import re
from decimal import Decimal
from functools import reduce
import os
import json
# removed to lessen dependencies for sript to work, feel free to enable, if you enable, uncomment out lines 31 and 367 
# from win10toast import ToastNotifier

# set notification variable
# toaster = ToastNotifier()

# create clear function to keep cmd clean while running program
def clear(): 
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

while True:
    clear()
    # quick check for current browser setting for main menu
    try:
        with open(r'configs/browser_config.json', 'r') as f:
            browser_config = json.load(f)
    except:
        pass
    try:
        browser_check = browser_config['browser_choice']
        if browser_check == '1':
            default_browser = 'Firefox'
        if browser_check == '2':
            default_browser = 'Chrome'
    except:
        default_browser = 'Not Set'

    # main menu
    print('\nUpnext - YouTube Playlist Manager\n')
    print('Main Menu')
    try:
        print('1. Run\n2. Change Default Browser (Current: ' + default_browser + ') \n3. Subscription Settings\n4. Playlist Settings\n\n0. Exit\n')
    except NameError:
        print('1. Run\n2. Change Default Browser (Current: Not set)\n3. Subscription Settings\n4. Playlist Settings\n\n0. Exit\n')
    # handles user input
    while True:
        menu_choice = input('Selection: ')
        if menu_choice in ('1', '2', '3', '4', '0'):
            break
        print('\nInvalid input. Please enter a valid menu option\n')
    # main program loop
    if menu_choice == '1':
        # attemps to load default browser config if available
        try:
            with open(r'configs/browser_config.json', 'r') as f:
                browser_config = json.load(f)
        # if browser config file does not exist, create 
        except:
            print('\nBrowser settings not stored. Either first time use or config file deleted. Starting to capture browser settings...\n')
        try:
            browser_check = browser_config['browser_choice']
        except:
            print('Choose Browser:\n1. Firefox\n2. Chrome\n\n0. Exit\n')
            # handles user input
            while True:
                browser_check = input('Selection: ')
                if browser_check in ('1', '2', '0'):
                    break
                print('\nInvalid input. Please enter a valid menu option\n')
        
        # if user selects Firefox
        if browser_check == '1':
            # driver settings for firefox browser
            try:
                with open(r'configs/ff_config.json', 'r') as f:
                    ff_config = json.load(f)
            except:
                print('\nFirefox settings not stored. Either first time use or config file deleted. Starting to capture Firefox settings.')
                print('Type "/exit" to exit setup if needed.')
            try:
                ff_driver = ff_config['ff_driver']
            except:
                found = False
                ff_driver = None
                while not found:
                    ff_driver = input('\nDriver location: ')
                    if ff_driver == '/exit':
                        exit()
                    elif not os.path.isfile(ff_driver):
                        print('\nThis is not a valid file. Please try again.')
                    else:
                        found = True
            # profile settings for firefox browser
            try:
                ff_profile = ff_config['ff_profile']
            except:
                found = False
                ff_profile = None
                while not found:
                    ff_profile = input('\nBrowser profile directory: ')
                    if ff_profile == '/exit':
                        exit()
                    elif not os.path.isdir(ff_profile):
                        print('\nThis not a valid directory. Please try again.')
                    else:
                        found = True      

        # if user selects Chrome    
        if browser_check == '2':
            # driver settings for chrome
            try:
                with open(r'configs/gc_config.json', 'r') as f:
                    gc_config = json.load(f)
            except:
                print('\nChrome settings not stored. Either first time use or config file deleted. Starting to capture Chrome settings.')
                print('Type "/exit" to exit setup if needed.')
            try:
                gc_driver = gc_config['gc_driver']
            except:
                found = False
                gc_driver = None
                while not found:
                    gc_driver = input('\nDriver location: ')
                    if gc_driver == '/exit':
                        exit()
                    elif not os.path.isfile(gc_driver):
                        print('\nThis is not a valid file. Please try again.')
                    else:
                        found = True
            # profile settings for chrome
            try:
                gc_profile = gc_config['gc_profile']
            except:
                found = False
                gc_profile = None
                while not found:
                    gc_profile = input('\nBrowser profile directory: ')
                    if gc_profile == '/exit':
                        exit()
                    elif not os.path.isdir(gc_profile):
                        print('\nThis not a valid directory. Please try again.')
                    else:
                        found = True 

        if browser_check == '0':
            break

        # attemps to load subs settings
        try:
            with open(r'configs/sub_config.json', 'r') as f:
                sub_config = json.load(f)
        except:
            print('\nSubscription settings not stored. Either first time use or config file deleted. Starting to capture Subscription settings...\n')
        # check if subs have been declared
        try:
            subs_to_keep = sub_config['subs']
        # if subs havent been declared, start capture
        except:
            subs_to_keep = []
            print('Enter the EXACT channel names for videos you want to add to the playlist. When finished, type "/done".')
            while True:
                add_to_list = input('Channel name: ')
                if add_to_list == '/done':
                    break
                elif add_to_list == '/exit':
                    exit()
                else:
                    subs_to_keep.append(add_to_list)

        # attempts to load playlist settings
        try:
            with open(r'configs/playlist_config.json', 'r') as f:
                playlist_config = json.load(f)
        except:
            print('\nPlaylist settings not stored. Either first time use or config file deleted. Starting to capture Playlist settings...')
        # check if playlist link has been declared
        try:
            playlist_link = playlist_config['playlist']
        # if subs havent been declared, start capture
        except:
            print('\nEnter in the direct link to the playlist you would like to add the videos to.')
            print('Please note: the link MUST start with "https://" (note the "s").')
            while True:
                playlist_link = input('\nPlaylist link: ')
                if "https://" in playlist_link:
                    break
                elif playlist_link == '/exit':
                    exit()
                else:
                    print('\nInvalid URL. Please try again')

        if browser_check == '1':
            # firefox driver settings
            options = webdriver.FirefoxOptions()
            options.headless = True
            try:
                browser = webdriver.Firefox(ff_profile, options=options, executable_path=ff_driver)
            # handles cases where driver location may have changed
            except WebDriverException:
                print('\nLooks like your driver location for the Firefox browser in incorrect, has the file or folder containing it been moved?')
                found = False
                ff_driver = None
                while not found:
                    ff_driver = input('\nDriver location: ')
                    if ff_driver == '/exit':
                        exit()
                    elif not os.path.isfile(ff_driver):
                        print('\nThis is not a valid file. Please try again.')
                    else:
                        found = True
                browser = webdriver.Firefox(ff_profile, options=options, executable_path=ff_driver)
            except FileNotFoundError:
                print('\nLooks like your browser path has changed. Did you delete a browser profile?')
                found = False
                ff_profile = None
                while not found:
                    ff_profile = input('\nBrowser profile directory: ')
                    if ff_profile == '/exit':
                        exit()
                    elif not os.path.isdir(ff_profile):
                        print('\nThis not a valid directory. Please try again.')
                    else:
                        found = True      
                browser = webdriver.Firefox(ff_profile, options=options, executable_path=ff_driver)

        if browser_check == '2':
            # chrome driver settings
            options = webdriver.ChromeOptions()
            options.add_argument("user-data-dir=" + gc_profile)
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            try:
                browser = webdriver.Chrome(options=options, executable_path=gc_driver)
            # handles cases where driver location may have changed
            except WebDriverException:
                print('\nLooks like your driver location for the Google Chrome browser in incorrect, has the file or folder containing it been moved?')
                found = False
                gc_driver = None
                while not found:
                    gc_driver = input('\nDriver location: ')
                    if gc_driver == '/exit':
                        exit()
                    elif not os.path.isfile(gc_driver):
                        print('\nThis is not a valid file. Please try again.')
                    else:
                        found = True
                browser = webdriver.Chrome(options=options, executable_path=gc_driver)

        #########################
        ### main program loop ###
        #########################

        # access playlist
        browser.get(playlist_link)

        print('\nRemoving previous videos from playlist...')

        # finds playlist name
        playlist_name_element = browser.find_element_by_xpath('//*[@id="text-displayed"]')
        playlist_name = playlist_name_element.text
        
        # clear videos from playlist
        videos_to_remove = browser.find_elements_by_xpath('//*[@id="video-title"]')

        for videos in videos_to_remove: 
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-playlist-video-renderer.style-scope:nth-child(1) > div:nth-child(3) > ytd-menu-renderer:nth-child(1)'))).click()
            time.sleep(1)
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-menu-service-item-renderer.style-scope:nth-child(4) > tp-yt-paper-item:nth-child(1)'))).click()
            time.sleep(1)

        # access subscription page
        print('Accessing YouTube subscription page...')
        time.sleep(3)
        browser.get("https://www.youtube.com/feed/subscriptions")

        # identifys video elements
        time.sleep(3)
        video_elements = browser.find_elements_by_class_name('style-scope ytd-grid-video-renderer')

        # adds selected channel subscriptions to playlist
        time.sleep(3)
        print('Adding videos to playlist...')
        for element in video_elements:
            # indentifys channel names
            channel_names = element.find_elements_by_class_name('style-scope ytd-channel-name')
            for name in channel_names:    
                # matches channel names with sub list
                if name.text in subs_to_keep:
                    # determines if video has been watched yet
                    try:                      
                        watched_flag = element.find_element_by_class_name('style-scope ytd-thumbnail-overlay-resume-playback-renderer')
                    # adds videos that haven't been watched to playlist
                    except NoSuchElementException:
                        # finds video playlist options
                        WebDriverWait(element, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'style-scope ytd-menu-renderer'))).click()
                        time.sleep(2)
                        # add to playlist click
                        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-menu-service-item-renderer.style-scope:nth-child(3) > tp-yt-paper-item:nth-child(1)'))).click()
                        time.sleep(1)                
                        # identify correct playlist
                        playlist_name_path = '//*[contains(text(), "'+ playlist_name +'")]'
                        # adds all elements that have playlist name text to list
                        correct_playlist_check = browser.find_elements_by_xpath(playlist_name_path)
                        # try to click each item in list, if error, move to the next
                        for check in correct_playlist_check:
                            time.sleep(1)
                            try:
                                check.click()
                            except (ElementClickInterceptedException, ElementNotInteractableException) as error:
                                pass
                        time.sleep(1)
                        # close out of menu options
                        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'yt-icon.ytd-add-to-playlist-renderer'))).click()
                        time.sleep(1)

        # writes user settings to config file if config was created outside of settings menu

        # default browser setting
        browser_config = {'browser_choice': browser_check}
        with open(r'configs/browser_config.json', 'w') as f:
            json.dump(browser_config, f)

        if browser_check == '1':
            ff_config = {'browser_choice': browser_check, 'ff_driver': ff_driver, 'ff_profile': ff_profile}
            with open(r'configs/ff_config.json', 'w') as f:
                json.dump(ff_config, f)
        if browser_check == '2':
            gc_config = {'browser_choice': browser_check, 'gc_driver': gc_driver, 'gc_profile': gc_profile}
            with open(r'configs/gc_config.json', 'w') as f:
                json.dump(gc_config, f)

        # user settings
        sub_config = {'subs': subs_to_keep}
        with open(r'configs/sub_config.json', 'w') as f:
            json.dump(sub_config, f)

        playlist_config = {'playlist': playlist_link}
        with open(r'configs/playlist_config.json', 'w') as f:
            json.dump(playlist_config, f)

        # quits
        print('Complete!')
        time.sleep(3)
        browser.quit()
        # windows 10 notification, enable if you uncomment the win10toast import
        # also will want to add program icon to toast notification
        # toaster.show_toast("Playlist updated!", "Upnext has successfully added videos to your playlist")

    #####################
    ### settings menu ###
    #####################

    # if user selects 2, start browser edit settings
    if menu_choice == '2':
        clear()
    # displays menu
        print('\nBrowser Settings\n')
        print('Browser List:\n1. Firefox\n2. Chrome\n\n0. Exit\n')
        
        # handles user input
        while True:
            browser_check = input('Selection: ')
            if browser_check in ('1', '2', '0'):
                break
            else:
                print('\nInvalid input. Please enter a valid menu option\n')

        # attemps to load firefox browser
        if browser_check == '1':
            try:
                with open(r'configs/ff_config.json', 'r') as f:
                    ff_config = json.load(f)
            # if firefox browser setting has not been stored
            except:
                print('\nBrowser settings not stored. Either first time use or config file deleted. Starting to capture user settings...')
            # load or create firefox driver setting
            try:
                ff_driver = ff_config['ff_driver']
            except:
                found = False
                ff_driver = None
                while not found:
                    ff_driver = input('\nDriver location: ')
                    if ff_driver == '/exit':
                        exit()
                    elif not os.path.isfile(ff_driver):
                        print('\nThis is not a valid file. Please try again.')
                    else:
                        found = True
            # load or create firefox profile
            try:
                ff_profile = ff_config['ff_profile']
            except:
                found = False
                ff_profile = None
                while not found:
                    ff_profile = input('\nBrowser profile directory: ')
                    if ff_profile == '/exit':
                        exit()
                    elif not os.path.isdir(ff_profile):
                        print('\nThis not a valid directory. Please try again.')
                    else:
                        found = True
            # save firefox browser settings 
            ff_config = {'ff_driver': ff_driver, 'ff_profile': ff_profile}
            with open(r'configs/ff_config.json', 'w') as f:
                json.dump(ff_config, f)
            # save as default browser choice
            browser_config = {'browser_choice': browser_check}
            with open(r'configs/browser_config.json', 'w') as f:
                json.dump(browser_config, f)

            print('Browser settings updated.\n')

            clear()
        
        # attemps to load chrome browser
        if browser_check == '2':
            try:
                with open(r'configs/gc_config.json', 'r') as f:
                    gc_config = json.load(f)
            # if chrome browser setting has not been stored
            except:
                print('\nBrowser settings not stored. Either first time use or config file deleted. Starting to capture user settings...')
            # load or create chrome driver setting
            try:
                gc_driver = gc_config['gc_driver']
            except:
                found = False
                gc_driver = None
                while not found:
                    gc_driver = input('\nDriver location: ')
                    if gc_driver == '/exit':
                        exit()
                    elif not os.path.isfile(gc_driver):
                        print('\nThis is not a valid file. Please try again.')
                    else:
                        found = True
            # load or create chrome profile setting
            try:
                gc_profile = gc_config['gc_profile']
            except:
                found = False
                gc_profile = None
                while not found:
                    gc_profile = input('\nBrowser profile directory: ')
                    if gc_profile == '/exit':
                        exit()
                    elif not os.path.isdir(gc_profile):
                        print('\nThis not a valid directory. Please try again.')
                    else:
                        found = True 
            # save chrome browser settings
            gc_config = {'gc_driver': gc_driver, 'gc_profile': gc_profile}
            with open(r'configs/gc_config.json', 'w') as f:
                json.dump(gc_config, f)
            # save as default browser choice
            browser_config = {'browser_choice': browser_check}
            with open(r'configs/browser_config.json', 'w') as f:
                json.dump(browser_config, f)

            print('Browser settings updated.\n')

            clear()

    # exit to main menu
    if browser_check == '0':
        pass
        clear()

    # if user selects 3, start sub edit settings
    if menu_choice == '3':
        clear()
        # attempts to load sub settings
        try:
            with open(r'configs/sub_config.json', 'r') as f:
                sub_config = json.load(f)
        # if no sub settings have been created
        except:
            print('\nA list of Channel Subscriptions has not been created yet.\n')
            subs_to_keep = []
            print('Enter the EXACT channel names for videos you want to add to the playlist. When finished, type "/done".\n')
            # starts sub addition loop
            while True:
                add_to_list = input('Channel name: ')
                if add_to_list == '/done':
                    break
                else:
                    subs_to_keep.append(add_to_list)
                sub_config = {'subs': subs_to_keep}
                # saves sub settings
                with open(r'configs/sub_config.json', 'w') as f:
                    json.dump(sub_config, f)
        
        # displays settings title
        print('\nYouTube Subscription Settings\n')
        
        # prints current sub list
        print('Current Subscription Choices: ')
        try:
            subs_to_keep = sub_config['subs']
            for sub in subs_to_keep:
                print(sub)
        except UnboundLocalError:
            print("You havent added any subs.")

        # displays menu
        print('\n1. Add Subs\n2. Remove Subs\n\n0. Exit\n')
        
        # handles user input
        while True:
            sub_settings_choice = input('Selection: ')
            if sub_settings_choice in ('1', '2', '0'):
                break
            else:
                print('\nInvalid input. Please enter a valid menu option\n')

        # add new sub option
        if sub_settings_choice == '1':
            try:
                subs_to_keep = sub_config['subs']
            except UnboundLocalError:
                subs_to_keep = []
            # starts sub addition loop
            while True:
                add_to_list = input('Channel name: ')
                if add_to_list == '/done':
                    break
                else:
                    subs_to_keep.append(add_to_list)
            # saves list with new sub adds
            sub_config = {'subs': subs_to_keep}
            with open(r'configs/sub_config.json', 'w') as f:
                json.dump(sub_config, f)

            print('Sub list successfully updated.\n')
            clear()

        # remove sub option
        if sub_settings_choice == '2':
            try:
                subs_to_keep = sub_config['subs']   
                # starts sub removal loop
                while True:
                    remove_from_list = input('Channel name: ')
                    if remove_from_list == '/done':
                        break
                    else:
                        try:
                            subs_to_keep.remove(remove_from_list)
                        except ValueError:
                            print('\nThis name is not currently stored in your Sub list. Unable to remove!\n')
                # saves list with removed subs
                    with open(r'configs/sub_config.json', 'w') as f:
                        json.dump(sub_config, f)
                
                print('\nSub list successfully updated.')
                clear()
            except (UnboundLocalError):
                print('\nThere are no Subs currently configured, so there is nothing to remove.')
                clear()

        # exit to main menu
        if sub_settings_choice == '0':
            pass
            clear()

    # if user selects 4, start playlist edit settings
    if menu_choice == '4':
        clear()
        # attemps to load playlist settings
        try:
            with open(r'configs/playlist_config.json', 'r') as f:
                playlist_config = json.load(f)
        # if no playlist settings are stored
        except:
            print('\nA playlist link has not been saved yet.')
            print('\nEnter in the direct link to the playlist you would like to add the videos to.')
            print('Please note: the link MUST start with "https://" (note the "s").')
            print('Type "/exit" to end Playlist setup if needed\n')
            while True:
                playlist_link = input('Playlist link: ')
                if "https://" in playlist_link:
                    break
                elif playlist_link == '/exit':
                    exit()
                else:
                    print('\nInvalid URL. Please try again\n')
            playlist_config = {'playlist': playlist_link}
            # saves playlist setting
            with open(r'configs/playlist_config.json', 'w') as f:
                json.dump(playlist_config, f)

        # displays setting title + current playlist link
        print('\nYouTube Playlist Settings\n')
        print('Current Playlist Link: ' + playlist_config['playlist'] + '\n')

        # displays menu
        print('1. Change Playlist Link\n\n0. Exit')
        playlist_settings_choice = input('\nSelection: ')

        # change playlist link
        if playlist_settings_choice == '1':
            print('\nEnter in the direct link to the playlist you would like to add the videos to.')
            print('Please note: the link MUST start with "https://" (note the "s").')
            while True:
                new_playlist = input('\nEnter new playlist link: ')
                if "https://" in new_playlist:
                    break
                elif new_playlist == '/exit':
                    exit()
                else:
                    print('\nInvalid URL. Please try again')

            playlist_config['playlist'] = new_playlist
            # saves new playlist setting
            with open(r'configs/playlist_config.json', 'w') as f:
                json.dump(playlist_config, f)
            
            print('\nPlaylist Link successfully updated.\n')
            clear()
        
        # exits to main menu
        if playlist_settings_choice == '0':
            pass
            clear()

    # exits program
    if menu_choice == '0':
        exit()
