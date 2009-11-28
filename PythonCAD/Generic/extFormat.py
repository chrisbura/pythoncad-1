#
# Copyright (c) 2009 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the termscl_bo of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
#
# This code is written by Yagnesh Desai
#


import os.path
import re # added to handle Mtext
from PythonCAD.Generic.point    import Point
from PythonCAD.Generic.segment  import Segment
from PythonCAD.Generic.circle   import Circle
from PythonCAD.Generic.arc      import Arc
from PythonCAD.Generic.layer    import Layer

dxfDebug=True # debug variable

class ExtFormat(object):
    """
        This class provide base class for hendly different drawing format in pythoncad
    """
    def __init__(self,gtkimage):
        """
            Default Constructor
        """
        self.__gtkimage=gtkimage
    def openFile(self,fileName):
        """
           Open a generic file 
        """
        path,exte=os.path.splitext( fileName )
        if( exte.upper()==".dxf".upper()):
            dxf=Dxf(self.__gtkimage,fileName)
            dxf.importEntitis()

class DrawingFile(object):
    """
        This Class provide base capability to read write a  file
    """
    def __init__(self,fileName):
        """
            Base Constructor
        """
        self.__fn=fileName
        self.__fb=None
    def ReadAsci(self):
        """
            Read a generic file 
        """
        self.__fb=open(self.__fn,'r')
    def FileObject(self):
        """
            Return the file opened 
        """
        if self.__fb is not None: 
          return self.__fb
        else: 
          return None

