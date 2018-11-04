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

    if len(line) == 8:
        line = line[1:]
    elif len(line) == 9:
        line = line[2:]

    element["GOE"] = float(line[0].replace(",","."))
    if element["base"] > 0:
        for judge,score in enumerate(line[1:-2]):
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
            # Handle variations in how
            # tabula splits whitespace
            if len(words) == 11:
                words = words[3:]
            elif len(words) == 12:
                words = words[4:]

            skater["TSS"] = float( ".".join(words[0:2]).split('"')[1] )
            skater["TES"] = float( ".".join(words[3:5]).split('"')[1] )
            skater["PCS"] = float( ".".join(words[5:7]).split('"')[1] )

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

def parse_ISUCalcFS_element(line,num_judges):
    element = {}

    tmp = list(
            filter(
                lambda itm: len(itm), line))
    element["order"],tmp = int(tmp[0]),tmp[1:]
    element["total"],tmp = float(tmp[-1][:-1]),tmp[:-1]

    # Test if element and base are in
    # same string, and correct
    if "." in tmp[0].split()[-1] :
        tmp = tmp[0].split() + tmp[1:]

    # If element is late, extra column has
    # been made, merge it into element name instead
    if "x" in line:
        element["executed"] = tmp[0]+" "+tmp[2]
        tmp = [tmp[1]]+tmp[3:]
    else:
        element["executed"] = tmp[0]
        tmp = tmp[1:]

    element["base"],element["GOE"],tmp = float(tmp[0]),float(tmp[1]),tmp[2:]
    element["judges"]= " ".join(tmp).split()

    try:
        element["judges"] = list(map(int,element["judges"]))
    except ValueError:
        pass
    return element

def parse_ISUCalcFS_deductions(line):
    # First is just "Deductions", last is total we already have
    words = iter(line.split(",")[1:-1])
    deductions = []

    for itm in words:
        deduction = {"type":itm[:-1]}
        if "(" in line:
            type_total = next(words).split("(")
            deduction["subtotal"] = float(type_total[0])
            deduction["count"] = int(type_total[1].split(")")[0])
        else:
            type_total = next(words)
            deduction["subtotal"] = float(type_total)

        deductions.append(deduction)

def parse_ISUCalcFS_component(line,component):
    component = {"factor":0,"scores":0}
    tmp = list(
        filter(
            lambda itm: len(itm), line))
    tmp = tmp[2:]
    tmp[-1] = tmp[-1][:-1]

    # remove any extra spaces
    # floating about
    tmp = " ".join(tmp).split()
    try:
        tmp = list(map(float,tmp))
    except ValueError:
        pass

    component["factor"],component["scores"] = tmp[0],tmp[1:]

    return component

def tolka_ISUCalcFs_resultat(filnamn,num_judges):

    with open(filnamn,"r") as fil:
        lines = fil.readlines()

    skaters = []
    skater  = {}
    elements = {}
    components = {}

    lines = iter(lines)

    for line in lines:
        words = line.split(",")
        if "Rank" in words[0]:
            next(lines)
            line = csv.reader( [next(lines)] ) 
            line = list(line)
            skater["placed"],skater["name"],skater["nation"],skater["startpos"],skater["TSS"],skater["TES"],skater["PCS"],skater["deductions"] = line[0]
            skater["placed"] = int(skater["placed"])
            skater["startpos"] = int(skater["startpos"])
            skater["deductions"] = float(skater["deductions"])
            skater["TSS"] = float(skater["TSS"])
            skater["TES"] = float(skater["TES"])
            skater["PCS"] = float(skater["PCS"])
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

                # Handle header row
                if "Elements Value" in element_line or "Value" in element_line:
                    continue
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
                element = parse_ISUCalcFS_element(element_line,num_judges)
                elements.append(element)

        if "Skating Skills" in words:
            components["Skating Skills"] = parse_ISUCalcFS_component(words,"Skating Skills")
        if "Transitions" in words:
            components["Transitions"] = parse_ISUCalcFS_component(words,"Transitions")
        if "Performance" in words:
            components["Performance"] = parse_ISUCalcFS_component(words,"Performance")
        if "Composition" in words:
            components["Composition"] = parse_ISUCalcFS_component(words,"Composition")
        if "Interpretation" in line:
            components["Interpretation"] = parse_ISUCalcFS_component(words,"Interpretation")

        if "Deductions" in words[0]:            
            skater["deductions"] = parse_ISUCalcFS_deductions(line)
            skater["components"] = components
            skaters.append(skater)
            skater = {}
            components = {}

    return skaters

if __name__ == "__main__":

#    skaters = tolka_ISUCalcFs_resultat("tabula-SkateMalmo2018-korta.csv")
    skaters = tolka_TimeSchedule_resultat("tabula-Seniorer_A_Damer_Segment_1_JD_Mariestad-2018-10-27.csv")
    print(skaters)

#   filnamn = "tabula-Senior_A_Damer_Korta_Örebro.csv"
#   skaters = tolka_TimeSchedule_resultat(filnamn)
