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
