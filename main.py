from modules.javarenser import Javarenser
import os
"""
TODO:
    Углублённый поиск по директориям сайта (составление карты сайта)
    Улучшение системы поиска комментариев JS
    Многопоточность для js beautify
"""

if __name__ == "__main__":
    url = input("Введите ссылку на страницу для анализа комментариев: ")
    renser = Javarenser(url)
    print("Парсинг может занять некоторое время...")
    scripts = renser.getPageScripts()

    while True:
        os.system("cls")
        print("e. Exit")
        for index, i in enumerate(scripts):
            print(f"{index}. {i.url}")
        user = input()

        if user == "e":
            exit()
        else:
            for j in scripts[int(user)].comments:
                print(j)
            input("Press enter")
