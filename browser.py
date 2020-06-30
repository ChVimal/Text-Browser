import os
from sys import argv
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, Back

path = argv[1]
if not os.path.exists(path):
    os.mkdir(path)
path = os.getcwd() + '/' + path
files = []
back_button = deque()


def print_content(file_name):
    with open(file_name, 'r') as f:
        print(f.read())


while True:
    url = input()

    if url == "exit":
        exit()

    if url == "back":
        if len(back_button) != 0:
            back_button.pop()
            if len(back_button) != 0:
                url = back_button.pop()
            else:
                continue
        else:
            continue
    back_button.append(url)

    if url in files:
        file_name = path + '/' + url
        print_content(file_name)
        continue

    if "." not in url:
        print("Error: Incorrect URL")
        back_button.pop()
        continue

    if url.find('.') == url.rfind('.'):
        url = "https://www." + url
    elif not url.startswith("https://"):
        url = "https://" + url

    files.append(url[url.find('.') + 1:url.rfind('.')])
    file_name = path + '/' + url[url.find('.') + 1:url.rfind('.')]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    with open(file_name, 'w') as f:
        for tag in soup.find_all(["p", "a", "ul", "ol", "li"]):
            if tag.name == "a":
                f.write(Fore.BLUE + tag.get_text() + Style.RESET_ALL)
            else:
                f.write(tag.get_text())

    print_content(file_name)
