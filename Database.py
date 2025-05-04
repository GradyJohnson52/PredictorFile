import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import argparse

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)



parser = argparse.ArgumentParser()
parser.add_argument("-q", help="for search term")


args = parser.parse_args()

urlRD = f"https://www.teamrankings.com/college-football/stat/opponent-rushing-yards-per-game"
urlPD = f"https://www.teamrankings.com/college-football/stat/opponent-passing-yards-per-game"
urlRO = f"https://www.teamrankings.com/college-football/stat/rushing-yards-per-game"
urlPO = f"https://www.teamrankings.com/college-football/stat/passing-yards-per-game"
urlSD = f"https://www.teamrankings.com/college-football/stat/opponent-points-per-game"
urlSO = f"https://www.teamrankings.com/college-football/stat/points-per-game"
urlTR = f"https://www.teamrankings.com/ncf/trends/win_trends/"
urlTD = f"https://www.teamrankings.com/college-football/stat/takeaways-per-game"
urlTO = f"https://www.teamrankings.com/college-football/stat/giveaways-per-game"
urlPR = f"https://www.teamrankings.com/college-football/ranking/predictive-by-other"
urlHome = f"https://www.teamrankings.com/college-football/ranking/home-by-other"
urlAway = f"https://www.teamrankings.com/college-football/ranking/away-by-other"
urlSOS = f"https://www.teamrankings.com/college-football/ranking/schedule-strength-by-other"
'''urlROF = f"https://www.teamrankings.com/college-football/stat/rushing-yards-per-game?date=2024-01-09"
urlwp23 = f"https://www.teamrankings.com/ncf/trends/win_trends/?range=yearly_2023"
urlPOF = f"https://www.teamrankings.com/college-football/stat/passing-yards-per-game?date=2024-01-09"
urlRDF = f"https://www.teamrankings.com/college-football/stat/opponent-rushing-yards-per-game?date=2024-01-09"
urlPDF = f"https://www.teamrankings.com/college-football/stat/opponent-passing-yards-per-game?date=2024-01-09"
urlTOF = f"https://www.teamrankings.com/college-football/stat/giveaways-per-game?date=2024-01-09"
urlTDF = f"https://www.teamrankings.com/college-football/stat/takeaways-per-game?date=2024-01-09"
urlSOF = f"https://www.teamrankings.com/college-football/stat/points-per-game?date=2024-01-09"
urlSDF = f"https://www.teamrankings.com/college-football/stat/opponent-points-per-game?date=2024-01-09"'''




RD = requests.get(urlRD)
print(RD)

PD = requests.get(urlPD)

RO = requests.get(urlRO)

PO = requests.get(urlPO)

SD = requests.get(urlSD)

SO = requests.get(urlSO)

TD = requests.get(urlTD)

TO = requests.get(urlTO)

TR = requests.get(urlTR)

PR = requests.get(urlPR)

Home = requests.get(urlHome)

Away = requests.get(urlAway)

SOS = requests.get(urlSOS)


'''ROF = requests.get(urlROF)

wp23 = requests.get(urlwp23)

POF = requests.get(urlPOF)

PDF = requests.get(urlPDF)

RDF = requests.get(urlRDF)

SOF = requests.get(urlSOF)

SDF = requests.get(urlSDF)

TOF = requests.get(urlTOF)

TDF = requests.get(urlTDF)'''


soupRD = bs(RD.text, "html.parser")

soupPD = bs(PD.text, "html.parser")

soupRO = bs(RO.text, "html.parser")

soupPO = bs(PO.text, "html.parser")

soupSD = bs(SD.text, "html.parser")

soupSO = bs(SO.text, "html.parser")

soupTD = bs(TD.text, "html.parser")

soupTO = bs(TO.text, "html.parser")

soupTR = bs(TR.text, "html.parser")

soupPR = bs(PR.text, "html.parser")

soupHome = bs(Home.text, "html.parser")

