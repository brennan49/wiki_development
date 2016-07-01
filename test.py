import requests
import getpass
from requests.auth import HTTPDigestAuth
import json
import argparse
import sys
import keyring

BASE_URL = "http://wiki.optum.com/rest/api/content"

#my_response = requests.get(url, auth = HTTPDigestAuth(input("username: "), input("Password: ")))

#print(my_response.status_code)

def fixGetpass():
  import getpass
  import warnings
  fallback = getattr(getpass, 'fallback_getpass', None) # >= 2.6
  if not fallback:
      fallback = getpass.win_getpass(stream=None) # <= 2.5
  getpass.win_getpass = fallback
  if hasattr(getpass, 'GetPassWarning'):
      warnings.simplefilter("ignore", category=getpass.GetPassWarning)

def getChildPages():
    pageid = 63782193
    url = '{base}/{pageid}?expand=children.children'.format(base=BASE_URL, pageid=pageid)
    request = requests.get(url, auth=auth)
    request.raise_for_status()
    return request.json()['children']

def pprint(data):
    print (json.dumps(data,sort_keys = True, indent = 4, separators = (', ', ' : ')))

def getUserInfo():
    #print("Please enter your username and password.")
    username = input("username: ")
    fixGetpass()
    passwd = getpass.win_getpass(stream=None)
    auth = (username, passwd)
    return auth

def addFile(file):
    {}

def update_page(pageName,data):
    {}

def update_page_id(pageID, data):
    {}

def getPageAncestors(auth, pageid):
    url = '{base}/{pageid}?expand=ancestors'.format(base = BASE_URL, pageid = pageid)
    request = requests.get(url, auth = auth)
    request.raise_for_status()
    return request.json()['ancestors']

def searchUsingPageID(pageID):
    url = BASE_URL + '/search?cql=id~' + pageID
    request = requests.get(url, auth=auth)
    request.raise_for_status()
    return request.json()['title', 'id']

def searchUsingPageName(name, auth):
    request = requests.get(BASE_URL, params={"title": name}, auth=auth)
    request.raise_for_status()
    return request.json()

def createNewPage(page_name, data, auth):
    request = requests.post(BASE_URL, params={"title":page_name, "type":"page", "space":{"key": "TST"},
                                             "body":{"storage":{"value":data,"representation":"storage"}}},
                            auth=auth)
    request.raise_for_status()
    return request.json()

def createPageAsChild(page_name, parentId, data, auth):
    request = requests.post(BASE_URL, params={"type":"page","title":page_name, "ancestors":[{"id":parentId}],
                                              "space":{"key":"TST"},
                                              "body":{"storage":{"value":data,"representation":"storage"}}},
                            auth=auth)
    request.raise_for_status()
    return request.json()

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
        auth = getUserInfo()

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
        else:
            print("Please type either id or name")
    elif(ans == "3"):
        pageName = input("Please specify a page name. ")
        location = input("please select where you would like to create the page. ")
        createNewPage(pageName, location)

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

auth = ("devlin.brennan", "Brenndev_49")#getUserInfo()
#anc = searchUsingPageName("Foundation Engineering Organization", auth)
#anc = getPageAncestors(auth, 64684723)
#anc = getChildPages()
#anc = searchUsingPageID(63782193)
data = "this is a test page"
#anc = createNewPage("Test Page", data, auth)
anc = createPageAsChild("New Test Page", 64684724, data, auth)
pprint(anc)