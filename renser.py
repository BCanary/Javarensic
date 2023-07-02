from modules.javarenser import Javarenser
import argparse
"""
TODO:
    Многопоточность
"""

parser = argparse.ArgumentParser()

parser.add_argument('--url', help='Ссылка на начальную страницу')
parser.add_argument('--hop', help='Глубина поиска по страницам')
parser.add_argument('--crossdomain', action="store_true", help='Включает возможность кроссдоменного перехода')

args = parser.parse_args()

if args.crossdomain == None:
    args.crossdomain = False

if __name__ == "__main__":
    print("Парсинг может занять некоторое время...")
    domain = domain=args.url.split("/")[2]
    if args.crossdomain:
        domain = ""
    renser = Javarenser(args.url, hop=int(args.hop), domain=domain)
    renser.sitemapToFile("sitemap.md") 
    renser.commentsToFile("comments.md")