soupAway = bs(Away.text, "html.parser")

soupSOS = bs(SOS.text, "html.parser")


'''soupROF = bs(ROF.text, "html.parser")

soupPOF = bs(POF.text, "html.parser")

soupRDF = bs(RDF.text, "html.parser")

soupPDF = bs(PDF.text, "html.parser")

soupSOF = bs(SOF.text, "html.parser")

soupSDF = bs(SDF.text, "html.parser")

soupTOF = bs(TOF.text, "html.parser")

soupTDF = bs(TDF.text, "html.parser")

soupwp23 = bs(wp23.text, "html.parser")'''

RD_scrape = soupRD.find("table", {'class': 'tr-table'})
RDR =RD_scrape.find_all('tr')
RDdata =[]
for row in RDR:
    cells = row.find_all('td')  # Use 'th' for header cells
    RDdata.append([cell.text.strip() for cell in cells])
RDT=pd.DataFrame(RDdata)
RD_Table = RDT.iloc[1:, [1, 2]]
RD_Table.to_csv('RD_Table.csv', index=False)



PD_scrape = soupPD.find("table", {'class': 'tr-table'})
PDR =PD_scrape.find_all('tr')
PDdata = []
for row in PDR:
    cells = row.find_all('td')  # Use 'th' for header cells
    PDdata.append([cell.text.strip() for cell in cells])
PDT=pd.DataFrame(PDdata)
PD_Table = PDT.iloc[1:, [1, 2]]
PD_Table.to_csv('PD_Table.csv', index=False)


RO_scrape = soupRO.find("table", {'class': 'tr-table'})
ROR =RO_scrape.find_all('tr')
ROdata = []
for row in ROR:
    cells = row.find_all('td')  # Use 'th' for header cells
    ROdata.append([cell.text.strip() for cell in cells])
ROT=pd.DataFrame(ROdata)
RO_Table = ROT.iloc[1:, [1, 2]]
RO_Table.to_csv('RO_Table.csv', index=False)



PO_scrape = soupPO.find("table", {'class': 'tr-table'})
POR =PO_scrape.find_all('tr')
POdata = []
for row in POR:
    cells = row.find_all('td')  # Use 'th' for header cells
    POdata.append([cell.text.strip() for cell in cells])
POT=pd.DataFrame(POdata)
PO_Table = POT.iloc[1:, [1, 2]]
PO_Table.to_csv('PO_Table.csv', index=False)



SD_scrape = soupSD.find("table", {'class': 'tr-table'})
SDR =SD_scrape.find_all('tr')
SDdata=[]
for row in SDR:
    cells = row.find_all('td')  # Use 'th' for header cells
    SDdata.append([cell.text.strip() for cell in cells])
SDT=pd.DataFrame(SDdata)
SD_Table = SDT.iloc[1:, [1, 2]]
SD_Table.to_csv('SD_Table.csv', index=False)


SO_scrape = soupSO.find("table", {'class': 'tr-table'})
SOR =SO_scrape.find_all('tr')
SOdata=[]
for row in SOR:
    cells = row.find_all('td')  # Use 'th' for header cells
    SOdata.append([cell.text.strip() for cell in cells])
SOT=pd.DataFrame(SOdata)
SO_Table = SOT.iloc[1:, [1, 2]]
SO_Table.to_csv('SO_Table.csv', index=False)



TD_scrape = soupTD.find("table", {'class':'tr-table'})
TDR =TD_scrape.find_all('tr')
TDdata=[]
for row in TDR:
    cells = row.find_all('td')  # Use 'th' for header cells
    TDdata.append([cell.text.strip() for cell in cells])
TDT=pd.DataFrame(TDdata)
TD_Table = TDT.iloc[1:, [1, 2]]
TD_Table.to_csv('TD_Table.csv', index=False)



