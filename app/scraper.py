import requests
from bs4 import BeautifulSoup
import openpyxl

from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

def generateRollNos(start, end):
    base = start[:-2]
    start = start[-2:]
    end = end[-2:]

    while start <= end:
        yield base + start
        unitsPlace = (int(start[-1]) + 1) % 10
        tensPlace = start[0]
        if unitsPlace == 0:
            if tensPlace.isalpha():
                tensPlace = chr(ord(tensPlace) + 1)
            else:
                tensPlace = (int(tensPlace) + 1) % 10
                if tensPlace == 0:
                    # 99 -> A0
                    tensPlace = 'A'
        start = str(tensPlace) + str(unitsPlace)


def getResults(resultsID, rollno):
    link = (
        f'https://svce.edu.in/results/results?table={resultsID}&roll={rollno}'
    )

    res = requests.get(link)

    return res.text

def parseHTML(html):
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.findAll('table')

    header, body = soup.findAll('table', limit=2)

    res = []
    for row in header.findAll('tr', limit=2):
        for elem in row.findAll('td'):
            res.append([elem.text])

    res.append([
        'S.No', 'Subject Code', 'Subject Name', 'Internal', 'External',
        'Total', 'Pass/Fail', 'Credits', 'Grade', 'Grade Points',
    ])

    for row in body.findAll('tr'):
        tmp = []
        for elem in row.findAll('td'):
            tmp.append(elem.text)
        if tmp:
            res.append(tmp)

    res[-2].insert(0, 'Total Marks')
    res[-1].insert(0, 'Total Credits')

    return res


def getResultsRows(resultsID, rollno):
    try:
        html = getResults(resultsID, rollno)
        rows = parseHTML(html)
    except:
        print(f'{rollno} - not found')
        return None

    return rows


def toExcel(resultsID, rollnos, filename):
    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]
    rollnos = list(rollnos)

    with ThreadPoolExecutor() as executor:
        results = executor.map(getResultsRows, repeat(resultsID), rollnos)

    for rows in results:
        if rows is None:
            continue
        
        for row in rows:
            ws.append(row)
        ws.append([])
        ws.append([])

    wb.save(filename)
    return True


def download_results(link, start, end, filename):
    resultsID = link.split('/')[-1]
    rollnos = generateRollNos(start, end)

    return toExcel(resultsID, rollnos, filename)


def main():
    resultsID = input('Enter results link: ').strip('/')[-1]

    start = input('Enter starting roll number: ').strip().upper()
    end = input('Enter ending roll no: ').strip().upper()

    filename = input('Enter file name to save: ').strip()

    rollnos = generateRollNos(start, end)
    toExcel(resultsID, rollnos, filename)


if __name__ == '__main__':
    main()
