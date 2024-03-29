from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import datetime as dt
from utils import login as login_f, get_new_date


def login(EMAIL, PASS):
    
    login_f(EMAIL, PASS, driver)

def set_sort_order_desc():
    # settings btn
    settings_btn = wait.until(lambda driver: driver.find_elements(By.XPATH, "//a[@popover='Settings']"))[0]
    settings_btn.click()

    # DESC btn in dropdown
    sort_dd = driver.find_element(By.ID, 'sortDirectionId')
    sort_dd.location_once_scrolled_into_view
    sort_dd.click()
    desc_btn = sort_dd.find_elements(By.XPATH, "//*[contains(text(), 'DESC')]")[0]
    desc_btn.click()

    # close settings
    settings_btn.click()


def get_latest_lesson():
    
    rows = driver.find_elements(By.TAG_NAME, "tr")
    def is_private_lessons(row):
        return len(row.find_elements(By.XPATH, ".//*[ contains (text(), 'Private Lessons with Paula' ) ]")) > 0
    lessons = [row for row in rows if is_private_lessons(row)]
    latest_lesson = lessons[0] # first one because sorted in desc order
    # scroll into view
    latest_lesson.location_once_scrolled_into_view

    return latest_lesson


def click_duplicate_btn(latest_lesson):
    print("Clicking duplicate btn")

    # expand more actions dropdown
    more_actions_btn = latest_lesson.find_elements(By.XPATH, ".//a[@popover='More Actions']")[0]
    more_actions_btn.click()

    # click duplicate button
    duplicate_btn = latest_lesson.find_elements(By.XPATH, ".//a[@popover='Duplicate Sign Up']")[0]
    duplicate_btn.click()


def edit_title():
    print("Editing title")
    title = wait.until(lambda driver: driver.find_element(By.ID, "newtitle"))
    old_title = title.get_attribute("value")
    old_date = old_title.split("Paula")[-1].strip()
    new_date = get_new_date(old_date)
    title.clear()
    new_title = "Private Lessons with Paula " + new_date
    title.send_keys(new_title)
    return new_title


def create_copy():
    print("Creating copy")
    create_copy_btn = driver.find_elements(By.XPATH, ".//input[@value='Create Copy']")[0]
    create_copy_btn.location_once_scrolled_into_view
    create_copy_btn.click()


def go_to_unpublished_sign_up(sign_up_title, attempt = 1):

    attempt_text = ""
    if attempt > 1:
        attempt_text = f"(attempt {attempt})"
    print(f"Searching for unpublished sign up {attempt_text}")

    time.sleep(2)

    # search for target sign up
    search_bar = wait.until(lambda driver: driver.find_elements(By.XPATH, ".//input[@name='filter']"))[0]
    search_bar.send_keys(sign_up_title)


    # get first (newest) sign up
    try:
        target_sign_up = driver.find_elements(By.TAG_NAME, "tr")[0]
        edit_btn = target_sign_up.find_elements(By.XPATH, ".//a[@popover='Edit Sign Up']")[0]
        edit_btn.location_once_scrolled_into_view
        edit_btn.click()
    except:
        print(f'Could not find sign up "{sign_up_title}"')
        driver.refresh()
        go_to_unpublished_sign_up(sign_up_title, attempt = attempt + 1)

def edit_slots(day_of_week):
    print(f"Editing slot ({day_of_week})")

    # click edit multiple
    edit_mult = wait.until(EC.element_to_be_clickable((By.XPATH, ".//a[@uib-popover='Select multiple dates']")))
    edit_mult.location_once_scrolled_into_view
    edit_mult.find_element(By.XPATH, '..').click()
    
    # check day
    search_bar = driver.find_elements(By.XPATH, ".//input[@name='filter']")[0]
    search_bar.location_once_scrolled_into_view
    search_bar.clear()
    search_bar.send_keys(day_of_week)
    time.sleep(1) # wait for filter 
    driver.find_element(By.ID, "selectAllDates").click()

    # edit btn
    edit_btn = driver.find_elements(By.XPATH, '//button[@data-ng-click="{}"]'.format("w2.editMulti('date')"))[0]
    edit_btn.location_once_scrolled_into_view
    edit_btn.click()

    # check date checkbox
    check_date = wait.until(lambda driver:driver.find_element(By.XPATH, "//input[@name='ed_updateDate']"))
    check_date.find_element(By.XPATH, '..').click()

    # edit date
    date_field = driver.find_element(By.XPATH, "//input[@name='ed_dateToEdit']")
    date_field.click()
    old_date = date_field.get_attribute('value')
    new_date = datetime.strptime(old_date, "%m/%d/%Y") + dt.timedelta(days=7)
    date_field.clear()
    date_field.send_keys(new_date.strftime("%m/%d/%Y"))


    # save
    save_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    save_btn.location_once_scrolled_into_view
    save_btn.click()


def publish():
    publish_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[ contains (text(), 'Publish' ) ]")))
    publish_btn.location_once_scrolled_into_view
    publish_btn.click()
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[ contains (text(), 'Save & Proceed' ) ]")))
    save_btn.click()

    # second publish button
    publish_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-ng-click="{}"]'.format("w4.clickPublish()"))))
    publish_btn.location_once_scrolled_into_view
    publish_btn.click()


def get_url():
    urlDOM = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-copy="signupURL"]')))
    urlDOM.location_once_scrolled_into_view
    return urlDOM.text
    


##### DRIVER CODE ######

# globals initialization for import
chrome_options = Options()  
chrome_options.add_argument("--headless")
userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.20 Safari/537.36"
chrome_options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
wait = ui.WebDriverWait(driver, 10) # timeout after 10 seconds



def run(email, password, bar, st, latest_iteration):
    
    driver.get("https://www.signupgenius.com/register")
    latest_iteration.text(driver.page_source)
    i = 0

    # steps
    latest_iteration.text("Logging in")
    login(email, password)
    i += .09
    bar.progress(i)

    latest_iteration.text("Changing sort to desc")
    set_sort_order_desc()
    i += .09
    bar.progress(i)

    latest_iteration.text("Getting latest lesson")
    ll = get_latest_lesson()
    i += .09
    bar.progress(i)

    latest_iteration.text("Duplicating latest lesson")
    click_duplicate_btn(ll)
    i += .09
    bar.progress(i)

    latest_iteration.text("Calculating new sign up title")
    sign_up_title = edit_title()
    i += .09
    bar.progress(i)

    latest_iteration.text("Creating copy")
    create_copy()
    i += .09
    bar.progress(i)
    
    driver.get("https://www.signupgenius.com/myaccount/")
    driver.refresh()

    latest_iteration.text("Changing sort to desc")
    set_sort_order_desc()
    i += .09
    bar.progress(i)

    latest_iteration.text("Going to unpublished sign up")
    go_to_unpublished_sign_up(sign_up_title, attempt = 1)
    i += .09
    bar.progress(i)
    
    slot_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[ contains (text(), 'Slots' ) ]")))
    slot_btn.click()

    dow = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for day in dow:
        latest_iteration.text(f"Editing day ({day})")
        edit_slots(day)
        i += .015
        bar.progress(i)

    latest_iteration.text("Publishing")
    publish()
    i += .09
    bar.progress(i)

    latest_iteration.text("Getting sign up url")
    sign_up_url = get_url()
    i += .09
    bar.progress(i)

    latest_iteration.text("Done!")

    st.balloons()
    st.success(f'----- {sign_up_title} created! ----')

    return sign_up_url
