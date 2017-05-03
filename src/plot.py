import sys,os
import pandas as pd
from bokeh.charts import Bar, output_file, show, save
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend

if not len(sys.argv) == 2:
  print "Usage:",sys.argv[0],"results_folder "
  sys.exit(-1)
 

def plot(path,file_csv,name):
	df = pd.read_csv(path+file_csv, sep='\t', encoding='utf-8')
	df = df.iloc[::-1]
	names = list(df.columns.values)
	dic = df.set_index('Unnamed: 0').to_dict()
	bar = Bar(df, 
		  values=blend(str(names[9]),str(names[8]),str(names[7]),str(names[6]),str(names[5]),str(names[4]),str(names[3]),str(names[2]),str(names[1]),name='localizations', labels_name='localization'),
          label=cat(columns='Unnamed: 0', sort=False),
          stack=cat(columns='localization', sort=True),
          color=color(columns='localization', palette=['#1f77b4','#ff7f0e','#7f7f7f','#d62728','#9467bd','#bcbd22','#98df8a','#17becf','#393b79'],sort=True),
          legend= (0.0,+480.0),
          xlabel = "",
          ylabel = "Score",
          title="Results",
          tooltips=[('LOC', '@localization'), ('Score', '@height{1.11}')])
	bar.xaxis.major_label_text_font_size = "10pt"	
	bar.yaxis.axis_label_text_font_size = "15pt"
	bar.legend.orientation = "horizontal"
	output_file(path+name+".html")
	save(bar)

for files_csv in os.listdir(sys.argv[1]+"/plot/"):
	print files_csv
	name_plot = files_csv.split('.')[0]
	plot(sys.argv[1]+"/plot/",files_csv,name_plot)
