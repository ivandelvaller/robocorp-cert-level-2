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
    browser.configure(slowmo=100)
    open_robot_order_website()
    orders = get_orders()
    print(orders)


def open_robot_order_website():
    """Open robot order website"""
    url_website = "https://robotsparebinindustries.com/#/robot-order"
    browser.goto(url=url_website)


def get_orders():
    """Get orders from website"""
    http = HTTP()
    library = Tables()

    ordes_urls = "https://robotsparebinindustries.com/orders.csv"
    http.download(url=ordes_urls, overwrite=True)

    orders_path = "orders.csv"
    orders = library.read_table_from_csv(path=orders_path)
    print(orders)
