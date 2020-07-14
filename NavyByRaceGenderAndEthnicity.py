# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 18:51:12 2020

@author: naomi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CategoricalColorMapper, FactorRange, HoverTool, Select, Legend
from bokeh.models.widgets import Panel, Tabs
from bokeh.palettes import Viridis7, BuPu3, Oranges3, RdYlGn7, Blues7
from bokeh.layouts import widgetbox, column, row, gridplot
from bokeh.transform import dodge

def createDataList(sDF, rankNames, cat, catContent):
    valList = []
    revSDF = sDF[sDF.loc[:,cat]==catContent]
    for rankN in rankNames:
        valList.append(len(revSDF[revSDF.loc[:,'rank']==rankN]))
    return(valList)
    
def createDataListPercent(sDF, rankName, cat, catContents):
    valList = []
    revSDF = sDF[sDF.loc[:,'rank']==rankName]
    for catContent in catContents:
        valList.append(len(revSDF[revSDF.loc[:,cat]==catContent]))
    valArray = np.array(valList)  
    valArray = valArray/np.sum(valArray)*100
    return(valArray)

def createCountSource(sDF, rankNames, cat, catContents):
    data = {'rank': rankNames}
    for num, catContent in enumerate(catContents):
        localList = createDataList(sDF, rankNames, cat, catContent)
        data.update({str(num):localList}) 
    return(data)    

def createCountP(source, rankNames, colSpec, title, catContents):       
    p = figure(x_range=FactorRange(*rankNames), plot_height=370, plot_width=650,
           title=title,
           toolbar_location=None, tools="")
    for num, cat in enumerate(catContents):
        location = -0.45+(num*0.15)
        width = 0.1
        if (len(catContents) == 2):
            location = -0.31+(num*0.32)
            width = 0.3
        p.vbar(x=dodge('rank', location, range=p.x_range), top=str(num), width=width, source=source,
               color=colSpec[num]) 
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    return(p)   
    
def createPercentSource(sDF, rankNames, cat, catContents):
    data2 = {'rank': rankNames} 
    catCountList=[[] for i in range(len(catContents))]
    for rankName in rankNames:
        localList = createDataListPercent(sDF, rankName, cat, catContents)
        for num, val in enumerate(localList):
            catCountList[num].append(val)
    for num in range(len(catContents)):         
        data2.update({str(num):catCountList[num]})
    return(data2)
    
def createPercentP(source, rankNames, colSpec, title, catContents, legP=False):     
    p2 = figure(x_range=FactorRange(*rankNames), plot_height=430, plot_width=650,
           title=title,
           toolbar_location=None, tools="")
    catNums = [str(i) for i in range(len(catContents))]
    if (legP):
        p2.add_layout(Legend(orientation='horizontal'), 'below') 
        p2.vbar_stack(catNums, x='rank', width=0.9, source=source, color=colSpec,
             legend=catContents)
        p2.legend.label_text_font_size = '5.5pt'

    else:    
        p2.vbar_stack(catNums, x='rank', width=0.9, source=source, color=colSpec,
             legend=None)    
    p2.x_range.range_padding = 0.1
    p2.xgrid.grid_line_color = None
    return(p2)
    
df2019 = pd.read_csv('Navy2019.csv', header=0, index_col=0)
df2020 = pd.read_csv('Navy2020.csv', header=0, index_col=0)

raceNames = df2020.race.unique().tolist()
enlistedRanks = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9']
officerRanks = ['O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O9', 'O10']
warrantRanks = ['CWO2', 'CWO3', 'CWO4', 'CWO5']
ethnicNames = ['hispanic', 'not_hispanic']
genderNames = ['F', 'M']

select1 = Select(title='Rank Group', options=['Enlisted Ranks', 'Officer Ranks', 
                                              'Warrant Officer Ranks'], 
                 value='Enlisted Ranks')
select2 = Select(title='Rank Group', options=['Enlisted Ranks', 'Officer Ranks', 
                                              'Warrant Officer Ranks'], 
                 value='Enlisted Ranks')
select3 = Select(title='Rank Group', options=['Enlisted Ranks', 'Officer Ranks', 
                                              'Warrant Officer Ranks'], 
                 value='Enlisted Ranks')
rankNames1 = enlistedRanks
colSpec = Viridis7

title1 = "Navy Personnel Racial Makeup by Rank as of Jan 1, 2019 (source: U.S. Navy Demographic Data)"
title2 = "Navy Personnel Racial Makeup by Rank (%) as of Jan 1, 2019 (source: U.S. Navy Demographic Data)"
title3 = "Navy Personnel Racial Makeup by Rank as of Jan 1, 2020 (source: U.S. Navy Demographic Data)"
title4 = "Navy Personnel Racial Makeup by Rank (%) as of Jan 1, 2020 (source: U.S. Navy Demographic Data)"
 
