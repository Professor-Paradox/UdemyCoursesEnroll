from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import date, timedelta

# chrome options gives us options to pass arguments to chrome browser,these commands can be accessed from terminal also
options = webdriver.ChromeOptions()

# loads the user profile in this location,used to run in a desired environment
options.add_argument("user-data-dir=/home/t/.config/google-chrome/Selenium/")

# assigning the chrome options to the webdriver chrome instance
driver = webdriver.Chrome(executable_path="./chromedriver", options=options)

# gives yesterdays date in desired format
yesterday = (date.today() - timedelta(days=1)).strftime("%B %d, %Y")

courses = []

# searches for course link based on date,if course has yesterday's time stamp takes the link
def get_course_websites():
    """
    get_course_websites gets all the links of course coupon websites located in a page

    Returns:
        (list): list of course coupon websites
    """
    courses_list = []
    # sleep is used to reduce number of requests,if multiple requests are passed the server blocks the ip
    time.sleep(1)

    # takes all the class blocks with needed data
    course_block = driver.find_elements_by_class_name("box")
    for block in course_block:
        # fetching the date course was posted on
        course_date = block.find_element_by_class_name("posted-date").text
        # returns the block containing course website link
        course_data = block.find_element_by_class_name("title")
        if course_date == yesterday:
            # if date matches,getting link of course website
            link = course_data.find_element_by_tag_name("a").get_attribute("href")
            # appending links to a list
            courses_list.append(link)
    return courses_list


def get_udemy_link():
    """
    get_udemy_links gets the udemy coupon link present in a website
    Returns:
        (string): udemy coupon link
    """
    time.sleep(1)
    # gets link assigned to a button
    udemy_link = driver.find_element_by_css_selector("a.maxbutton-1").get_attribute(
        "href"
    )
    return udemy_link


def enroll_free_course(course_data_box):
    # clicks on enroll now button on first page
    course_data_box.find_element_by_class_name("buy-box__element--buy-button").click()

    # waits for enroll button and clicks on it on second page
    time.sleep(3)
    enroll_now_buttons = driver.find_elements_by_css_selector(
        "button.ellipsis.btn.btn-lg.btn-primary.btn-block"
    )

    for i in enroll_now_buttons:
        if i.is_displayed():
            i.click()
            time.sleep(3)

def enrolling_to_a_course():
    """
    enrolling_to_a_course enrolls to course present in the link
    if course is free will enroll,
    if course is paid will skip,
    if already enrolled moves on.
    """

    # checks if course is already enrolled or not
    # block gets executed when the link points to a free course
    try:
        time.sleep(1)
        driver.find_element_by_css_selector(
            "button.udlite-btn.udlite-btn-small.udlite-btn-primary.udlite-heading-sm.udlite-btn-experiment-red.styles--btn--express-checkout--28jN4"
        ).click()
    except NoSuchElementException:
        # if this is not found displays following
        print("not a free course/ already enrolled")

    # checks if course is paid or discounted(free)
    try:
        time.sleep(1)
        # gets the course enroll box data
        course_data_box = driver.find_element_by_class_name("buy-box")
        # getting the price details of course
        course_price = course_data_box.find_element_by_class_name(
            "udlite-clp-discount-price"
        )
        time.sleep(1)
        # enrolls only if free
        if "Free" in course_price.text:
            enroll_free_course(course_data_box)
            # print("discounted course enrolled successfully")
    except NoSuchElementException:
        print("not a discounted course/ already enrolled\n")
        return


# getting all the links from 1 to 10 pages
# initiating website with starting page
driver.get("https://tutsnode.net/category/udemy")
courses.extend(get_course_websites())

# gets websites with udemy courses
# continuing to get website links in 10 pages
for i in range(2, 11):
    driver.get(f"https://tutsnode.net/category/udemy/page/{i}")
    print(f"got links from page {i}")
    time.sleep(1)
    courses.extend(get_course_websites())

# print(courses)
# gets udemy course links
for i in courses:
    time.sleep(1)
    driver.get(i)
    link=get_udemy_link()
    print(f"fetched:    {link}")
    driver.get(link)
    enrolling_to_a_course()


driver.quit()
