import pandas as pd
import matplotlib.pyplot as pl
import matplotlib.colors as col

# För fixande av importerade html tabell
html_table_names = ['Name', 'TSS', 'TES', "nan", 'PCS', 'SS', 'TR', 'PE', 'CO', 'IN', 'Deduction', 'StN']

#Skate malmö korta
korta = pd.read_html("http://www.skatesweden.wehost.se/17-18/Interclub/Skate_Malmo/html/SEG013.HTM",header=0,index_col=0,decimal=".")
korta = korta[0]

korta.columns = html_table_names

fig, ax = pl.subplots()
ax.scatter(korta.TES-korta.Deduction, korta.PCS, c = korta.TSS, norm=col.Normalize(10,30))
pl.xlabel("TES")
pl.ylabel("PCS")

for i,name in enumerate(korta.Name):
    skater = name.split()[0] +" "+ name.split()[1][:1]
    ax.annotate( skater , ( korta.TES.iloc[i]-korta.Deduction.iloc[i] +.3, korta.PCS.iloc[i]) )

pl.show()
