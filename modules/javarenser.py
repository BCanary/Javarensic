import requests
from bs4 import BeautifulSoup as bs
import jsbeautifier
import re
from modules.config import Config
import hashlib

class JavarenserScript:
    all_scripts = []
    all_parsed_scripts = []
    all_hashes = []
    def __init__(self, url, content=None, filehash=None):
        self.url = None
        if url in JavarenserScript.all_scripts:
            return
        JavarenserScript.all_scripts.append(url)
        
        self.url = url
        if content is None:
            try:
                self.content = requests.get(self.url).text
            except:
                pass
        else:
            self.content = content
        self.comments = []
        self.urls = []
        
        if filehash == None:
            filehash = hashlib.md5(self.content.encode()).hexdigest()
        if filehash in JavarenserScript.all_hashes:
            self.url = None
            return
        JavarenserScript.all_hashes.append(filehash)

        #try:
        #    self.content = jsbeautifier.beautify(self.content)
        #except:
        #    pass
        print(f"НАЧАЛО ОБРАБОТКИ СКРИПТА {self.url}")
        self._findComments()
        self._findLinks()

        JavarenserScript.all_parsed_scripts.append(self)
        #print("СКРИПТ ОБРАБОТАН")

    def __repr__(self):
        return f"JavarenserScript({self.url})"
    
    def _findLinks(self):
        pattern = r"""['"]?\/([^'"\s]*)['"]?"""
        self.urls = re.findall(pattern, self.content, re.DOTALL | re.MULTILINE)
        self.urls = [url for url in self.urls if len(url) > 2]
    def _findComments(self):
        pattern = r'(?://[^\n]*|/\*.*?\*/)'

        self.comments = re.findall(pattern, self.content, re.DOTALL | re.MULTILINE)

#class JavarenserUrl:
#    def __init__(self, url):
#        self.url = url
#        self.protocol = ""
#        self.domain = ""
#        self.path = ""
#        self.args = ""
#
#    def parse(self):
#        pass
        
class JavarenserPage:
    all_pages = []
    def __init__(self, url, hop=5, domain=""):
        #print(hop, url)
        url = url.split("#")[0]
        if url[-1] == "/":
            url = url[0:-1]

        #print(hop, url)
        self.url = ""
        if url in JavarenserPage.all_pages:
            return
        JavarenserPage.all_pages.append(url)

        self.url = url
        self.scripts = []
        self.pages = []
        self.hop = hop 
        self.domain = domain
        
        if ".pdf" in url or ".docx" in url or ".mp4" in url or ".jpg" in url or ".png" in url:
            return
        if domain != "":
            if domain not in url:
                return
        if hop == 0:
            return

        try:
            self.content = requests.get(self.url, headers=Config.HEADERS)
            self.soup = bs(self.content.text, "lxml")
            #print(f"ХОП ({self.hop}). Получили страницу: {self.url}")
        except:
            #print(f"ОШИБКА ДЛЯ: {self.url}")
            return
        print(self.hop, self.url)
        self._getAllPages()
        self._getAllScripts()
        #print(self.pages)
        #print(self.scripts) 

    def __repr__(self):
        return f"JavarenserPage({self.url})"
    
    def _getFullUrl(self, url):
        if url.startswith("https://") or url.startswith("http://"):
            return url
        else:
            if url.startswith("/"):
                return "/".join(self.url.split("/")[:3]) + url
            else:
                return "/".join(self.url.split("/")[:3]) + "/" + url

    def _getAllPagesRaw(self):
        links = [link["href"] for link in self.soup.find_all("a") if link.has_attr("href")]
        forms = [link["action"] for link in self.soup.find_all("form") if link.has_attr("action")]
        return links + forms
    
    def _getAllPages(self):
        pages = self._getAllPagesRaw()
        #print(f"{self.url}:PAGES:{pages}")
        for i in pages:
            page = JavarenserPage(self._getFullUrl(i), self.hop-1, self.domain)
            if page.url == "":
                continue
            self.pages.append(page)

    def _getAllScriptsRaw(self):
        raw_scripts = self.soup.findAll("script")
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
                script = JavarenserScript( self._getFullUrl(i["src"]) )
                if script.url == None:
                    continue
                self.scripts.append(script)
            else:
                filehash = hashlib.md5(i.text.encode())
                script = JavarenserScript(f"{self.url}:INNER_SCRIPT({str(filehash.hexdigest())})", i.text, filehash=str(filehash.hexdigest()))
                if script.url == None:
                    continue
                self.scripts.append(script)

class Javarenser:
    def __init__(self, url, hop=3, domain=""):
        self.page = JavarenserPage(url, hop, domain)
        self._getAllPages()

    def _getAllPages(self):
        self.page._getAllPages()
    
    def commentsToFile(self, filename):
        scripts = JavarenserScript.all_parsed_scripts 
        with open(filename, "w", encoding="UTF-8") as file:
            for index, i in enumerate(scripts):
                file.write("\n------\n"+i.url+"\n---\n")
                for j in i.comments:
                        file.write("\t"+str(j))
                file.write("\n---URLS:\n")
                for j in i.urls:
                    file.write("\t"+j+"\n")

    def sitemapToFile(self, filename):
        sitemap = ""
        stack = [[self.page, 0]]

        while stack:
            page, depth = stack.pop()
            sitemap += "\t"*depth+"- "+page.url+"\n"
            for i in reversed(page.pages):
                stack.append([i, depth+1])

        with open(filename, "w") as file:
            file.write(sitemap)
