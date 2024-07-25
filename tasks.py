from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    # browser.configure(slowmo=1000)
    browser.configure(slowmo=1000)
    open_robot_order_website()
    close_annoying_modal()
    orders = get_orders()

    for order in orders:
        head = order["Head"]
        body = order["Body"]
        leags = order["Legs"]
        address = order["Address"]

        fill_the_form_and_submit(
            head,
            body,
            leags,
            address,
        )


def open_robot_order_website():
    """Open robot order website"""
    url_website = "https://robotsparebinindustries.com/#/robot-order"
    browser.goto(url=url_website)
    page = browser.page()


def get_orders():
    """Returns the list of orders"""
    http = HTTP()
    library = Tables()

    ordes_urls = "https://robotsparebinindustries.com/orders.csv"
    http.download(url=ordes_urls, overwrite=True)

    orders_path = "orders.csv"
    orders = library.read_table_from_csv(path=orders_path)
    return orders


def close_annoying_modal():
    """Close the modal that pops up when open website"""
    click_ok_button()


## BUTTONS CLICK


def click_prev_button():
    """Look for and click the button for previewing the robot."""
    page = browser.page()
    page.click("button:text('Preview')")


def click_ok_button():
    """Look for and click order another button."""
    page = browser.page()
    page.click("button:text('Ok')")


def click_order_button():
    """Look for and click button for submitting the order."""
    page = browser.page()
    page.click("button:text('Order')")


def click_another_order_button():
    """Look for and click button for ordering another robot."""
    page = browser.page()
    page.click("button:tect('Order another robot')")


# FORMS


def fill_the_form_and_submit(head, body, legs, address):
    """Fill form of website with data"""

    page = browser.page()
    page.select_option("#head", head)
    page.check("#id-body-{body}".format(body=body))
    page.fill("div.mb-3 input[type=number]", legs)
    page.fill("#address", address)

    while True:
        click_order_button()
        # if element exists, it means there is not any error.
        go_next = page.query_selector("#order-another")

        if go_next:
            click_order_button()
            close_annoying_modal()
            break
