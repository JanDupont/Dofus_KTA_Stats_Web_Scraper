from helium import *
import pandas as pd
import time

dofusClasses = ["cra", "ecaflip", "eliotrope", "eniripsa", "enutrof", "feca", "huppermage", "iop", "osamodas",
                "pandawa", "rogue", "sacrier", "sadida", "sram", "foggernaut", "xelor", "masqueraider", "ouginak"]

bansAmount = 4
picksAmount = 3

start_chrome(url=None, headless=False)


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
        if len(bansA) < bansAmount:
            bansA.append(getDofusClassName(splitted[1]) if len(splitted) > 1 else "")
        else:
            bansB.append(getDofusClassName(splitted[1]) if len(splitted) > 1 else "")

    pickDivs = find_all(S(".pick-card"))
    picksA = []
    picksB = []
    for div in pickDivs:
        splitted = div.web_element.get_attribute("class").split(" ")
        if len(picksA) < picksAmount:
            picksA.append(getDofusClassName(splitted[1]) if len(splitted) > 1 else "")
        else:
            picksB.append(getDofusClassName(splitted[1]) if len(splitted) > 1 else "")

    return bansA, bansB, picksA, picksB


tournamentURL = r"https://ktarena.com/en/207-dofus-world-cup"
helium.go_to(tournamentURL)
time.sleep(0.5)
dismissCookies()
click(S("#head_matchs"))
click(S("#head_matchs_427"))
highestRoundID = 1750
rounds = 13

all_Rounds = []
all_Maps = []
all_Winners = []
all_A_Names = []
all_A_Pick_1 = []
all_A_Pick_2 = []
all_A_Pick_3 = []
all_A_Ban_1 = []
all_A_Ban_2 = []
all_A_Ban_3 = []
all_A_Ban_4 = []
all_B_Names = []
all_B_Pick_1 = []
all_B_Pick_2 = []
all_B_Pick_3 = []
all_B_Ban_1 = []
all_B_Ban_2 = []
all_B_Ban_3 = []
all_B_Ban_4 = []

allDraftLinks = []

for i in range(rounds):
    helium.go_to(r"https://ktarena.com/en/207-dofus-world-cup/matches/" + str(highestRoundID - i))
    time.sleep(0.5)
    showAllRoundMatches()
    roundMatchesCount = len(find_all(S(".match")))

    # for each match
    for index in range(roundMatchesCount):
        rm = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index + 1) + ") > td > div"))[0]
        click(rm)
        time.sleep(0.1)
        draftLink = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(
            index+1) + ") > td > div > div.games > div > div.actions > div:nth-child(3) > a"))[0].web_element.get_attribute("href")
        allDraftLinks.append(draftLink if draftLink else "")

        draftRound = rounds - int(i)
        all_Rounds.append(draftRound)

        draftMap = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) +
                            ") > td > div > div.games > div > div.actions > div.map"))[0].web_element.text
        all_Maps.append(draftMap)

        A_Name = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) +
                          ") > td > div > div.head > div:nth-child(2) > span.name > a"))[0].web_element.text
        all_A_Names.append(A_Name)
        B_Name = find_all(S("#DataTables_Table_0 > tbody > tr:nth-child(" + str(index+1) +
                          ") > td > div > div.head > div:nth-child(4) > span.name > a"))[0].web_element.text
        all_B_Names.append(B_Name)

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
        all_Winners.append(winner)

for index, link in enumerate(allDraftLinks):
    A_Bans = ["", "", "", ""]
    B_Bans = ["", "", "", ""]
    A_Picks = ["", "", ""]
    B_Picks = ["", "", ""]
    if(all_Winners[index] != "draw" and link != "" and link != None):
        A_Bans, B_Bans, A_Picks, B_Picks = analyzeDraft(str(link))

    all_A_Pick_1.append(A_Picks[0] if len(A_Picks) == picksAmount else "")
    all_A_Pick_2.append(A_Picks[1] if len(A_Picks) == picksAmount else "")
    all_A_Pick_3.append(A_Picks[2] if len(A_Picks) == picksAmount else "")
    all_A_Ban_1.append(A_Bans[0] if len(A_Bans) == bansAmount else "")
    all_A_Ban_2.append(A_Bans[1] if len(A_Bans) == bansAmount else "")
    all_A_Ban_3.append(A_Bans[2] if len(A_Bans) == bansAmount else "")
    all_A_Ban_4.append(A_Bans[3] if len(A_Bans) == bansAmount else "")

    all_B_Pick_1.append(B_Picks[0] if len(B_Picks) == picksAmount else "")
    all_B_Pick_2.append(B_Picks[1] if len(B_Picks) == picksAmount else "")
    all_B_Pick_3.append(B_Picks[2] if len(B_Picks) == picksAmount else "")
    all_B_Ban_1.append(B_Bans[0] if len(B_Bans) == bansAmount else "")
    all_B_Ban_2.append(B_Bans[1] if len(B_Bans) == bansAmount else "")
    all_B_Ban_3.append(B_Bans[2] if len(B_Bans) == bansAmount else "")
    all_B_Ban_4.append(B_Bans[3] if len(B_Bans) == bansAmount else "")


def generateExcel():
    print("GENERATE EXCEL")
    data = {
        "Round": all_Rounds,
        "Map": all_Maps,
        "Winner": all_Winners,
        "ATeam": all_A_Names,
        "APick1": all_A_Pick_1,
        "APick2": all_A_Pick_2,
        "APick3": all_A_Pick_3,
        "ABan1": all_A_Ban_1,
        "ABan2": all_A_Ban_2,
        "ABan3": all_A_Ban_3,
        "ABan4": all_A_Ban_4,
        "BTeam": all_B_Names,
        "BPick1": all_B_Pick_1,
        "BPick2": all_B_Pick_2,
        "BPick3": all_B_Pick_3,
        "BBan1": all_B_Ban_1,
        "BBan2": all_B_Ban_2,
        "BBan3": all_B_Ban_3,
        "BBan4": all_B_Ban_4
    }
    df = pd.DataFrame(data)
    df.to_excel(r'.\KTA_stats.xlsx', index=False)


generateExcel()
get_driver().quit()
