########################################################################
# $Header: /tmp/libdirac/tmp.stZoy15380/dirac/DIRAC3/DIRAC/Core/Utilities/Graphs/Legend.py,v 1.4 2009/06/08 23:48:42 atsareg Exp $
########################################################################

""" Legend encapsulates a graphical plot legend drawing tool
    
    The DIRAC Graphs package is derived from the GraphTool plotting package of the
    CMS/Phedex Project by ... <to be added>
"""

__RCSID__ = "$Id: Legend.py,v 1.4 2009/06/08 23:48:42 atsareg Exp $"

from matplotlib.patches import Rectangle
from matplotlib.text import Text
from DIRAC.Core.Utilities.Graphs.GraphUtilities import *  
from DIRAC.Core.Utilities.Graphs.Palette import Palette  
from DIRAC.Core.Utilities.Graphs.GraphData import GraphData
from matplotlib.figure import Figure 
from matplotlib.backends.backend_agg import FigureCanvasAgg
import types

class Legend:

  def __init__(self,data=None,axes=None,*aw,**kw):
  
    self.labels = {}
    if type(data) == types.DictType:
      for label,ddict in data.items():
        #self.labels[label] = pretty_float(max([ float(x) for x in ddict.values() if x ]) )  
        self.labels[label] = "%.1f" % max([ float(x) for x in ddict.values() if x ])   
    elif type(data) == types.InstanceType and data.__class__ == GraphData:
      self.labels = data.getLabels()    
    else:
      self.labels = data  
    self.labels.reverse()  
    self.ax = axes
    self.canvas = None
    if self.ax:
      self.canvas = self.ax.figure.canvas
      self.ax.set_axis_off()
    self.prefs = evalPrefs(*aw,**kw)
    self.palette = Palette()
    self.__get_column_width()
    
  def dumpPrefs(self):
  
    for key in self.prefs:
      print key.rjust(20),':',str(self.prefs[key]).ljust(40)
      
  def setLabels(self,labels):
  
    self.labels = labels   
    
  def setAxes(self,axes):
  
    self.ax = axes  
    self.canvas = self.ax.figure.canvas
    self.ax.set_axis_off() 
    
  def getLegendSize(self):
    self.__get_column_width()
    legend_position = self.prefs['legend_position']
    legend_width = float(self.prefs['legend_width']) 
    legend_height = float(self.prefs['legend_height']) 
    legend_padding = float(self.prefs['legend_padding'])   
    if legend_position in ['right','left']:
      # One column in case of vertical legend
      legend_width = self.column_width+legend_padding
    elif legend_position == 'bottom':
      nColumns = min(self.prefs['max_columns'],int(legend_width/self.column_width))
      nLabels = len(self.labels)
      maxRows = self.prefs['max_rows']
      nRows_ax = int(legend_height/1.6/self.prefs['text_size'])
      nRows_label = nLabels/nColumns + (nLabels%nColumns != 0)
      nRows = max(1,min(min(nRows_label,maxRows),nRows_ax ))
      text_padding = self.prefs['text_padding']    
      text_padding = pixelToPoint(text_padding,self.prefs['dpi'])    
      legend_height = min(legend_height,(nRows*(self.text_size+text_padding)+text_padding))
      
    return legend_width,legend_height  

  def __get_column_width(self):
  
    max_length = 0
    max_column_text = ''
    for label,num in self.labels:
      if num is not None:
        column_length = len(str(label)+str(num)) + 1
      else:
        column_length = len(str(label)) + 1  
      if column_length > max_length:
        max_length = column_length
        max_column_text = '%s  %s' % (str(label),str(num))
               
    figure = Figure()   
    canvas = FigureCanvasAgg(figure) 
    dpi = self.prefs['dpi']
    figure.set_dpi( dpi ) 
    text_size = self.prefs['text_size']    
    self.text_size = pixelToPoint(text_size,dpi)           
    text = Text(0.,0.,text=max_column_text,size=self.text_size)
    text.set_figure(figure)
    bbox = text.get_window_extent(canvas.get_renderer())
    self.column_width = bbox.width+6*self.prefs['text_size']
    
  def draw(self):
  
    dpi = self.prefs['dpi']
    self.text_size = float(self.prefs['text_size'])*100./float(dpi)
    ax_xsize = self.ax.get_window_extent().width
    ax_ysize = self.ax.get_window_extent().height
  
    nLabels = len(self.labels)
    nColumns = min(self.prefs['max_columns'],int(ax_xsize/self.column_width))
    
    maxRows = self.prefs['max_rows']
    nRows_ax = int(ax_ysize/1.6/self.prefs['text_size'])
    nRows_label = nLabels/nColumns + (nLabels%nColumns != 0)
    nRows = max(1,min(min(nRows_label,maxRows),nRows_ax ))
    maxLabels = nColumns*nRows - 1
    self.ax.set_xlim(0.,float(ax_xsize))
    self.ax.set_ylim(-float(ax_ysize),0.)
   
    self.text_size_point = float(self.prefs['text_size'])*100./float(self.prefs['dpi'])
        
    box_width = self.prefs['text_size']
    legend_offset = (ax_xsize - nColumns*self.column_width)/2 
    
    nc = 0
    self.labels.reverse()
    for label,num in self.labels:
      num = "%.1f" % num
      color = self.palette.getColor(label)
      row = nc%nRows 
      column = nc/nRows          
      if row == nRows-1 and column == nColumns-1 and nc != nLabels-1:
        last_text = '... plus %d more' % (nLabels-nc)
        self.ax.text(float(column*self.column_width)+legend_offset,-float(row*1.6*box_width),
                     last_text,horizontalalignment='left',
                     verticalalignment='top',size=self.text_size_point)  
        break   
      else:
        self.ax.text(float(column*self.column_width)+2.*box_width+legend_offset,-row*1.6*box_width,
                     str(label),horizontalalignment='left',
                     verticalalignment='top',size=self.text_size_point)
        if num is not None:
          self.ax.text(float((column+1)*self.column_width)-2*box_width+legend_offset,-float(row*1.6*box_width),
                       str(num),horizontalalignment='right',
                       verticalalignment='top',size=self.text_size_point)             
        box = Rectangle((float(column*self.column_width)+legend_offset,-float(row*1.6*box_width)-box_width),
                        box_width,box_width)            
        box.set_ec('black')
        box.set_linewidth(pixelToPoint(0.5,dpi))
        box.set_fc(color)
        self.ax.add_patch(box)
        nc += 1    
