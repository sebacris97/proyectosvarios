import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests_html import HTMLSession
from urllib.parse import urljoin
import webbrowser
import sys
import logging

#para no mostrar mensaje de conecction
logging.getLogger("urllib3").setLevel(logging.WARNING)

# initialize an HTTP session
session = HTMLSession()

url = 'https://www.skidrowreloaded.com/'

def get_all_forms(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.find_all("form")

#print(get_all_forms(url))

def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

form_details = get_form_details(get_all_forms(url)[0])

#print(form_details)

# the data body we want to submit
data = {}
contador=0
for input_tag in form_details["inputs"]:
    if input_tag["type"] == "hidden":
        # if it's hidden, use the default value
        data[input_tag["name"]] = input_tag["value"]
    elif input_tag["type"] != "submit":
        # all others except submit, prompt the user to set it
        #value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
        value = input('Ingrese el nombre del juego: ')
        data[input_tag["name"]] = value
        contador+=1
    if contador==1:
        break


# join the url with the action (form request URL)
url = urljoin(url, form_details["action"])

if form_details["method"] == "post":
    res = session.post(url, data=data)
elif form_details["method"] == "get":
    res = session.get(url, params=data)




# the below code is only for replacing relative URLs to absolute ones
soup = BeautifulSoup(res.content, "html.parser")
for link in soup.find_all("link"):
    try:
        link.attrs["href"] = urljoin(url, link.attrs["href"])
    except:
        pass
for script in soup.find_all("script"):
    try:
        script.attrs["src"] = urljoin(url, script.attrs["src"])
    except:
        pass
for img in soup.find_all("img"):
    try:
        img.attrs["src"] = urljoin(url, img.attrs["src"])
    except:
        pass
for a in soup.find_all("a"):
    try:
        a.attrs["href"] = urljoin(url, a.attrs["href"])
    except:
        pass

# write the page content to a file
#open("page.html", "w").write(str(soup.encode("utf-8")))


#webbrowser.open("page.html")



divs=[]
for div in soup.find_all('div',{'class': 'post class='}):
    #print(div)
    #print('\n\n\nAAAAAAAAAAAAAAAAAAA\n\n\n')
    divs.append(div)


msg_error = 'No search results found, try searching again'
hayh3=divs[1].find("h3")!=None
if hayh3:
    not_ok = (msg_error == divs[1].find("h3").text)
else:
    not_ok = False
if len(divs)==2 and not_ok:
    print(divs[1].find("h3").text)
    sys.exit()

"""           #HASTA ACA TENGO EL LINK DEL POST DEL JUEGO
h2=[]
juegos={}
for tag in divs[1:]:
    h2Tags = tag.find_all("h2")
    h2.append(h2Tags[0])
    for tag in h2Tags:
        print (tag.text)
        juegos[tag.text]=tag.find("a").get('href')


print('\n')  

print("\n".join("{!r}: {!r},\n".format(k, v) for k, v in juegos.items()))
"""


#ACA OBTENGO DIRECTAMENTE EL LINK DE 1FICHIER
h2=[]
juegos={}
for tag in divs[1:]:
    h2Tags = tag.find_all("h2")
    h2.append(h2Tags[0])
    for tag in h2Tags:
        URL = tag.find("a").get('href')
        html_text = requests.get(URL).text
        soup2 = BeautifulSoup(html_text, 'html.parser')
        value = soup2.find_all('a',{'href':lambda value: value and value.startswith('https://1fichier.com/')})
        if len(value)!=0:
            links1fichier = []
            for i in value:
                links1fichier.append(i.get('href'))
        else:
            links1fichier='No Aplica'
        juegos[tag.text]=links1fichier


print('\n\n')

for i in juegos.keys():
    #print(i+': '+str(juegos[i])+'\n')
    print(i+': ')
    if isinstance(juegos[i], str):
        print(juegos[i])
    else:
        for k in juegos[i]:
            print(k)
    print('\n')

o=input()