hoverRace = HoverTool(tooltips=[
        ('Rank','@rank'), ('American Native','@0'), ('Asian', '@1'), ('African American', '@2'),
        ('Pacific Islander', '@3'), ('Multiple Races', '@4'), ('Decline to Respond', '@5'),
        ('White', '@6')
        ])
data1 = createCountSource(df2019, rankNames1, 'race', raceNames)
source1 = ColumnDataSource(data=data1)
p1 = createCountP(source1, rankNames1, colSpec, title1, raceNames)    
data2 = createPercentSource(df2019, rankNames1, 'race', raceNames)
source2 = ColumnDataSource(data2)
p2 = createPercentP(source2, rankNames1, colSpec, title2, raceNames)    
data3 = createCountSource(df2020, rankNames1, 'race', raceNames)
source3 = ColumnDataSource(data3)
p3 = createCountP(source3, rankNames1, colSpec, title3, raceNames)    
data4 = createPercentSource(df2020, rankNames1, 'race', raceNames)
source4 = ColumnDataSource(data4)
p4 = createPercentP(source4, rankNames1, colSpec, title4, raceNames, True)   
p1.y_range = p3.y_range; p2.y_range = p4.y_range
p1.title.text_font_size = '8pt';p2.title.text_font_size = '8pt'
p3.title.text_font_size = '8pt';p4.title.text_font_size = '8pt'
p1.add_tools(hoverRace); p2.add_tools(hoverRace)
p3.add_tools(hoverRace); p4.add_tools(hoverRace)

def callback1(attr, old, new):
    newRanks = enlistedRanks
    if select1.value == 'Warrant Officer Ranks':
        newRanks = warrantRanks
    elif select1.value == 'Officer Ranks':
        newRanks = officerRanks
        
    p1.x_range.factors = newRanks 
    new_data1 = createCountSource(df2019, newRanks, 'race', raceNames)
    source1.data = new_data1
    p2.x_range.factors = newRanks 
    new_data2 = createPercentSource(df2019, newRanks, 'race', raceNames) 
    source2.data = new_data2
    p3.x_range.factors = newRanks 
    new_data3 = createCountSource(df2020, newRanks, 'race', raceNames)  
    source3.data = new_data3
    p4.x_range.factors = newRanks 
    new_data4 = createPercentSource(df2020, newRanks, 'race', raceNames)
    source4.data = new_data4
    
def callback2(attr, old, new):
    newRanks = enlistedRanks
    if select2.value == 'Warrant Officer Ranks':
        newRanks = warrantRanks
    elif select2.value == 'Officer Ranks':
        newRanks = officerRanks
        
    p5.x_range.factors = newRanks 
    new_data5 = createCountSource(df2019, newRanks, 'sex', genderNames)
    source5.data = new_data5
    p6.x_range.factors = newRanks 
    new_data6 = createPercentSource(df2019, newRanks, 'sex', genderNames)
    source6.data = new_data6
    p7.x_range.factors = newRanks 
    new_data7 = createCountSource(df2020, newRanks, 'sex', genderNames)
    source7.data = new_data7
    p8.x_range.factors = newRanks 
    new_data8 = createPercentSource(df2020, newRanks, 'sex', genderNames)
    source8.data = new_data8 
    
def callback3(attr, old, new):
    newRanks = enlistedRanks
    if select3.value == 'Warrant Officer Ranks':
        newRanks = warrantRanks
    elif select3.value == 'Officer Ranks':
        newRanks = officerRanks
        
    p9.x_range.factors = newRanks 
    new_data9 = createCountSource(df2019, newRanks, 'ethnicity', ethnicNames)
    source9.data = new_data9
    p10.x_range.factors = newRanks 
    new_data10 = createPercentSource(df2019, newRanks, 'ethnicity', ethnicNames)
    source10.data = new_data10
    p11.x_range.factors = newRanks 
    new_data11 = createCountSource(df2020, newRanks, 'ethnicity', ethnicNames) 
    source11.data = new_data11
    p12.x_range.factors = newRanks 
    new_data12 = createPercentSource(df2020, newRanks, 'ethnicity', ethnicNames)
    source12.data = new_data12    
   
select1.on_change('value', callback1)  
select2.on_change('value', callback2)  
select3.on_change('value', callback3)  

