"""
Denne fila tar seg av alt fra rå txt fil til å få
alle nye transaksjoner inn i databasen
"""
import csv
import os
from transactions.models import Transaction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
in_path = os.path.join(BASE_DIR, 'scripts/transaksjonliste.txt')
out_path = os.path.join(BASE_DIR, 'scripts/transaksjonliste-ut.csv')


def file_fixer():
    """
    Denne funksjonen tar inn rå txt fil fra dnb og
    gjere den til ein csv fil som kan formatterast.
    """

    with open(in_path, 'r', encoding="ISO-8859-1") as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split("\";") for line in stripped if line)

        with open(out_path, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)


def format_fix(row):
    """
    Funksjonen formaterer ein rad i forrige csv-fil. Den reformaterer
    dato, setter "" til null, fjerner 1000-sklle og bytter
    komma med punktom i desimal. I tillegg slår den sammen utgift og
    inntekt til "amount"
    """
    #Namnsetter alle (relevante) radene:
    date = row[0]
    description = row[1]
    expence = row[3]
    deposit = row[4]
    t_type = row[5]
    amount = row[6]

    #Fikser dato:
    date = date.replace("\"", "")
    row_split = date.split('.')

    seq = (row_split[2], row_split[1], row_split[0])
    date = "-".join(seq)

    #Tappert  forsøk på å fjerne hermeteik
    description = description.strip("\"")
    expence = expence.strip("\"")
    deposit = deposit.strip("\"")

    #Splitter opp beskrivelsen:
    # Regel:
    #   1. Sett første ord aleina.
    #   2. Dersom beskrivelse inneholder "Vipps", sett typen lik vipps

    desc_list = description.split(" ")
    t_type = desc_list[0]
    description = " ".join(desc_list[1:])
    if "Vipps" in description:
        t_type += " vipps"


    #Fjerner komma i tusen og bytter komma med punktum
    expence = str(expence).replace(".", "")
    expence = expence.replace(",", ".")
    deposit = str(deposit).replace(".", "")
    deposit = deposit.replace(",", ".")

    #Sjekker om utgift eller inntekt er tom og setter den andre
    #lik amount, visst det er utgift blir den negativ
    if not any(char.isdigit() for char in row[3]):
        amount = float(deposit)
    else:
        amount = -float(expence)

    return [date, t_type, description, amount]


def importer():
    """
    Dette er "main" funskjonen som interagerer med databasen
    og som faktisk legger inn dei nye transaksjonenen.
    Denne vil returnere det som ikkje vart lagt inn,
    fordi dei allereie eksisterer.
    """
    #Lager liste der eg legg transaksjonar som blir henta og ikkje laga:
    get_list = []

    #Gjer txt-fila i mappen om til csv-fil
    file_fixer()

    with open(out_path) as file:
        reader = csv.reader(file)
        r_0 = next(reader)
        r_0.append("type")
        r_0.append('amount')
        r_0.append('category')
        r_0.append('account')
        r_0.append('project')


        for row in reader:
            #Legger til dei fire kollonenne (amount, account, subaacount, project), tomme.
            row.append("")
            row.append("")

            #Omformatterer rader:
            row = format_fix(row)
            row.append("")
            row.append("")
            row.append("")
            print(row)


            try:
                obj, created = Transaction.objects.get_or_create(
                    date=row[0],
                    transaction_type=row[1],
                    description=row[2],
                    amount=row[3]
                    )

            except Transaction.MultipleObjectsReturned:
                continue

            if not created:
                get_list.append(obj.pk)

    return get_list
