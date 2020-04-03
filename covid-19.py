'''
Covid-19 Death/Total Cases Checker
'''

import requests, bs4

res = requests.get('https://www.worldometers.info/coronavirus/')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features="lxml")
table = soup.find_all('tbody')
table_body = table[0].find_all("tr")
table_total = table[1].find_all("td")
table_cont = []

for elem in table_body:
    table_cont.append(elem.find_all("td"))

country_dpt = {}

for elem in table_cont:
    country = elem[0].getText()
    total = float(elem[1].text.replace(',', ''))

    if elem[3].text != ' ':
        deaths = elem[3].text.replace(',', '')
        deaths = float(deaths.replace(' ', ''))
        country_dpt[country] = (deaths / total) * 100
    else:
        country_dpt[country] = 0

    country_dpt = {k: v for k, v in sorted(
    country_dpt.items(), key=lambda item: item[1], reverse=True)}

    total = float(table_total[1].text.replace(',', ''))
    total_deaths = float(table_total[3].text.replace(',', ''))

print("Welcome to the Covid-19 Death per Total stat pack!")

def main():
    choice = input("\nWhich country's info would you like to see?\n\nPick one using the format: 'Gambia', or type 'top10' or 'show_all':\n")

    if choice == "show_all":
        print("\nCovid-19 Deaths per Total cases:\n")
        print(table_total[0].text, str((total_deaths / total) * 100) + "%\n")
        for k, v in country_dpt.items():
            print(k + ":", str(v) + "%")
    elif choice == "top10":
        print("\nCovid-19 Deaths per Total cases:\n")
        print(table_total[0].text, str((total_deaths / total) * 100) + "%\n")
        dpt_list = list(country_dpt.items())
        for i in range(10):
            print(dpt_list[i][0] + ":", str(dpt_list[i][1]) + "%")
        
    else:
        while country_dpt.get(choice, False) == False:
            choice = input("That country doesn't exist! Either that or you didn't use a capital letter, try again:\n")
        print("\nCovid-19 Deaths per Total cases:\n")
        print(table_total[0].text, str((total_deaths / total) * 100) + "%\n")
        print(choice + ":", str(country_dpt[choice]) + "%\n")
        print("That's {} difference from the average!".format(str(country_dpt[choice] - ((total_deaths / total) * 100)) + "%"))


main()

again = input("\nWant to check another? (y/n)\n")

while again != 'n':
    main()
    again = input("\nWant to check another? (y/n)\n")

print("\nThanks! See you later (hopefully).")
