# Author: JuliMonsa
# little program to get crypto prices
# and save them into an sqlite3 .db
# script meant only to practice python.

import sqlite3
from requests import get
from datetime import datetime
from os.path import exists
from time import sleep

from rich import print as richPrint
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Confirm
from rich.console import Console
from rich.table import Table


# =====================================
# Script Beggining :)
richPrint(Panel(Text(">>> Beggining <<<", style="#00d700", justify="center")))
sleep(1.5)


# create db, cursor, table and commit
try:
    # if exists, connect.
    if exists('crypto_prices.db'):
        conn = sqlite3.connect('crypto_prices.db')
        cur = conn.cursor()
        richPrint("==| [green]Connected through relative path")
        sleep(1)
    
    # if not exists, create and connect.
    else:
        with open('crypto_prices.db', 'w', encoding="utf8"):
            conn = sqlite3.connect('crypto_prices.db')
            cur = conn.cursor()
            richPrint("==| [green]Created new db and connected.")
            sleep(1)

except:
    # otherwise use abs. path.
    FULL_PATH = "¯\_(ツ)_/¯"
    conn = sqlite3.connect(FULL_PATH)
    cur = conn.cursor()
    richPrint("==| [red]Connected through absolute path")


# uncomment code below if reboot table required
# cur.execute("DROP TABLE IF EXISTS crypto;") 
cur.execute("""CREATE TABLE IF NOT EXISTS crypto(
    query INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    name TEXT,
    price TEXT
);""")

conn.commit()


def update_price(date: str , crypto_name: str, price: str):
    with conn:
        cur.execute("INSERT INTO crypto(date, name, price) VALUES(?, ?, ?);", (date, crypto_name, price))
        conn.commit()
        richPrint("Data inserted [green]succesfully !")


def get_crypto_price(crypto: str, currency: str) -> tuple:
    """
    Custom function to get coins values 
    using cryptocompare public api 
    returns tuple (crypto, price)
    """
    crypto = crypto.lower()
    currency = currency.upper()
    BASE_URL = f"https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms={currency}"
    if crypto and currency:
        try: 
            req = get(BASE_URL).json()
            price = req[currency]
            return (crypto, f"{price} {currency}")
        except: 
            richPrint("[red]==! There was an error when calling API !")
            sleep(1.5)
            richPrint("[red]==! try again in a few minutes or create an issue !")
            sleep(1.5)
            exit()
    else:
        print("[red]==! There was an error when calling get_crypto_price() !")


def runScript():
    while True:
        checkMarket = Confirm.ask("==| Wanna check crypto market?")
        sleep(1)
        
        if checkMarket:           
            # calling API.
            cryptoOption = str(input("==| Which one? (BTC,LTC,ETH or any other...)\n>>> "))
            currrencyOption = str(input("==| Which currency? (USD,ARS,CNY,CLP or any other...)\n>>> "))
            actualQuery = get_crypto_price(cryptoOption, currrencyOption)

            # printing price.
            richPrint(Panel(Text(f"{actualQuery}", style="#00d700", justify="center")))
            sleep(1)

            # ask for saving data into sql.
            saveOption = str(input("==| Wanna save data in sql? (y/n)\n>>> ")) 
            if saveOption.lower() == 'y':
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                update_price(now, actualQuery[0], actualQuery[1])
            else: pass

        else:
            richPrint(Panel(Text("Okay no problem see ya later :)", style="#00d700", justify="center")))
            exit()

        # printing every row in table
        totalCol = cur.execute("SELECT COUNT(*) FROM crypto") 
        totalCol = int(totalCol.fetchone()[0])

        richPrint(f'A table was found with [blue]{totalCol}[/blue] columns !')
        sleep(1)
        if totalCol != 0:
            checkTables = Confirm.ask("==| Wanna check saved records?")
            if checkTables: 
                dataToPrint = cur.execute("SELECT name, price FROM crypto")
                rows = dataToPrint.fetchall()

                print()
                table = Table(title="Saved crypto prices")
                table.add_column("Crypto", justify="center", style="cyan")
                table.add_column("Price", justify="center", style="cyan")

                for i in rows:
                    table.add_row(i[0], i[1])  # i[0] for crypto, i[1] for currency...              

                console = Console()
                console.print(table)
        else:
            print("==! Empty database :(")
            sleep(1)


        exitOption = Confirm.ask("==| Wanna leave the program?")
        sleep(1)
        if exitOption:
            richPrint(Panel(Text("See you soon :)", style="#00d700", justify="center")))
            exit()
        else:
            print("\n\n\n\n\n\n")
            pass

if __name__ == "__main__":
    runScript()