class Dxf(DrawingFile):
    """
        this class provide dxf reading/writing capability 
    """
    def __init__(self,gtkimage,fileName):
        """
            Default Constructor
        """
        DrawingFile.__init__(self,fileName)
        self.__gtkimage=gtkimage
        self.__image=gtkimage.getImage()
        _layerName,_ext=os.path.splitext(os.path.basename(fileName))
        _layerName="Imported_"+_layerName
        _dxfLayer=Layer(_layerName)
        self.__image.addLayer(_dxfLayer)
        self.__dxfLayer=_dxfLayer 
        
    def importEntitis(self):
        """
            Open The file and create The entity in pythonCad
        """
        print "Debug: import entitys"
        self.ReadAsci();
        fo=self.FileObject()
        while True:
            line = fo.readline()
            if not line: break
            else:
                #print "Debug: Read Line line = [%s] "%str(line), lineNumber
                """Implement here your method"""
                k = line
                if k[0:4] == 'LINE':
                    self.createLineFromDxf(fo)
                if k[0:6] == 'CIRCLE':
                    self.createCircleFromDxf(fo)
                """                
                if k[0:5] == 'MTEXT':
                    self.createTextFromDxf(fo)
                if k[0:4] == 'TEXT':
                    self.createTextFromDxf(fo)
                """
                if k[0:3] == 'ARC':
                    self.createArcFromDxf(fo)                 
                if not k : break
                #break
                # indicates the data of lines are there in next block of 19 lines
                # Similar subroutine can be return for collecting data of circle/polyline/arc
                # Matteo Boscolo ++
    
    def createLineFromDxf(self,fo):
        """
            read the line dxf section and create the line
        """
        dPrint("createLineFromDxf" )
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        g = 0 # start counter to read lines
        while g < 20:
            line = fo.readline()
            #print "Debug g =", g
            #print "Debug: Read line  g = %s Value = %s "%(str(g),str(line))
            g+=1
            #  continue
            k = line
            #print "Debug: Read line g = %s k =  %s "%(str(g),str(k))
            """if g == 5:# this line contains color property
            we can get the color presently not implemented
            color=(float(k[0:-1]))"""
            dPrint( "line value for line creation k=" + k)
            if k[0:3] == ' 10':
                #print "debug 10", k
                # this line of file contains start point"X" co ordinate
                #print "Debug: Convert To flot x1: %s" % str(k[0:-1])
                k = fo.readline()
                x1 = (float(k[0:-1]))
            if k[0:3] == ' 20':# this line of file contains start point "Y" co ordinate
                #print "Debug: Convert To flot y1: %s" % str(k[0:-1])
                k = fo.readline()
                y1 = (float(k[0:-1]))
            if k[0:3] == ' 30':# this line of file contains start point "Z" co ordinate
                #print "Debug: Convert To flot z1: %s" % str(k[0:-1])
                k = fo.readline()
                z1 = (float(k[0:-1])) 
                # Z co ordinates are not used in PythonCAD we can live without this line
            if k[0:3] == ' 11':# this line of file contains End point "X" co ordinate
                #print "Debug: Convert To flot x2: %s" % str(k[0:-1])
                k = fo.readline()
                x2 = (float(k[0:-1]))
            if k[0:3] == ' 21':# this line of file contains End point "Y" co ordinate
                #print "Debug: Convert To flot y2: %s" % str(k[0:-1])
                k = fo.readline()
                y2 = (float(k[0:-1]))
            if k[0:3] == ' 31':# this line of file contains End point "Z" co ordinate
                #print "Debug: Convert To flot z2: %s" % str(k[0:-1])
                k =  fo.readline()
                z2 = (float(k[0:-1]))
                #Z co ordinates are not used in PythonCAD we can live without this line
                #'I need a "create segment code" here to append the segment to image'
        if x1 != None and y1!= None and x2!= None and y2!= None :
            self.createLine(x1,y1,x2,y2)
                #g = 0 # Search for next line in the dxf file
            
        #x2+=2
        #y2+=2 

    def createLine(self,x1,y1,x2,y2):
      """
          Create the line into the current drawing
          In this implementation all the lines gose to the active layer and use the global settings of pythoncad
          Feauture implementation could be :
          1) Create a new layer(ex: Dxf Import)
          2) Read dxf import style propertis and set it to the line
      """    
      _active_layer = self.__dxfLayer
      _p1 = Point(x1, y1)
      _active_layer.addObject(_p1)
      _p2 = Point(x2, y2)
      _active_layer.addObject(_p2)
      _s = self.__image.getOption('LINE_STYLE')
      _seg = Segment(_p1, _p2, _s)
      _l = self.__image.getOption('LINE_TYPE')
      if _l != _s.getLinetype():
          _seg.setLinetype(_l)
      _c = self.__image.getOption('LINE_COLOR')
      if _c != _s.getColor():
          _seg.setColor(_c)
      _t = self.__image.getOption('LINE_THICKNESS')
      if abs(_t - _s.getThickness()) > 1e-10:
          _seg.setThickness(_t)
      _active_layer.addObject(_seg)
    
    def createCircleFromDxf(self,fo):
        """
            Read and create the Circle into drawing
        """
        print "Debug createCircleFromDxf" 
        x = None
        y = None
        r = None
        g = 0 # reset g
        while g < 20:
            g+=1
            k = fo.readline()
            print "line value for circle creation k=", k
            if k[0:3] == ' 10':
                k = fo.readline()
                x = (float(k[0:-1]))
                print "circle center x =", x
            if k[0:3] == ' 20':
                k = fo.readline()
                y = (float(k[0:-1]))
                print "circle center y =", y
            if k[0:3] == ' 30':
                k = fo.readline()
                z = (float(k[0:-1]))
                print "circle center z =", z
            if k[0:3] == ' 40':
                k = fo.readline()
                r = (float(k[0:-1]))
                print "circle radius=", r
                # g > 1 for break
        if x is not None and y is not None and r is not None:
            self.createCircle(x,y,r)
        
    def createCircle(self,x,y,r):
        """
            create a circle entitys into the current drawing
        """
        _active_layer = self.__dxfLayer
        _center = Point(x, y)
        _active_layer.addObject(_center)
        _s = self.__image.getOption('LINE_STYLE')
        _circle = Circle(_center, r, _s)        
        _l = self.__image.getOption('LINE_TYPE')
        if _l != _s.getLinetype():
            _circle.setLinetype(_l)
        _c = self.__image.getOption('LINE_COLOR')
        if _c != _s.getColor():
            _circle.setColor(_c)
        _t = self.__image.getOption('LINE_THICKNESS')
        if abs(_t - _s.getThickness()) > 1e-10:
            _circle.setThickness(_t)
        _active_layer.addObject(_circle)
        
    def createTextFromDxf(self,fo):
        """
            Read and create the Circle into drawing
        """
        print "Debug createTextFromDxf" 
        g = 0 # reset g
        while g < 20:
            g+=1
            k = fo.readline()
            dPrint( "line value for text from k="+ k)
            if k[0:3] == ' 10':
                k = fo.readline()
                x = (float(k[0:-1]))
                dPrint ("Text Loc x ="+ x)
            if k[0:3] == ' 20':
                k = fo.readline()
                y = (float(k[0:-1]))
                dPrint ("Text Loc y ="+ y)
            if k[0:3] == ' 30':
                k = fo.readline()
                z = (float(k[0:-1]))
                dPrint ("Text Loc z ="+z)
            if k[0:3] == ' 40':
                k = fo.readline()
                h = (float(k[0:-1]))
                dPrint("Text Height ="+ h)
            if k[0:3] == '  1':
                k = fo.readline()
                t = k.replace('\~', ' ')
                msg=str("Text itself is ", x, y, z, 'height', h, t)   
                dPrint(msg) 
                # g > 1 for break
    # createText (x,y,h,t) needed
                
    def createArcFromDxf(self,fo):
        """
            Read and create the ARC into drawing
        """
        dPrint( "createArcFromDxf" )
        g = 0 # reset g
        x=None
        y=None
        sa=None
        ea=None
        r=None
        while g < 20:
            g+=1
            k = fo.readline()
            dPrint("Line: %s"%str(k))
            if k[0:3] == ' 10':
                k = fo.readline()
                x = (float(k[0:-1]))
                dPrint( "Arc center x =" + str(x))
            if k[0:3] == ' 20':
                k = fo.readline()
                y = (float(k[0:-1]))
                dPrint("Arc center y ="+ str(y))
            if k[0:3] == ' 30':
                k = fo.readline()
                z = (float(k[0:-1]))
                dPrint("Arc center z ="+str(z))
            if k[0:3] == ' 40':
                k = fo.readline()
                r = (float(k[0:-1]))
                dPrint("Arc radius=" + str(r))
            if k[0:3] == ' 50':
                k = fo.readline()
                sa = (float(k[0:-1]))
                dPrint("Start Angle=" + str(sa))
            if k[0:3] == ' 51':
                k = fo.readline()
                ea = (float(k[0:-1]))
                dPrint( "End Angle=" + str(ea))
                # g > 1 for break
                'I need a "create Arc code" here to append the segment to image'
        if  (x is not None and y is not None and sa is not None
                                and ea is not None and r is not None):
            self.createArc(x,y,sa,ea,r)

    def createArc(self,x,y,sa,ea,r):
        """
            create a Arc entitys into the current drawing
        """
        _active_layer = self.__dxfLayer
        _center = Point(x, y)
        _active_layer.addObject(_center)
        _s = self.__image.getOption('LINE_STYLE')
        _arc = Arc(_center, r, sa, ea, _s)
        _l = self.__image.getOption('LINE_TYPE')
        if _l != _s.getLinetype():
            _arc.setLinetype(_l)
        _c = self.__image.getOption('LINE_COLOR')
        if _c != _s.getColor():
            _arc.setColor(_c)
        _t = self.__image.getOption('LINE_THICKNESS')
        if abs(_t - _s.getThickness()) > 1e-10:
            _arc.setThickness(_t)
        _active_layer.addObject(_arc)
def dPrint(msg):
    """
        Debug function for the dxf file
    """
    if dxfDebug :
        print "Debug: %s " %str(msg)