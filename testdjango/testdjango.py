import requests

class Testing:
    def __init__(self,url,word):
        self.URL=url
        self.WORD=word
        self.response = requests.get(self.URL)
        self.TEKST=self.response.text
        self.check()
        """def check(self): zogt voor de test of het woord (csrfmiddlewaretoken) in de HTML structuur staat. En print resultaat
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
        if self.WORD in self.TEKST:
            print("It is Django!")
        else:
            print ("It is not Django")

if __name__ == '__main__':
  URL='http://localhost:8000/admin/login/?next=/admin/'
  WORD="csrfmiddlewaretoken"
  test=Testing(URL,WORD)