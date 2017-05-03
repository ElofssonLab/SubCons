from bokeh.charts import Bar, output_file, show
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend
from bokeh.palettes import Spectral6,small_palettes,inferno,Set1,Set3,Paired,Category20
import pandas as pd
import os,sys
import numpy as np

df = pd.read_csv(sys.argv[1],sep = '\t')
df = df.iloc[::-1]
names = list(df.columns.values)
dic = df.set_index('Unnamed: 0').to_dict()
bar = Bar(df, 
		  values=blend(str(names[9]),str(names[8]),str(names[7]),str(names[6]),str(names[5]),str(names[4]),str(names[3]),str(names[2]),str(names[1]),name='localizations', labels_name='localization'),
          label=cat(columns='Unnamed: 0', sort=False),
          stack=cat(columns='localization', sort=True),
          color=color(columns='localization', palette=Category20[9],sort=True),
          legend='top_right',
          xlabel = "",
          ylabel = "Score",
          title="Results",
          tooltips=[('LOC', '@localization'), ('Score', '@height{1.11}')])
bar.axis.major_label_text_font_size = "10pt"	
output_file(sys.argv[1]+".html")
  
        
show(bar)


