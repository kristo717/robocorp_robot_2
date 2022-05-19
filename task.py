"""This robot is for the Robocorp certification level 2."""

# +
import os
import sys
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF

browser = Selenium()
pdf_file = PDF()
input_list = []
dir_path = "./files/"
url = "https://robotsparebinindustries.com/#/robot-order"
csv = "https://robotsparebinindustries.com/orders.csv"


# -

def generate_zip_file(DESTINY_PATH):
    print("WE PROCEED TO GENERATE THE ZIP FILE FOR THE ROBOT STORE FUNCTIONALITY.")


def press_button_and_get_screenshot(button_id, FILE_NAME, DIV):
    while(True):
        if browser.get_element_count(DIV) == 1:
            browser.screenshot(
                DIV, dir_path + FILE_NAME)
            browser.wait_until_element_is_visible(DIV)
            break
        else:
            browser.click_button(button_id)


def download_the_csv_file():
    http = HTTP()
    http.download(
        url=csv,
        overwrite=True)
    os.remove(dir_path + 'orders.csv')
    os.rename('./orders.csv', dir_path + 'orders.csv')


def open_browser(URL):
    print("THE URL WILL BE OPEN: " + URL)
    browser.open_available_browser(URL)
    browser.click_button("OK")


def get_legs_input_id():
    input_list = browser.get_webelements("tag=input")
    id_value = browser.get_element_attribute(input_list[6], "id")

    return id_value


def generate_pdf_file(identity_number, output_path, robot_picture, receipt_picture):
    pdf_file.add_watermark_image_to_pdf(output_path + robot_picture, output_path + "order_" + str(identity_number) + ".pdf")


def fill_and_get_preview(head, body, legs, address):
    browser.select_from_list_by_value("id=head", str(head))
    browser.click_element("id=id-body-" + str(body))
    browser.input_text("id=" + str(get_legs_input_id()), str(legs))
    browser.input_text("id=address", address)
    browser.click_button("id=preview")


def fill_the_form_using_the_data_from_the_csv_file():
    RECEIPT_DIV = "receipt"
    ROBOT_IMAGE_DIV = "robot-preview-image"
    csv = Tables()
    sales_orders = csv.read_table_from_csv("./files/orders.csv", 
                                           columns=["Order number", "Head", "Body", 
                                                    "Legs", "Address"])
    counter = 0
    for sales_order in sales_orders:
        counter = counter + 1
        if counter > 1:
            browser.click_button("OK")
        browser.wait_until_element_is_visible("id=head")
        fill_and_get_preview(sales_order["Head"], sales_order["Body"], sales_order["Legs"], 
                                 sales_order["Address"])
        press_button_and_get_screenshot("preview", "robot_pic_" + str(counter) + ".png", "id=" + ROBOT_IMAGE_DIV)
        press_button_and_get_screenshot("order", "receipt_" + str(counter) + ".png", "id=" + RECEIPT_DIV)
        # generate_pdf_file(number_order, dir_path, "robot" + str(number_order) + ".png", "id=" + RECEIPT_DIV)
        browser.click_button("id=order-another")


def close_browser():
    print("CLOSE THE BROWSER...")
    browser.close_browser()


def minimal_task():
    try:
        open_browser(url)
        download_the_csv_file()
        fill_the_form_using_the_data_from_the_csv_file()
        # get_the_screenshots_and_receipts(dir_path)
        # generate_zip_file(dir_path)
    finally:
        print("HERE WILL BE TERMINATED THE AUTOMATION PROCESS.")
        close_browser()
    print("THE AUTOMATION PROCESS IS OVER, DONE!!!")


if __name__ == "__main__":
    minimal_task()
