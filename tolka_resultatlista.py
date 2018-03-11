import pandas as pd
import csv

def parse_TimeSchedule_element(line):
    element = {}
    trick_section = line[0].split()
    element["order"] = int(trick_section[0])
    element["trick"] = trick_section[1]
    if len(trick_section) == 3:
        element["base"]  = float(trick_section[2].replace(",","."))
    elif trick_section[3] == "x" :
        element["base"]  = float(trick_section[2].replace(",","."))
    elif trick_section[3] == "e" :
        element["trick"] += trick_section[2] 
        element["base"]  = float(trick_section[4].replace(",","."))
    else:
        element["base"]  = float(trick_section[3].replace(",","."))
    
    if trick_section[2] == "!":
        element["trick"] +="!"

    element["GOE"] = float(line[1].replace(",","."))
    if element["base"] > 0:
        for judge,score in enumerate(line[2:-2]):
            element["J"+str(judge+1)] = int(score)
    element["score"] = float(line[-1].replace(",","."))
    return element

def tolka_TimeSchedule_resultat(filnamn):

    with open(filnamn,"r") as fil:
        lines = fil.readlines()

    skaters = []
    skater  = {}
    elements = {}

    lines = iter(lines)

    for line in lines:
        words = line.split(",")

        if "COMPETITION" in words[0]:
            skater["competition"] = words[0].split(":")[-1].lower().strip()
            continue
        if "CATEGORY" in words[0]:
            skater["category"] = words[0].split(":")[-1].strip()
            skater["part"] = words[1].strip()
            continue
        if "NAME START" in words[0]:
            words = next(lines).split(",")
            words = words[0].split()
            skater["placed"] = int(words[0])
            skater["startpos"] = int(words[-1])
            skater["name"] = " ".join(words[1:-1]).strip()
            
            words = next(lines).split(",")
            skater["club"] = words[0].strip()

            words = next(lines).split(",")
            skater["total"] = float( ".".join(words[3:5]).split('"')[1] )
            skater["element score"] = float( ".".join(words[6:8]).split('"')[1] )
            skater["pc score"] = float( ".".join(words[8:10]).split('"')[1] )

            continue
        if "EXECUTED" in words[0]:
            elements = []
            element  = {}
            for line in lines:
                element_line = next( csv.reader([line]) )
                # Line after last element has lots of spaces
                # tabula makes this into empty strings in the middle 
                # of a row. test for empty by joining them up 
                # and checking if the result is empty
                if  "".join(element_line[2:7]) == "":
                    skater["base score"] = float(element_line[0].replace(",","."))
                    skater["elements"] = elements
                    elements = {}
                    break
                element = parse_TimeSchedule_element(element_line)
                elements.append(element)
        if "COMPONENTS" in words[0]:
            components = {}
            line = next(lines)
            component_line = next( csv.reader([line]) )
            # Extra ugly hack to handle "Skating skills", don't want to do better atm
            component, factor = component_line[0][:-4], component_line[0][-4:] 
            components[component] = {
                "scores": [float(score.replace(",",".")) for score in component_line[1:-1] if score != "" ],
                "factor": float(factor.replace(",",".")) }

            for line in lines:
                component_line = next( csv.reader([line]) )
                if "".join(component_line[2:7]) == "":
                    skater["components"] =  components
                    components = {}
                    break
                component, factor = component_line[0].split()
                components[component] = {
                    "scores": [float(score.replace(",",".")) for score in component_line[1:-1] if score != "" ],
                    "factor": float(factor.replace(",",".")) }
        if "DEDUCTIONS" in words[0]:
            deductions = []
            for line in lines:
                words = line.split(",")
                if "JUDGES" in words[0]:
                    break

                deductions.append(words[0])

            skater["deductions"] = deductions
            skaters.append(skater)
            skater = {}

    return skaters


