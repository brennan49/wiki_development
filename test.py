import requests
import getpass
from requests.auth import HTTPDigestAuth
import json

url = ""

my_response = requests.get(url, auth = HTTPDigestAuth(input("username: "), input("Password: ")))

print(my_response.status_code)


def getUserPass():
    {}

def addFile(file):
    {}

def update_page(pageName,data):
    {}

def update_page_id(pageID, data):
    {}

def searchUsingPageID(pageID):
    {}

def searchUsingPageName(name):
    {}

def createPage(page_name, location):
    {}

def main():
    ans = input("""
                    Please choose from the following list by entering their associated number on the left:
                    1. login
                    2. search for page
                    3. create a new page
                    4. update page
                    5. add file to page
                    """)
    if(ans == "1"):
        getUserPass()

    elif(ans == "2"):
        searchBy = input("""
                          search for page using pageID or page name?
                          (please type id or name)
                          """)
        if(searchBy == "id"):
            id = input("What is the id number? ")
            searchUsingPageID(id)
        if(searchBy == "name"):
            page = input("What is the page name? ")
            searchUsingPageName(page)
    elif(ans == "3"):
        pageName = input("Please specify a page name. ")
        location = input("please select where you would like to create the page. ")
        createPage(pageName, location)

    elif(ans == "4"):
        searchBy = input("""
                          search for page to update using pageID or page name?
                          (please type id or name)
                          """)
        if (searchBy == "id"):
            id = input("What is the id number? ")
            update_page_id(id, data)
        if (searchBy == "name"):
            page = input("What is the page name? ")
            update_page(pageName, data)
