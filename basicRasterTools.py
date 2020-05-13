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
from org.gvsig.fmap.dal.swing import DALSwingLocator
from gvsig import logger,LOGGER_WARN
from org.gvsig.tools import ToolsLocator
from java.awt import Color

class TransparencySRSAndOverviewsRasterTools(FormPanel):
    def __init__(self):
        FormPanel.__init__(self, getResource(__file__, "basicRasterTools.xml"))
        toolsSwingManager = ToolsSwingLocator.getToolsSwingManager()
        
        self.btnColorT.setText("")
        self.inputfileT = toolsSwingManager.createFilePickerController(self.txtInputFileT, self.btnInputFileT)
        self.outputfileT = toolsSwingManager.createFilePickerController(self.txtOutputFileT, self.btnOutputFileT)
        self.colorT = toolsSwingManager.createColorPickerController(self.txtColorT, self.btnColorT)
        self.colorT.set(Color(97, 97, 97))

        self.inputfileS = toolsSwingManager.createFilePickerController(self.txtInputFileS, self.btnInputFileS)
        self.outputfileS = toolsSwingManager.createFilePickerController(self.txtOutputFileS, self.btnOutputFileS)
        self.projS = DALSwingLocator.getDataSwingManager().createProjectionPickerController(self.txtNewSRS, self.btnNewSRS)

        self.inputfileO = toolsSwingManager.createFilePickerController(self.txtInputFileO, self.btnFileO)

        self.setPreferredSize(600,300)

    def btnTransp_click(self, *args):
        #GUI INFO
        inputFT=self.inputfileT.get()
        outputFT=self.outputfileT.get()
        colorTr=self.colorT.get()
        outputFormat=self.cboOutputFormatT.getSelectedItem()
        
        if inputFT == None: 
            msgbox("No hay especificado un fichero de entrada")
            return
            
        if outputFT == None: 
            msgbox("No hay especificado un fichero de salida") #MIRAR LO DEL COLOR
            return
            
        #Path INFO
        gdalwarpFile= getCommand("gdalwarp")

        #Request
        cmdGdalwarp=[
               gdalwarpFile,
               r"-srcnodata",'"%s %s %s"' %(colorTr.getRed(),colorTr.getGreen(),colorTr.getBlue()),
               r"-dstnodata",'"%s %s %s"' %(colorTr.getRed(),colorTr.getGreen(),colorTr.getBlue()),
               r"-dstalpha",
               r"-of",str(outputFormat),
               inputFT.getAbsolutePath(),
               outputFT.getAbsolutePath()
               ]
        logger(str(cmdGdalwarp))
        returnCode=subprocess.call(cmdGdalwarp)
        if returnCode!=0:
            logger('Error al ejecutar el comando de GDAL (returnCode %s)' %returnCode,LOGGER_WARN)
            msgbox("Error en el proceso.")
        else:
            msgbox("Proceso ejecutado con exito")



    def btnSRS_click(self, *args):
        #GUI INFO
        inputFS=self.inputfileS.get()
        outputFS=self.outputfileS.get()
        newSRS=self.projS.get().getAbrev()
        compress=self.radioCompressorS.isSelected()
        tiles=self.radioTilesS.isSelected()
        outputFormat=self.cboOutputFormatSRS.getSelectedItem()
        
        if inputFS == None: 
            msgbox("No hay especificado un fichero de entrada")
            return
            
        if outputFS == None: 
            msgbox("No hay especificado un fichero de salida")
            return
            
        if newSRS == None: 
            msgbox("No hay especificado SRS")
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
        gdal_translateFile= getCommand("gdal_translate")

        #Request
        cmdGdal_translate=[
               gdal_translateFile,
               r"-a_srs",newSRS,
               r"-co",compressF,
               r"-co",tilesF,
               r"-of",str(outputFormat),
               inputFS.getAbsolutePath(),
               outputFS.getAbsolutePath()
               ]
        logger(str(cmdGdal_translate))
        returnCode=subprocess.call(cmdGdal_translate)
        if returnCode!=0:
            logger('Error al ejecutar el comando de GDAL (returnCode %s)' %returnCode,LOGGER_WARN)
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
        gdaladdoFile= getCommand("gdaladdo")

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
        logger(str(cmdGdaladdo))
        returnCode=subprocess.call(cmdGdaladdo)
        if returnCode!=0:
            logger('Error al ejecutar el comando de GDAL (returnCode %s)' %returnCode,LOGGER_WARN)
            msgbox("Error en el proceso")
        else:
            msgbox("Proceso ejecutado con exito")

def getCommand(name):
    packageManager = ToolsLocator.getPackageManager()
    pluginsManager = PluginsLocator.getManager()
    appfolder = pluginsManager.getApplicationFolder().getAbsolutePath()
    if packageManager.getOperatingSystemFamily()=="win":
        folder = "%s/gvSIG/extensiones/org.gvsig.gdal.app.mainplugin/gdal/bin/gdal/apps" % appfolder
    else:
        folder = "%s/gvSIG/extensiones/org.gvsig.gdal.app.mainplugin/gdal/" % appfolder
    pathname = "%s/%s" % (folder, name)
    pathname = pathname.replace("\\","/")
    return pathname


def rasterTools(*args):
    l=TransparencySRSAndOverviewsRasterTools()
    l.showWindow("Basic Raster Tools")


def main (*args):
    rasterTools()