TO_scrape = soupTO.find("table", {'class':'tr-table' })
TOR = TO_scrape.find_all('tr')
TOdata=[]
for row in TOR:
    cells = row.find_all('td')  # Use 'th' for header cells
    TOdata.append([cell.text.strip() for cell in cells])
TOT=pd.DataFrame(TOdata)
TO_Table = TOT.iloc[1:, [1, 2]]
TO_Table.to_csv('TO_Table.csv', index=False)



TR_scrape = soupTR.find("table", {'class':'tr-table' })
TRR = TR_scrape.find_all('tr')
TRdata=[]
for row in TRR:
    cells = row.find_all('td')  # Use 'th' for header cells
    TRdata.append([cell.text.strip() for cell in cells])
TRT=pd.DataFrame(TRdata)
TR_Table = TRT.iloc[1:, [0, 2]]
TR_Table[2] = TR_Table[2].str.rstrip('%').astype('float')
TR_Table.to_csv('TR_Table.csv', index=False)

PR_scrape = soupPR.find("table", {'class':'tr-table' })
PRR = PR_scrape.find_all('tr')
PRdata = []
for row in PRR:
    cells = row.find_all('td')  
    if len(cells) > 2:  
        team_name = cells[1].find('a').text.strip()  
        rating = cells[2].text.strip()
        PRdata.append([team_name, rating])  
PRT = pd.DataFrame(PRdata, columns=['Team', 'Rating'])
PRT.to_csv('PR_Table.csv', index=False)


Home_scrape = soupHome.find("table", {'class':'tr-table' })
HomeR = Home_scrape.find_all('tr')
Home_data = []
for row in HomeR:
    cells = row.find_all('td')
    if len(cells) > 2:
        team_name = cells[1].find('a').text.strip()
        rating = cells[2].text.strip()
        Home_data.append([team_name, rating])
HomeT = pd.DataFrame(Home_data, columns=['Team', 'Rating'])
HomeT.to_csv('Home_Table.csv', index=False)

Away_scrape = soupAway.find("table", {'class':'tr-table' })
AwayR = Away_scrape.find_all('tr')
Away_data = []
for row in AwayR:
    cells = row.find_all('td')
    if len(cells) > 2:
        team_name = cells[1].find('a').text.strip()
        rating = cells[2].text.strip()
        Away_data.append([team_name, rating])
AwayT = pd.DataFrame(Away_data, columns=['Team', 'Rating'])
AwayT.to_csv('Away_Table.csv', index=False)

SOS_scrape = soupSOS.find("table", {'class':'tr-table' })
SOSR = SOS_scrape.find_all('tr')
SOS_data = []
for row in SOSR:
    cells = row.find_all('td')
    if len(cells) > 2:
        team_name = cells[1].find('a').text.strip()
        rating = cells[2].text.strip()
        SOS_data.append([team_name, rating])
SOST = pd.DataFrame(SOS_data, columns=['Team', 'Rating'])
SOST.to_csv('SOS_Table.csv', index=False)



