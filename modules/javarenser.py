import requests
from bs4 import BeautifulSoup as bs
import jsbeautifier
import re
from modules.config import Config

class JavarenserScript:
    def __init__(self, url, content=None):
        self.url = url
        if content is None:
            self.content = requests.get(self.url).text
        else:
            self.content = jsbeautifier.beautify(content)
        self.comments = []
        self._findComments()

    def _findComments(self):
        pattern = r'//.*?$|/\*.*?\*/'

        self.comments = re.findall(pattern, self.content, re.DOTALL | re.MULTILINE)

class JavarenserPage:
    def __init__(self, url):
        self.url = url
        self.scripts = []
        self.pages = []
	
    def _getScriptSrc(self, script_url):
        if script_url.startswith("https://") or script_url.startswith("http://"):
            return script_url
        else:
            if not script_url.startswith("/"):
                return "/".join(self.url.split("/")[:3]) + "/" + script_url
            else:
                return self.url+script_url

    def _getAllScriptsRaw(self):
        a = requests.get(self.url, headers=Config.HEADERS)
        soup = bs(a.text, "lxml")
        raw_scripts = soup.findAll("script")
        return raw_scripts

    def _checkIfExcluded(self, url):
        for i in Config.EXCLUDE_SCRIPTS:
            if i in url:
                return True
        return False

    def _getAllScripts(self):
        raw_scripts = self._getAllScriptsRaw()
        for index, i in enumerate(raw_scripts):
            if i.has_attr("src"):
                if self._checkIfExcluded(i["src"]):
                    continue
                script = JavarenserScript( self._getScriptSrc(i["src"]) )
                self.scripts.append(script)
            else:
                script = JavarenserScript( None, i.text )
                self.scripts.append(script)

class Javarenser:
	def __init__(self, url):
		self.page = JavarenserPage(url)
	
	def getPageScripts(self):
		self.page._getAllScripts()
		return self.page.scripts
