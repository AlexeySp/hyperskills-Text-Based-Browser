import os, sys, requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

def do_request(url):
    if not url.startswith('https'):
        url = 'https://' + url
    r = requests.get(url)
    return r.text


def do_file(dir_path, file_name, content):
    if '.' in file_name:
        file_name_full = ''
        file_name = file_name.split('.')
        for _ in range(len(file_name)-1):
            if _ == 0:
                file_name_full = file_name[0]
            else:
                file_name_full += '.' + file_name[_]
    file_name_full = file_name_full
    with open(os.path.join(dir_path, file_name_full), 'w', encoding='UTF-8') as f:
        f.write(content)


def do_parsing(url):
    if not url.startswith('https'):
        url = 'https://' + url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    html = soup.find_all(text=True)
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style',
        # there may be more elements you don't want, such as "style", etc.
    ]
    # print(html)
    for x in html:
        if x.parent.name not in blacklist:
            if len(x.strip()) != 0:
                if x.parent.name == 'a':
                    print(Fore.BLUE + x)
                else:
                    print(x)
                    output += '{}'.format(x)
    # print(output)
    return output
    # if 'https://' not in url:
    #     url = 'https://' + url
    # r = requests.get(url)
    # soup = BeautifulSoup(r.content, 'html.parser')
    # text = ''
    # tags = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    # text = ''
    # for tag in soup.find_all(tags):
    #     print(tag.text)
    # return text


dir_path = sys.argv[1]
try:
    os.makedirs(dir_path)
except OSError:
    pass

queries = deque()
previous_page = ''


while True:
    line = input()
    if line == 'exit':
        break
    elif line == 'back' and len(queries) != 0:
        queries.pop()
        previous_page = queries.pop()
        do_parsing(line)
    # if line == 'bloomberg.com':
    #     data = do_request(line)
    #
    #     data = do_parsing(line)
    #     do_file(dir_path, line, data)
    #     queries.append(line)
    # elif line == 'nytimes.com':
    elif line == 'back' and len(queries) == 0:
        pass

    elif '.com' in line or '.org' in line:

        data = do_request(line)
        data = do_parsing(line)
        do_file(dir_path, line, data)
        queries.append(line)
    else:
        print('error')


