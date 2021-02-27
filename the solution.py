import csv
import re
from datetime import datetime

def standardFormat(date, des, debit, credit, currency, cardName, transaction, location):
    return {
        'date': date,
        'des' : des,
        'debit': debit,
        'credit': credit,
        'currency': currency,
        'cardName': cardName,
        'transaction': transaction,
        'location': location
    }


def writeCSV(filename, output):
    f = open(filename, 'w',newline='')
    writer = csv.writer(f)
    writer.writerow(["Date", "Transaction Description" , "Debit", "Credit", "Currency", "CardName", "Transaction", "Location"])
    for data in sorted(output, key=lambda x: x['date']):
        writer.writerow([
            data['date'].strftime("%d-%m-%Y"),
            data['des'],
            data['debit'],
            data['credit'],
            data['currency'],
            data['cardName'],
            data['transaction'],
            data['location']
        ])
     

def parseHDFC(_type, name, line):
    
    def domesticParser():
        date = datetime.strptime(line[0], '%d-%m-%Y')
        des = line[1].strip()
        debit = 0
        credit = 0
        if len(line[2].split(' ')) == 2:
            credit = line[2].split(' ')[0]
        else:
            debit = line[2]
        location = des.split()[-1]
        return standardFormat(date, des, debit, credit, 'INR', name, 'Domestic', location )

    def internationParser():
        date = datetime.strptime(line[0], '%d-%m-%Y')
        des = line[1].strip()
        debit = 0
        credit = 0
        if len(line[2].split(' ')) == 2:
            credit = line[2].split(' ')[0]
        else:
            debit = line[2]
        location = des.split()[-2]
        currency = des.split()[-1]

        des = ' '.join(des.split()[:-1])
        return standardFormat(date, des, debit, credit, currency, name, 'International', location)

    return domesticParser() if _type == 'Domestic' else internationParser()


def hdfcParser(fileName):
    file1 =  open(fileName, newline='', encoding='UTF-8')
    reader = csv.reader(file1)
    typeTransection = ""
    name = ""
    output = []
    skip = False
    for line in reader:
        if skip: 
            skip = False
            continue
        if 'Domestic Transactions' in line:
            typeTransection = "Domestic"
            skip = True
            continue
        if 'International Transactions' in line:
            typeTransection = "International"
            skip = True
            continue
        if line == ["", "", ""]:
            continue
        if line[0] == '' and line[2] == '':
            name = line[1]
            continue
        parsed = parseHDFC(typeTransection, name, line)
        if parsed:
            output.append(parsed)

    writeCSV('HDFC-Output-Case1.csv', output)






def isempty(line):
    val = True
    for item in line:
        if item != '':
            val = False
    return val


def parseICICI(transactiontype, cardname, line ):
    
    def domesticParser():
        date = datetime.strptime(line[0], '%d-%m-%Y')
        description = line[1].split()
        location = description[-1]
        debit = line[2]
        credit = line[3]
        return standardFormat(date, line[1], debit, credit, 'INR', cardname, 'Domestic', location)

    def internationParser():
        date = datetime.strptime(line[0], '%d-%m-%Y')
        description = line[1].split()
        location = description[-2]
        currency = description[-1]
        description = ' '.join(description[:-1])
        debit = line[2]
        credit = line[3]
        return standardFormat(date, description, debit, credit, currency, cardname, 'International', location)

    return domesticParser() if transactiontype == 'Domestic' else internationParser()


def icici_parser(filename):
    thefile = open(filename, newline='', encoding='UTF-8')
    reader = csv.reader(thefile)
    typeTransaction = ''
    cardname = ''
    output = []
    skip = False
    for line in reader:
        if skip: 
            skip = False
            continue
        if 'Domestic Transactions' in line:
            typeTransaction = "Domestic"
            skip = True
            continue
        if 'International Transaction' in  line:
            typeTransaction = "International"
            skip = True
            continue
        if isempty(line):
            continue
        if line[0] == '' and line[1] == '':
            cardname = line[2]
            continue
        
        parsed = parseICICI(typeTransaction, cardname, line)
        if parsed:
            output.append(parsed)
    writeCSV('ICICI-Output-Case2.csv', output)


