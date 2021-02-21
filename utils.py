import datetime


def login(email, password, driver):
    # email
    e = driver.find_element_by_id("email")
    e.send_keys(email)

    # password
    p = driver.find_element_by_id("pword")
    p.send_keys(password)
    
    l = driver.find_element_by_id("loginBtnId")
    driver.execute_script("arguments[0].scrollIntoView();", l)
    l.click()


def get_new_date(old_date):
    year = datetime.datetime.now().year

    old_starting_date = old_date.split('-')[0]
    old_starting_month = old_starting_date.split()[0]
    old_starting_month = datetime.datetime.strptime(old_starting_month, "%B").month
    old_starting_day = int(old_starting_date.split()[1])


    old_start_dt = datetime.datetime(year, old_starting_month, old_starting_day)

    new_start_dt = old_start_dt + datetime.timedelta(days=7)
    new_end_dt = new_start_dt + datetime.timedelta(days=5)

    # construct output

    start_date = new_start_dt.day
    end_date = new_end_dt.day

    if new_start_dt.month == new_end_dt.month:
        # February 10-17 
        month_name = new_start_dt.strftime("%B")

        output = '{} {}-{}'.format(month_name, start_date, end_date)
    else:
        # January 27-February 3
        start_month_name = new_start_dt.strftime("%B")
        end_month_name = new_end_dt.strftime("%B")

        output='{} {}-{} {}'.format(start_month_name, start_date, end_month_name, end_date)

    return output

def exception_handler(starting_message, error_message):
    def decorator(func):
        def inner_function(*args, **kwargs):
            try:
                print(starting_message)
                func(*args, **kwargs)
            except TypeError:
                print(error_message)
        return inner_function
    return decorator