'''ROF_scrape = soupROF.find("table", {'class': 'tr-table'})
ROFR =ROF_scrape.find_all('tr')
ROFdata =[]
for row in ROFR:
    cells = row.find_all('td')  # Use 'th' for header cells
    ROFdata.append([cell.text.strip() for cell in cells])
ROFT=pd.DataFrame(ROFdata)
ROF_Table = ROFT.iloc[:, [1, 2]]
ROF_Table =  ROF_Table.iloc[1:]
ROF_Table.to_csv('ROF_Table.csv', index=False)


POF_scrape = soupPOF.find("table", {'class': 'tr-table'})
POFR =POF_scrape.find_all('tr')
POFdata =[]
for row in POFR:
    cells = row.find_all('td')  # Use 'th' for header cells
    POFdata.append([cell.text.strip() for cell in cells])
POFT=pd.DataFrame(POFdata)
POF_Table = POFT.iloc[:, [1, 2]]
POF_Table =  POF_Table.iloc[1:]
POF_Table.to_csv('POF_Table.csv', index=False)


RDF_scrape = soupRDF.find("table", {'class': 'tr-table'})
RDFR =RDF_scrape.find_all('tr')
RDFdata =[]
for row in RDFR:
    cells = row.find_all('td')  # Use 'th' for header cells
    RDFdata.append([cell.text.strip() for cell in cells])
RDFT=pd.DataFrame(RDFdata)
RDF_Table = RDFT.iloc[:, [1, 2]]
RDF_Table =  RDF_Table.iloc[1:]
RDF_Table.to_csv('RDF_Table.csv', index=False)


PDF_scrape = soupPDF.find("table", {'class': 'tr-table'})
PDFR =PDF_scrape.find_all('tr')
PDFdata =[]
for row in PDFR:
    cells = row.find_all('td')  # Use 'th' for header cells
    PDFdata.append([cell.text.strip() for cell in cells])
PDFT=pd.DataFrame(PDFdata)
PDF_Table = PDFT.iloc[:, [1, 2]]
PDF_Table =  PDF_Table.iloc[1:]
PDF_Table.to_csv('PDF_Table.csv', index=False)


SOF_scrape = soupSOF.find("table", {'class': 'tr-table'})
SOFR =SOF_scrape.find_all('tr')
SOFdata =[]
for row in SOFR:
    cells = row.find_all('td')  # Use 'th' for header cells
    SOFdata.append([cell.text.strip() for cell in cells])
SOFT=pd.DataFrame(SOFdata)
SOF_Table = SOFT.iloc[:, [1, 2]]
SOF_Table =  SOF_Table.iloc[1:]
SOF_Table.to_csv('SOF_Table.csv', index=False)


SDF_scrape = soupSDF.find("table", {'class': 'tr-table'})
SDFR =SDF_scrape.find_all('tr')
SDFdata =[]
for row in SDFR:
    cells = row.find_all('td')  # Use 'th' for header cells
    SDFdata.append([cell.text.strip() for cell in cells])
SDFT=pd.DataFrame(SDFdata)
SDF_Table = SDFT.iloc[:, [1, 2]]
SDF_Table =  SDF_Table.iloc[1:]
SDF_Table.to_csv('SDF_Table.csv', index=False)


TOF_scrape = soupTOF.find("table", {'class': 'tr-table'})
TOFR =TOF_scrape.find_all('tr')
TOFdata =[]
for row in TOFR:
    cells = row.find_all('td')  # Use 'th' for header cells
    TOFdata.append([cell.text.strip() for cell in cells])
TOFT=pd.DataFrame(TOFdata)
TOF_Table = TOFT.iloc[:, [1, 2]]
TOF_Table =  TOF_Table.iloc[1:]
TOF_Table.to_csv('TOF_Table.csv', index=False)


TDF_scrape = soupTDF.find("table", {'class': 'tr-table'})
TDFR =TDF_scrape.find_all('tr')
TDFdata =[]
for row in TDFR:
    cells = row.find_all('td')  # Use 'th' for header cells
    TDFdata.append([cell.text.strip() for cell in cells])
TDFT=pd.DataFrame(TDFdata)
TDF_Table = TDFT.iloc[:, [1, 2]]
TDF_Table =  TDF_Table.iloc[1:]
TDF_Table.to_csv('TDF_Table.csv', index=False)



wp23_scrape = soupwp23.find("table", {'class': 'tr-table'})
wp23R =wp23_scrape.find_all('tr')
wp23data =[]
for row in wp23R:
    cells = row.find_all('td')  # Use 'th' for header cells
    wp23data.append([cell.text.strip() for cell in cells])
wp23T=pd.DataFrame(wp23data)
wp23_Table = wp23T.iloc[1:,[0, 2]]
wp23_Table =  wp23_Table.iloc[1:]
wp23_Table[2] = wp23_Table[2].str.rstrip('%').astype('float')
wp23_Table.to_csv('wp23_Table.csv', index=False)'''