colSpec2 = BuPu3 
title5 = "Navy Personnel Gender Makeup by Rank as of Jan 1, 2019 (source: U.S. Navy Demographic Data)"
title6 = "Navy Personnel Gender Makeup by Rank (%) as of Jan 1, 2019 (source: U.S. Navy Demographic Data)"
title7 = "Navy Personnel Gender Makeup by Rank as of Jan 1, 2020 (source: U.S. Navy Demographic Data)"
title8 = "Navy Personnel Gender Makeup by Rank (%) as of Jan 1, 2020 (source: U.S. Navy Demographic Data)"
   
data5 = createCountSource(df2019, rankNames1, 'sex', genderNames)
source5 = ColumnDataSource(data5)
p5 = createCountP(source5, rankNames1, colSpec2[:2], title5, genderNames)    
data6 = createPercentSource(df2019, rankNames1, 'sex', genderNames)
source6 = ColumnDataSource(data6)
p6 = createPercentP(source6, rankNames1, colSpec2[:2], title6, genderNames)    
data7 = createCountSource(df2020, rankNames1, 'sex', genderNames)
source7 = ColumnDataSource(data7)
p7 = createCountP(source7, rankNames1, colSpec2[:2], title7, genderNames)    
data8 = createPercentSource(df2020, rankNames1, 'sex', genderNames)
source8 = ColumnDataSource(data8)
p8 = createPercentP(source8, rankNames1, colSpec2[:2], title8, genderNames, True) 
p5.title.text_font_size = '8pt';p6.title.text_font_size = '8pt'
p7.title.text_font_size = '8pt';p8.title.text_font_size = '8pt'
p5.y_range = p7.y_range; p6.y_range = p8.y_range
hoverGender = HoverTool(tooltips=[
        ('Rank','@rank'), ('Female','@0'), ('Male', '@1')
        ])
p5.add_tools(hoverGender); p6.add_tools(hoverGender)
p7.add_tools(hoverGender); p8.add_tools(hoverGender)    

colSpec3 = Oranges3 
title9 = "Navy Personnel Ethnic Makeup by Rank as of Jan 1, 2019 (source: U.S. Navy Demographic Data)"
title10 = "Navy Personnel Ethnic Makeup by Rank (%) as of Jan 1, 2019 (source: U.S. Navy Demographic Data)"
title11 = "Navy Personnel Ethnic Makeup by Rank as of Jan 1, 2020 (source: U.S. Navy Demographic Data)"
title12 = "Navy Personnel Ethnic Makeup by Rank (%) as of Jan 1, 2020 (source: U.S. Navy Demographic Data)"
   
data9 = createCountSource(df2019, rankNames1, 'ethnicity', ethnicNames)
source9 = ColumnDataSource(data9)
p9 = createCountP(source9, rankNames1, colSpec3[:2], title9, ethnicNames) 
data10 = createPercentSource(df2019, rankNames1, 'ethnicity', ethnicNames)
source10 = ColumnDataSource(data10)
p10 = createPercentP(source10, rankNames1, colSpec3[:2], title10, ethnicNames)   
data11 = createCountSource(df2020, rankNames1, 'ethnicity', ethnicNames)
source11 = ColumnDataSource(data11)
p11 = createCountP(source11, rankNames1, colSpec3[:2], title11, ethnicNames)    
data12 = createPercentSource(df2020, rankNames1, 'ethnicity', ethnicNames)
source12 = ColumnDataSource(data12)
p12 = createPercentP(source12, rankNames1, colSpec3[:2], title12, ethnicNames, True)
p9.title.text_font_size = '8pt';p10.title.text_font_size = '8pt'
p11.title.text_font_size = '8pt';p12.title.text_font_size = '8pt'
p9.y_range = p11.y_range; p10.y_range = p12.y_range
hoverEthnicity = HoverTool(tooltips=[
        ('Rank','@rank'), ('Hispanic','@0'), ('Not Hispanic', '@1')
        ])
p9.add_tools(hoverEthnicity); p10.add_tools(hoverEthnicity)
p11.add_tools(hoverEthnicity); p12.add_tools(hoverEthnicity)  

first = Panel(child=gridplot([[p1,p3,widgetbox(select1, width=180)], [p2,p4,]]), title='Race')
second = Panel(child=gridplot([[p5,p7,widgetbox(select2, width=180)], [p6, p8,]]), title='Gender')
third = Panel(child=gridplot([[p9,p11,widgetbox(select3, width=180)], [p10, p12,]]), title='Ethnicity')
tabs = Tabs(tabs = [first, second, third])

curdoc().add_root(tabs)
#output_file('test.html')
#show(tabs)

  