def parseAXIS(transactiontype, cardname, line):
    
    def domesticParser():
        date = datetime.strptime(line[0], '%d-%m-%Y')
        debit = line[1]
        credit = line[2]
        description = line[3].split()
        location = description[-1]
        return standardFormat(date, line[3], debit, credit, 'INR', cardname, 'Domestic', location)
    
    def internationParser():
        date = datetime.strptime(line[0], '%d-%m-%Y')
        description = line[3].split()
        location = description[-2]
        currency = description[-1]
        description = ' '.join(description[:-1])
        debit = line[1]
        credit = line[2]
        return standardFormat(date, description, debit, credit, currency, cardname, 'International', location)

    return domesticParser() if transactiontype == 'Domestic' else internationParser()


def axis_parser(filename):
    thefile = open(filename, newline='', encoding='UTF-8')
    reader = csv.reader(thefile)
    typeTransaction = ''
    cardname = ''
    skip = False
    output = []

    for line in reader:
        if skip: 
            skip = False
            continue
        if 'Domestic Transactions' in line:
            typeTransaction = "Domestic"
            skip = True
            continue
        if 'International Transaction' in  line:
            typeTransaction = "International"
            skip = True
            continue
        if isempty(line):
            continue

        if line[0] == '' and line[1] == '':
            cardname = line[2]
            continue

        if([x.strip() for x in line] == ['Date', 'Debit', 'Credit', 'Transaction Details']):
            continue
        parsed = parseAXIS(typeTransaction, cardname, line)
        
        if parsed:
            output.append(parsed)
    
    writeCSV('AXIS-Output-Case3.csv', output)


def parserIDFC(typeTransaction, cardname, line):

    def domesticParser():
        date = datetime.strptime(line[1], '%d-%m-%Y')
        des = line[0].strip()
        debit = 0
        credit = 0
        if len(line[2].split(' ')) == 2:
            credit = line[2].split(' ')[0]
        else:
            debit = line[2]
        location = des.split()[-1]
        return standardFormat(date, des, debit, credit, 'INR', cardname, 'Domestic', location )

    def internationParser():
        date = datetime.strptime(line[1], '%d-%m-%Y')
        des = line[0].strip()
        debit = 0
        credit = 0
        if len(line[2].split(' ')) == 2:
            credit = line[2].split(' ')[0]
        else:
            debit = line[2]
        location = des.split()[-2]
        currency = des.split()[-1]

        des = ' '.join(des.split()[:-1])
        return standardFormat(date, des, debit, credit, currency, cardname, 'International', location)

    return domesticParser() if typeTransaction == 'Domestic' else internationParser()

def idfc_parser(filename):
    thefile = open(filename, newline='', encoding='UTF-8')
    reader = csv.reader(thefile)
    typeTransaction = ''
    cardname = ''
    output = []
    
    for line in reader:
        if 'Domestic Transactions' in line:
            typeTransaction = "Domestic"
            continue
        if 'International Transaction' in  line:
            typeTransaction = "International"
            continue
        if isempty(line):
            continue
        if [x.strip() for x in line] == ['Transaction Details', 'Date', 'Amount']:
            continue
        if line[0] == '' and line[2] == '':
            cardname = line[1]
            continue
        parsed = parserIDFC(typeTransaction, cardname, line)
        
        if parsed:
            output.append(parsed)
    writeCSV('IDFC-Output-Case4.csv', output)

hdfcParser('Interview_Fresher_Any_Language/HDFC-Input-Case1.csv')
icici_parser('Interview_Fresher_Any_Language/ICICI-Input-Case2.csv')
axis_parser('Interview_Fresher_Any_Language/Axis-Input-Case3.csv')
idfc_parser('Interview_Fresher_Any_Language/IDFC-Input-Case4.csv')