def parse_ISUCalcFS_element(line):
    element = {}
    
    element["order"] = int(line[0])
    line = line[1:]
    print(line)
    
    trick = []
    for ch in line[0]:
        pass
        #if  ch 

    if False:
        
        xpos = 2
        jpos = 3
        trick_section = line[1].split()
        print(trick_section, len(trick_section))
        element["order"] = int(line[0])
        element["trick"] = trick_section[0]
        if len(trick_section) == 1:
            element["base"] = float(line[2])
        elif len(trick_section) == 2:
            if "<" in line[1]: 
                element["base"] = float(line[2].replace(",","."))
                xpos = 3
                jpos = 4
            elif "*" in line[1]:
                element["base"] = float(line[2].replace(",","."))
                xpos = 3
                jpos = 4
            elif "e" in line[1]:
                element["base"] = float(line[2].replace(",","."))
                xpos = 3
                jpos = 4
            elif "!" in line[1]:
                element["base"] = float(line[2].replace(",","."))
            else:
                element["base"] = float(trick_section[1].replace(",","."))

        elif len(trick_section) == 3:
            element["base"] = float(trick_section[2].replace(",","."))
            #if "<" in trick_section[1]:
            #    element["base"]  = float(trick_section[2].replace(",","."))
            #elif trick_section[2] == "e" :
            #    element["trick"] += trick_section[2] 
            #    element["base"]  = float(trick_section[4].replace(",","."))
            #else:
        
    #    if trick_section[1] == "!":
    #        element["trick"] +="!"
        
        if "x" in line[xpos]:
            element["late"] =True
            element["GOE"] = line[2].split()[-1] 
            element["GOE"] = float(element["GOE"].replace(",","."))
        else:
            element["GOE"] = float(line[2].replace(",","."))

        if element["base"] > 0:        
            for judge,score in enumerate(line[jpos:-1]):
                if score == "":
                    break
                element["J"+str(judge+1)] = int(score)
        element["score"] = float(line[-1].replace(",","."))
    return element

def tolka_ISUCalcFs_resultat(filnamn):

    with open(filnamn,"r") as fil:
        lines = fil.readlines()

    skaters = []
    skater  = {}
    elements = {}

    lines = iter(lines)

    for line in lines:
        words = line.split(",")
        if "Rank" in words[0]:
            next(lines)
            line = csv.reader( [next(lines)] ) 
            line = list(line)
            skater["placed"],skater["name"],skater["nation"],skater["startpos"],skater["TSS"],skater["TES"],skater["PCS"],skater["deductions"] = line[0]
            continue
        if "CATEGORY" in words[0]:
            skater["category"] = words[0].split(":")[-1].strip()
            skater["part"] = words[1].strip()
            continue
        if "#" in words[0]:
            elements = []
            element  = {}
            for line in lines:
                element_line = next( csv.reader([line]) )
                # Line after last element has lots of spaces
                # tabula makes this into empty strings in the middle 
                # of a row. test for empty by joining them up 
                # and checking if the result is empty
                if  "".join(element_line[3:12]) == "":
                    if element_line[1] != "":
                        skater["base score"] = float(element_line[1].replace(",","."))
                    else:
                        skater["base score"] = float(element_line[2].replace(",","."))

                    skater["elements"] = elements
                    elements = {}
                    break
                element = parse_ISUCalcFS_element(element_line)
                elements.append(element)
        if "COMPONENTS" in words[0]:
            components = {}
            line = next(lines)
            component_line = next( csv.reader([line]) )
            # Extra ugly hack to handle "Skating skills", don't want to do better atm
            component, factor = component_line[0][:-4], component_line[0][-4:] 
            components[component] = {
                "scores": [float(score.replace(",",".")) for score in component_line[1:-1] if score != "" ],
                "factor": float(factor.replace(",",".")) }

            for line in lines:
                component_line = next( csv.reader([line]) )
                if "".join(component_line[2:7]) == "":
                    skater["components"] =  components
                    components = {}
                    break
                component, factor = component_line[0].split()
                components[component] = {
                    "scores": [float(score.replace(",",".")) for score in component_line[1:-1] if score != "" ],
                    "factor": float(factor.replace(",",".")) }
        if "DEDUCTIONS" in words[0]:
            deductions = []
            for line in lines:
                words = line.split(",")
                if "JUDGES" in words[0]:
                    break

                deductions.append(words[0])

            skater["deductions"] = deductions
            skaters.append(skater)
            skater = {}

    return skaters


if __name__ == "__main__":

    filnamn = "tabula-SkateMalmo2018-korta.csv"
    skaters = tolka_ISUCalcFs_resultat(filnamn)

#   filnamn = "tabula-Senior_A_Damer_Korta_Örebro.csv"
#   skaters = tolka_TimeSchedule_resultat(filnamn)
