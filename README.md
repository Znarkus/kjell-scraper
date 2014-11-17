
# Kjell scraper

Hämta lagerstatus för en produkt, för alla butiker. Exporterar lagerstatus, lat och long per butik, till XLSX.

Testat med Python 3.4.


## Installera

Checka ut via Git först. Använd sedan PiP för att installera beroenden (http://pip.readthedocs.org/en/latest/index.html).

    pip install -r requirements.txt


## Användning

    $ python3.4 kjell.py -h
    usage: kjell.py [-h] url

    Hämta lagerstatus för alla butiker och exportera till XLSX

    positional arguments:
      url         URL till produkt

    optional arguments:
      -h, --help  show this help message and exit
