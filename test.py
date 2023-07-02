from modules.test_module import Test, test_flask_server
from modules.javarenser import Javarenser, JavarenserPage, JavarenserScript
from tests.server import app
from tests.manifest import HOST, PORT, BASE_URL, pages, scripts

@test_flask_server(app=app, host=HOST, port=PORT)
def test_function():
    url = BASE_URL
    jr = Javarenser(url, domain="127.0.0.1:5000")
    
    print(f"СТРАНИЦЫ УКАЗАННЫЕ В МАНИФЕСТЕ ({len(pages)}):")
    print(pages)
    print(f"ПОЛУЧЕННЫЕ СТРАНЦИЫ ({len(JavarenserPage.all_pages)})")
    print(JavarenserPage.all_pages)

    print(f"СКРИПТЫ УКАЗАННЫЕ В МАНИФЕСТЕ ({len(scripts)}):")
    print(scripts)
    print(f"ПОЛУЧЕННЫЕ СТРАНЦИЫ ({len(JavarenserScript.all_scripts)})")
    print(JavarenserScript.all_scripts)

    jr.sitemapToFile("sitemap.md")
    jr.commentsToFile("comments.md")
    input("Press enter to shutdown")

if __name__ == "__main__":
    # The only way to stop Flask server in thread is to throw an error when thread is setDaemon(True)
    try:
        test_function()
    except RuntimeError:
        pass
