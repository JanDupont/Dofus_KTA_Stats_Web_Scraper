from helium import *
import pandas as pd
import time

dofusClasses = ["cra", "ecaflip", "eliotrope", "eniripsa", "enutrof", "feca", "huppermage", "iop", "osamodas",
                "pandawa", "rogue", "sacrier", "sadida", "sram", "foggernaut", "xelor", "masqueraider", "ouginak"]

start_chrome(url=None, headless=False)

class Match:
    A_Team: str
    A_Bans: list[str]
    A_Picks: list[str]
    B_Team: str
    B_Bans: list[str]
    B_Picks: list[str]
    Winner_Team: str
    def __init__(
            self, A_Team: str, A_Bans: list[str],
            A_Picks: list[str],
            B_Team: str, B_Bans: list[str],
            B_Picks: list[str]) -> None:
        self.A_Team = A_Team
        self.A_Bans = A_Bans
        self.A_Picks = A_Picks
        self.B_Team = B_Team
        self.B_Bans = B_Bans
        self.B_Picks = B_Picks

def dismissCookies():
    click("Close")
def goBack():
    get_driver().back();
def showAllRoundMatches():
    if Text("16").exists():
        click("16")
        click("All")
    elif Text("All").exists():
        click("All")
        click("16")
        click("16")
        click("All")

def getDofusClassName(classNr: str):
    return dofusClasses[int(classNr.split("-")[1])-1]

def analyzeDraft(draftURL: str):
    helium.go_to(draftURL)
    divs = find_all(S(".ban-card"))
    # bans
    bansA = []
    bansB = []
    for div in divs:
        if len(bansA) < 4:
            bansA.append(getDofusClassName(div.web_element.get_attribute("class").split(" ")[1]))
        else:
            bansB.append(getDofusClassName(div.web_element.get_attribute("class").split(" ")[1]))
    
    # TODO: picks

    
    ####################################################### TODO: move to bottom 
    # generate excel
    data = {"bansA": bansA, "bansB": bansB}
    df = pd.DataFrame(data)
    df.to_excel(r'.\export_dataframe.xlsx', index=False)
    #######################################################

    # TODO: return data instead of generating excel


tournamentURL = r"https://ktarena.com/en/207-dofus-world-cup"
helium.go_to(tournamentURL)
time.sleep(1)
dismissCookies()
click(S("#head_matchs"))
click(S("#head_matchs_427"))
allMatches = []
highestRoundID = 1750
rounds = 13
# for every round:
for i in range(rounds):
    helium.go_to(r"https://ktarena.com/en/207-dofus-world-cup/matches/" + str(highestRoundID - i))
    time.sleep(1)
    showAllRoundMatches()
    roundMatchesCount = len(find_all(S(".match")))

    # for each match
    for index in range(roundMatchesCount):
        rm = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index + 1) + ") > td > div"))[0]
        click(rm)
        time.sleep(0.1)
        draftLink = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) + ") > td > div > div.games > div > div.actions > div:nth-child(3) > a"))[0].web_element.get_attribute("href")
        # map
        draftMap = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) + ") > td > div > div.games > div > div.actions > div.map"))[0].web_element.text
        # team names
        A_Name = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) + ") > td > div > div.head > div:nth-child(2) > span.name > a"))[0].web_element.text
        B_Name = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) + ") > td > div > div.head > div:nth-child(4) > span.name > a"))[0].web_element.text
        # winner
        winner = None
        winIndicatorA = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) + ") > td > div > div.head > div:nth-child(2) > span.score"))[0].web_element.get_attribute("class").split(" ")[1]
        winIndicatorB = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) + ") > td > div > div.head > div:nth-child(4) > span.score"))[0].web_element.get_attribute("class").split(" ")[1]
        if winIndicatorA == "win": winner = "A"
        elif winIndicatorB == "win": winner = "B"
        else: winner = "draw"
        print(draftMap, A_Name, B_Name, winner)
        # analyze draft (picks, bans)
        analyzeDraft(str(draftLink)) # TODO: get the draft data and save in Match class instance
        goBack()
        showAllRoundMatches()
        time.sleep(1)
        
    
    
# generate excel 

#get_driver().quit()