import requests
import getpass
from requests.auth import HTTPDigestAuth
import json
import argparse
import sys
import keyring

BASE_URL = "http://wiki.optum.com/rest/api/content"

def fixGetpass():
    import getpass
    import warnings
    fallback = getattr(getpass, 'fallback_getpass', None) # >= 2.6
    if not fallback:
        fallback = getpass.win_getpass(stream=None) # <= 2.5
    getpass.win_getpass = fallback
    if hasattr(getpass, 'GetPassWarning'):
        warnings.simplefilter("ignore", category=getpass.GetPassWarning)


def getChildPages(auth):
    pageName = "AWS Project"
    pageData = searchUsingPageName(pageName, auth)
    pythonPageData = json.loads(pageData)
    pageId = pythonPageData["id"]
    url = '{base}/search?cql=parent={pageName}'.format(base=BASE_URL, pageName=pageName)
    request = requests.get(url, auth=auth)
    request.raise_for_status()
    return request.json()['children']


def pprint(data):
    print (json.dumps(data,sort_keys = True, indent = 4, separators = (', ', ' : ')))


def getUserInfo():
    username = input("username: ")
    fixGetpass()
    passwd = getpass.win_getpass(stream=None)
    auth = (username, passwd)
    return auth


def addFile(file):
    {}


def update_page(pageName, data, auth):
    {}


def update_page_id(pageID, data, auth):
    {}


def getPageAncestors(pageid, auth):
    url = '{base}/{pageid}?expand=ancestors'.format(base = BASE_URL, pageid = pageid)
    request = requests.get(url, auth = auth)
    request.raise_for_status()
    return request.json()['ancestors']


def searchUsingPageID(pageID, auth):
    #url = BASE_URL + '/search?cql=id=' + pageID
    #request =  requests.get(BASE_URL, params={"id": pageID}, auth=auth)
    request = requests.get(BASE_URL + "/" + pageID + "?status=any", auth=auth)
    request.raise_for_status()
    return request.json()


def searchUsingPageName(name, auth):
    request = requests.get(BASE_URL, params={"title": name}, auth=auth)
    request.raise_for_status()
    return request.json()


def createNewPage(page_name, data, auth):
    payload = {"title":page_name, "type":"page", "space":{"key": "TST"},
                                             "body":{"storage":{"value":data,"representation":"storage"}}}
    request = requests.post(BASE_URL + "/", data=payload,
                            auth=auth)
    request.raise_for_status()
    return request.json()


def createPageAsChild(page_name, parentId, data, auth):
    payload = {"type":"page","title":page_name, "ancestors":[{"id":parentId}],

                                              "body":{"storage":{"value":data,"representation":"storage"}}}
    request = requests.post(BASE_URL + "/", params={json.dumps(payload)},
                            auth=auth)
    request.raise_for_status()
    return request.json()


def main():
    while(1):
        auth = ("devlin.brennan", "Brenndev_49")
        ans = input("""
                    Please choose from the following list by entering their associated number on the left:
                    1. search for page
                    2. create a new page
                    3. update page
                    4. add file to page
                    5. Exit
                    """)
        #if ans == "1":
         #   auth = getUserInfo()


        '''After searching, ask user if they would like to do anything with the information received
           for example, create a new page as the child of page found, etc.'''
        if ans == "1":
            searchBy = input("""
                                search for page using pageID or page name?
                                (please type id or name)
                             """)

            if searchBy == "id":
                id = input("What is the id number? ")
                page = searchUsingPageID(id, auth)
                pprint(page)

            elif searchBy == "name":
                pageName = input("What is the page name? ")
                parentPage = searchUsingPageName(pageName, auth)
                pprint(parentPage)
                results = parentPage['results']
                parentId = results[0]['id']
                print("Would you like to perform any other actions of this page?")
                choice = input("""Your choices are:
                                  1. Create Child Page
                                  2. Update page
                                  3. Place attachment""")

                if choice == "1":
                    name = input("What do you want the child page to be named?")
                    data = input("Would you like to add any comments to the page?")
                    createPageAsChild(name, parentId, data, auth)

                elif choice == "2":
                    data = input("What would you like to add to the page?")
                    update_page(pageName,data, auth)

                elif choice == "3":
                    location = input("Please type the location of the file")
                    page = input("Where would you like to place the file? (specify page name)")
                    addFile(page, location, auth)

            else:
                print("Please type either id or name")


        #Create a new page at the root
        elif ans == "2":
            pageName = input("Please specify a page name. ")
            location = input("please select where you would like to create the page. ")
            createNewPage(pageName, location, auth)


        #will prompt to search for page to update using id or name
        #next it will find the page and update with the data
        #likely redundant and will be removed in end product
        elif ans == "3":
            searchBy = input("""
                          search for page to update using pageID or page name?
                          (please type id or name)
                          """)
            if searchBy == "id":
                id = input("What is the id number? ")
                data = ""
                update_page_id(id, data, auth)
            if searchBy == "name":
                pageName = input("What is the page name? ")
                update_page(pageName, data, auth)


        #search for page using id or name, once page found, attach specified document to it
        elif ans == "4":
            {}


        #exit the program
        elif ans == "5":
            print("Thank you.")
            break


        #error occurred
        else:
            print("Please enter the desired number from the list above.")


auth = ("devlin.brennan", "Brenndev_49")#getUserInfo()
#anc = searchUsingPageName("AWS Project", auth)
#id = anc["id"]
#anc = getPageAncestors(64684723, auth)
#anc = getChildPages(auth)
#anc = searchUsingPageID("64684724", auth)
data = "this is a test page"
#anc = createNewPage("Test Page", data, auth)
anc = createPageAsChild("New Test Page", 65700826, data, auth)
#main()
#anc = searchUsingPageName("AWS Project", auth)
pprint(anc)
#results = anc['results']
#print (results[0]['id'])