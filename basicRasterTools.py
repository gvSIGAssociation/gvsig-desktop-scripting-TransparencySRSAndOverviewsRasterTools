# encoding: utf-8

import gvsig
import os
import subprocess
from gvsig.libs.formpanel import FormPanel
from org.gvsig.andami import PluginsLocator
from gvsig import getResource
from gvsig.libs.formpanel import FormPanel, load_icon
from gvsig.commonsdialog import msgbox
from org.gvsig.tools.swing.api import ToolsSwingLocator

class TransparencySRSAndOverviewsRasterTools(FormPanel):
    def __init__(self):
        FormPanel.__init__(self, getResource(__file__, "basicRasterTools.xml"))
        toolsSwingManager = ToolsSwingLocator.getToolsSwingManager()
        
        self.btnColorT.setText("")
        self.inputfileT = toolsSwingManager.createFilePickerController(self.txtInputFileT, self.btnInputFileT)
        self.outputfileT = toolsSwingManager.createFilePickerController(self.txtOutputFileT, self.btnOutputFileT)
        self.colorT = toolsSwingManager.createColorPickerController(self.txtColorT, self.btnColorT)

        self.inputfileS = toolsSwingManager.createFilePickerController(self.txtInputFileS, self.btnInputFileS)
        self.outputfileS = toolsSwingManager.createFilePickerController(self.txtOutputFileS, self.btnOutputFileS)

        self.inputfileO = toolsSwingManager.createFilePickerController(self.txtInputFileO, self.btnFileO)

        self.setPreferredSize(500,275)

    def btnTransp_click(self, *args):
        #GUI INFO
        inputFT=self.inputfileT.get()
        outputFT=self.outputfileT.get()
        colorTr=self.colorT.get()
        
        if inputFT == None: 
            msgbox("No hay especificado un fichero de entrada")
            return
            
        if outputFT == None: 
            msgbox("No hay especificado un fichero de salida") #MIRAR LO DEL COLOR
            return
            
        #Path INFO
        pluginsManager = PluginsLocator.getManager()
        appfolder = pluginsManager.getApplicationFolder().getAbsolutePath()
        gdalwarpFile="%s/gvSIG/extensiones/org.gvsig.gdal.app.mainplugin/gdal/bin/gdal/apps/gdalwarp" % appfolder.replace("\\","/")

        #Request
        cmdGdalwarp=[
               gdalwarpFile,
               r"-srcnodata",
               '"%s %s %s"' %(colorTr.getRed(),colorTr.getGreen(),colorTr.getBlue()),
               r"-dstnodata",
               '"%s %s %s"' %(colorTr.getRed(),colorTr.getGreen(),colorTr.getBlue()),
               r"-dstalpha",
               inputFT.getAbsolutePath(),
               outputFT.getAbsolutePath()
               ]
        gdalwarp=subprocess.call(cmdGdalwarp)
        if gdalwarp==1:
            msgbox("Error en el proceso")
        else:
            msgbox("Proceso ejecutado con exito")



    def btnSRS_click(self, *args):
        #GUI INFO
        inputFS=self.inputfileS.get()
        outputFS=self.outputfileS.get()
        newSRS=self.txtSRS.getText()
        compress=self.radioCompressorS.isSelected()
        tiles=self.radioTilesS.isSelected()
        
        if inputFS == None: 
            msgbox("No hay especificado un fichero de entrada")
            return
            
        if outputFS == None: 
            msgbox("No hay especificado un fichero de salida")
            return

        if compress:
            compressF="COMPRESS=DEFLATE" #Se puede cambiar el algoritmo de compresion (PACKBITS, DEFLATE, LZW, LZMA, ZSTD)
        else:
            compressF="COMPRESS=None"

        if tiles:
            tilesF="TILED=YES"
        else:
            tilesF="TILED=NO"
            
        #Path INFO
        pluginsManager = PluginsLocator.getManager()
        appfolder = pluginsManager.getApplicationFolder().getAbsolutePath()
        gdal_translateFile="%s/gvSIG/extensiones/org.gvsig.gdal.app.mainplugin/gdal/bin/gdal/apps/gdal_translate" % appfolder.replace("\\","/")

        #Request
        cmdGdal_translate=[
               gdal_translateFile,
               r"-a_srs",
               newSRS,
               r"-co",
               compressF,
               r"-co",
               tilesF,
               inputFS.getAbsolutePath(),
               outputFS.getAbsolutePath()
               ]
        gdal_translate=subprocess.call(cmdGdal_translate)
        if gdal_translate==1:
            msgbox("Error en el proceso")
        else:
            msgbox("Proceso ejecutado con exito")


    def btnOverviews_click(self, *args):
        #GUI INFO
        inputFO=self.inputfileO.get()
        
        if inputFO == None: 
            msgbox("No hay especificado un fichero a modificar")
            return

        #Path INFO
        pluginsManager = PluginsLocator.getManager()
        appfolder = pluginsManager.getApplicationFolder().getAbsolutePath()
        gdaladdoFile="%s/gvSIG/extensiones/org.gvsig.gdal.app.mainplugin/gdal/bin/gdal/apps/gdaladdo" % appfolder.replace("\\","/")

        #Request
        cmdGdaladdo=[
               gdaladdoFile,
               r"--config",
               "COMPRESS_OVERVIEW DEFLATE",
               r"-ro",
               inputFO.getAbsolutePath(),
               "2",
               "4",
               "8",
               "16"
               ]
        gdaladdo=subprocess.call(cmdGdaladdo)
        if gdaladdo==1:
            msgbox("Error en el proceso")
        else:
            msgbox("Proceso ejecutado con exito")


def rasterTools(*args):
    l=TransparencySRSAndOverviewsRasterTools()
    l.showWindow("Basic Raster Tools")


def main (*args):
    rasterTools()
