from helium import *
import pandas as pd
import time

dofusClasses = ["cra", "ecaflip", "eliotrope", "eniripsa", "enutrof", "feca", "huppermage", "iop", "osamodas",
                "pandawa", "rogue", "sacrier", "sadida", "sram", "foggernaut", "xelor", "masqueraider", "ouginak"]

start_chrome(url=None, headless=False)


class Match:
    Round: int
    A_Team: str
    A_Bans: list[str]
    A_Picks: list[str]
    B_Team: str
    B_Bans: list[str]
    B_Picks: list[str]
    Winner_Team: str
    Map: str

    def __init__(
            self, Round: int, A_Team: str, A_Bans: list[str],
            A_Picks: list[str],
            B_Team: str, B_Bans: list[str],
            B_Picks: list[str], Winner, Map) -> None:
        self.Round = Round
        self.A_Team = A_Team
        self.A_Bans = A_Bans
        self.A_Picks = A_Picks
        self.B_Team = B_Team
        self.B_Bans = B_Bans
        self.B_Picks = B_Picks
        self.Winner_Team = Winner
        self.Map = Map


def dismissCookies():
    click("Close")

def goBack():
    get_driver().back()

def showAllRoundMatches():
    time.sleep(0.3)
    scroll_up(10000)
    picker = find_all(S(".selectric"))[1]
    click(picker)
    click("48")
    click(picker)
    click("All")

def getDofusClassName(classNr: str):
    return dofusClasses[int(classNr.split("-")[1])-1]

def analyzeDraft(draftURL: str):
    helium.go_to(draftURL)

    banDivs = find_all(S(".ban-card"))
    bansA = []
    bansB = []
    for div in banDivs:
        splitted = div.web_element.get_attribute("class").split(" ")
        if len(bansA) < 4:
            bansA.append(getDofusClassName(splitted[1]) if len(splitted)>1 else "")
        else:
            bansB.append(getDofusClassName(splitted[1]) if len(splitted)>1 else "")

    pickDivs = find_all(S(".pick-card"))
    picksA = []
    picksB = []
    for div in pickDivs:
        splitted = div.web_element.get_attribute("class").split(" ")
        if len(picksA) < 3:
            picksA.append(getDofusClassName(splitted[1]) if len(splitted)>1 else "")
        else:
            picksB.append(getDofusClassName(splitted[1]) if len(splitted)>1 else "")

    return bansA, bansB, picksA, picksB


tournamentURL = r"https://ktarena.com/en/207-dofus-world-cup"
helium.go_to(tournamentURL)
time.sleep(0.5)
dismissCookies()
click(S("#head_matchs"))
click(S("#head_matchs_427"))
allMatches = []
highestRoundID = 1750
rounds = 13

# for every round:
for i in range(1): # rounds
    helium.go_to(r"https://ktarena.com/en/207-dofus-world-cup/matches/" + str(highestRoundID - i))
    time.sleep(1)
    showAllRoundMatches()
    roundMatchesCount = len(find_all(S(".match")))

    # for each match
    for index in range(roundMatchesCount):
        rm = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index + 1) + ") > td > div"))[0]
        click(rm)
        time.sleep(0.1)
        draftLink = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(
            index+1) + ") > td > div > div.games > div > div.actions > div:nth-child(3) > a"))[0].web_element.get_attribute("href")

        draftMap = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) +
                            ") > td > div > div.games > div > div.actions > div.map"))[0].web_element.text

        A_Name = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) +
                          ") > td > div > div.head > div:nth-child(2) > span.name > a"))[0].web_element.text
        B_Name = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) +
                          ") > td > div > div.head > div:nth-child(4) > span.name > a"))[0].web_element.text

        winner = None
        winIndicatorA = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(
            index+1) + ") > td > div > div.head > div:nth-child(2) > span.score"))[0].web_element.get_attribute("class").split(" ")[1]
        winIndicatorB = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(
            index+1) + ") > td > div > div.head > div:nth-child(4) > span.score"))[0].web_element.get_attribute("class").split(" ")[1]
        if winIndicatorA == "win":
            winner = "A"
        elif winIndicatorB == "win":
            winner = "B"
        else:
            winner = "draw"
        
        A_Bans = []
        B_Bans = []
        A_Picks = []
        B_Picks = []
        if(winner != "draw" and draftLink):
            A_Bans, B_Bans, A_Picks, B_Picks = analyzeDraft(str(draftLink))
            goBack()

        newMatch = Match(13-int(i), A_Name, A_Bans, A_Picks, B_Name, B_Bans, B_Picks, winner, draftMap)
        allMatches.append(newMatch)
        
        showAllRoundMatches()
        time.sleep(1)


def generateExcel():
    print("GENERATE EXCEL")
    rounds =  [item.Round for item in allMatches]
    maps = [item.Map for item in allMatches]
    winners = [item.Winner_Team for item in allMatches]
    ATeams = [item.A_Team for item in allMatches]
    APick1s = [item.A_Picks[0] if len(item.A_Picks)==3 else "" for item in allMatches] 
    APick2s = [item.A_Picks[1] if len(item.A_Picks)==3 else "" for item in allMatches]
    APick3s = [item.A_Picks[2] if len(item.A_Picks)==3 else "" for item in allMatches]
    ABan1s = [item.A_Bans[0] if len(item.A_Bans)==4 else "" for item in allMatches]
    ABan2s = [item.A_Bans[1] if len(item.A_Bans)==4 else "" for item in allMatches]
    ABan3s = [item.A_Bans[2] if len(item.A_Bans)==4 else "" for item in allMatches]
    ABan4s = [item.A_Bans[3] if len(item.A_Bans)==4 else "" for item in allMatches]
    BTeams = [item.B_Team for item in allMatches]
    BPick1s = [item.B_Picks[0] if len(item.B_Picks)==3 else "" for item in allMatches]
    BPick2s = [item.B_Picks[1] if len(item.B_Picks)==3 else "" for item in allMatches]
    BPick3s = [item.B_Picks[2] if len(item.B_Picks)==3 else "" for item in allMatches]
    BBan1s = [item.B_Bans[0] if len(item.B_Bans)==4 else "" for item in allMatches]
    BBan2s = [item.B_Bans[1] if len(item.B_Bans)==4 else "" for item in allMatches]
    BBan3s = [item.B_Bans[2] if len(item.B_Bans)==4 else "" for item in allMatches]
    BBan4s = [item.B_Bans[3] if len(item.B_Bans)==4 else "" for item in allMatches]

    data = {
        "Round": rounds, 
        "Map": maps, 
        "Winner": winners, 
        "ATeam": ATeams, 
        "APick1": APick1s, 
        "APick2": APick2s, 
        "APick3": APick3s, 
        "ABan1": ABan1s, 
        "ABan2": ABan2s, 
        "ABan3": ABan3s, 
        "ABan4": ABan4s,
        "BTeam": BTeams, 
        "BPick1": BPick1s, 
        "BPick2": BPick2s, 
        "BPick3": BPick3s, 
        "BBan1": BBan1s, 
        "BBan2": BBan2s, 
        "BBan3": BBan3s, 
        "BBan4": BBan4s
    }
    df = pd.DataFrame(data)
    df.to_excel(r'.\export_dataframe.xlsx', index=False)

generateExcel()
get_driver().quit()
