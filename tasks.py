from robocorp.tasks import task
from robocorp import browser
import shutil

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(slowmo=1000)

    open_robot_order_website()
    close_annoying_modal()
    read_data_and_iterate()
    archive_receipts()


def read_data_and_iterate():
    """Read the data from csv and create the orders"""
    orders = get_orders()

    for order in orders:
        id_number = order["Order number"]
        head = order["Head"]
        body = order["Body"]
        leags = order["Legs"]
        address = order["Address"]
        fill_the_form_and_submit(
            head,
            body,
            leags,
            address,
            id_number,
        )


# FUNCTIONS FOR SPECITICATION


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


def store_receipt_as_pdf(id_order):
    """Stores the robot order .pdf file with the id_order as name of the file."""
    page = browser.page()
    pdf = PDF()

    path = "output/receipts/{id_order}.pdf".format(id_order=id_order)

    receipt_element = page.locator("#receipt").inner_html()
    pdf.html_to_pdf(receipt_element, path)
    return path


def screenshot_robot(id_order):
    """SC for the robot and save it."""
    page = browser.page()
    path = "output/screenshots/{id_order}.png".format(id_order=id_order)
    page.locator("#robot-preview-image").screenshot(path=path)
    return path


def embed_screenshot_to_receipt(pdf_path, sc_path):
    """Get the sc of the robor and add it to the pdf file in receipts folder: overwrite the pdf file."""
    pdf = PDF()
    pdf.add_watermark_image_to_pdf(
        image_path=sc_path, source_path=pdf_path, output_path=pdf_path
    )


def archive_receipts():
    """Compress the file in .zip file"""
    archive = Archive()
    archive.archive_folder_with_zip("./output/receipts", "./output/receipts.zip")


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
    page.click("button:text('Order another robot')")


# FORMS


def fill_the_form_and_submit(head, body, legs, address, id_number):
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
            pdf_path = store_receipt_as_pdf(id_number)
            sc_path = screenshot_robot(id_number)
            embed_screenshot_to_receipt(pdf_path, sc_path)

            click_another_order_button()
            close_annoying_modal()

            break
