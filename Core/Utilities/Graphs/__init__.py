########################################################################
# $Header: /tmp/libdirac/tmp.stZoy15380/dirac/DIRAC3/DIRAC/Core/Utilities/Graphs/__init__.py,v 1.9 2009/06/08 23:48:42 atsareg Exp $
########################################################################

""" DIRAC Graphs package provides tools for creation of various plots to provide
    graphical representation of the DIRAC Monitoring and Accounting data
    
    The DIRAC Graphs package is derived from the GraphTool plotting package of the
    CMS/Phedex Project by ... <to be added>
"""

__RCSID__ = "$Id: __init__.py,v 1.9 2009/06/08 23:48:42 atsareg Exp $"

from DIRAC.Core.Utilities.Graphs.Graph import Graph
from DIRAC.Core.Utilities.Graphs.GraphUtilities import evalPrefs
import time

graph_large_prefs = {
  'width':1000,
  'height':700,
  'max_rows':99,
  'max_columns':4,
  'text_size':8,
  'subtitle_size':10,
  'subtitle_padding':5,
  'title_size':15,
  'title_padding':5,
  'dpi':100,
  'text_padding':5,
  'figure_padding':15,
  'plot_title_size':12,
  'plot_padding':50,
  'frame':'On',
  'font' : 'Lucida Grande',
  'font_family' : 'sans-serif',
  'square_axis':False,
  'legend':True,
  'legend_position':'bottom',
  'legend_width':800,
  'legend_height':600,
  'legend_padding':20,
  'plot_grid':'1:1',
  'limit_labels':15,
  'graph_time_stamp':True                        
}

graph_normal_prefs = {
  'width':800,
  'height':600,
  'max_rows':99,
  'max_columns':4,
  'text_size':8,
  'subtitle_size':10,
  'subtitle_padding':5,
  'title_size':15,
  'title_padding':10,
  'dpi':100,
  'text_padding':5,
  'figure_padding':12,
  'plot_title_size':12,
  'plot_padding':50,
  'frame':'On',
  'font' : 'Lucida Grande',
  'font_family' : 'sans-serif',
  'square_axis':False,
  'legend':True,
  'legend_position':'bottom',
  'legend_width':600,
  'legend_height':120,
  'legend_padding':20,
  'plot_grid':'1:1',
  'limit_labels':15,
  'graph_time_stamp':True                        
}

graph_small_prefs = {
  'width':450,
  'height':330,
  'max_rows':99,
  'max_columns':4,
  'text_size':10,
  'subtitle_size':5,
  'subtitle_padding':4,
  'title_size':10,
  'title_padding':6,
  'dpi':100,
  'text_padding':3,
  'figure_padding':10,
  'plot_title_size':8,
  'plot_padding':35,
  'frame':'On',
  'font' : 'Lucida Grande',
  'font_family' : 'sans-serif',
  'square_axis':False,
  'legend':True,
  'legend_position':'bottom',
  'legend_width':300,
  'legend_height':50,
  'legend_padding':10,
  'plot_grid':'1:1',
  'limit_labels':15,
  'graph_time_stamp':True                         
}

graph_thumbnail_prefs = {
  'width':100,
  'height':80,
  'max_rows':99,
  'max_columns':4,
  'text_size':6,
  'subtitle_size':0,
  'subtitle_padding':0,
  'title_size':8,
  'title_padding':2,
  'dpi':100,
  'text_padding':1,
  'figure_padding':2,
  'plot_title_size':8,
  'plot_padding':0,
  'frame':'On',
  'font' : 'Lucida Grande',
  'font_family' : 'sans-serif',
  'square_axis':False,
  'legend':False,
  'plot_grid':'1:1',
  'plot_axis_grid':False,
  'plot_axis':False,
  'plot_axis_labels':False,
  'graph_time_stamp':False,
  'tight_bars':True                        
}

def graph(data,file,*args,**kw):
  
  prefs = evalPrefs(*args,**kw)
  if prefs.has_key('graph_size'):
    graph_size = prefs['graph_size']
  else:
    graph_size = "normal"
     
  if graph_size == "normal":
    defaults = graph_normal_prefs
  elif graph_size == "small":
    defaults = graph_small_prefs  
  elif graph_size == "thumbnail":
    defaults = graph_thumbnail_prefs   
  elif graph_size == "large":
    defaults = graph_large_prefs    
        
  graph = Graph()
  start = time.time()
  graph.makeGraph(data,defaults,prefs)
  #print "AT >>>> makeGraph time",time.time()-start
  start = time.time()
  graph.writeGraph(file,'PNG')
  #print "AT >>>> writeGraph time",time.time()-start

def barGraph(data,file,*args,**kw):
  
  graph(data,file,plot_type='BarGraph',*args,**kw)
  
def lineGraph(data,file,*args,**kw):
  
  graph(data,file,plot_type='LineGraph',*args,**kw)  
  
def cumulativeGraph(data,file,*args,**kw):
  
  graph(data,file,plot_type='LineGraph',cumulate_data=True,*args,**kw)  
  
def pieGraph(data,file,*args,**kw):
  
  graph(data,file,plot_type='PieGraph',*args,**kw)  
  
def qualityGraph(data,file,*args,**kw):  
  
  graph(data,file,plot_type='QualityMapGraph',*args,**kw)  