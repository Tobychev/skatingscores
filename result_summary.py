import numpy as np
import pandas as pd
import matplotlib.pyplot as pl 
import seaborn as sb

import tolka_resultatlista as tres

if False:
    filnamn = "tabula-Senior_A_Damer_Korta_Örebro.csv"
    skaters = tres.tolka_TimeSchedule_resultat(filnamn)

filnamn = "tabula-SkateMalmo2018-korta.csv"
skaters = tres.tolka_ISUCalcFs_resultat(filnamn)



