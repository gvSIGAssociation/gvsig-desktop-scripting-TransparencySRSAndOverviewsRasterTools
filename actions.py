# encoding: utf-8

import gvsig
from gvsig import getResource

import os.path

from os.path import join, dirname

from gvsig import currentView
from gvsig import currentLayer

from java.io import File

from org.gvsig.app import ApplicationLocator
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator

from addons.TransparencySRSAndOverviewsRasterTools.basicRasterTools import rasterTools
  
from org.gvsig.tools import ToolsLocator

def trace(msg):
  #print "###> ", msg
  pass
  
class RasterToolsExtension(ScriptingExtension):
  def __init__(self):
    pass

  def isVisible(self):
    return True

  def isEnabled(self):
    return True

  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "tools-basicrastertools":
        rasterTools()
      
def selfRegister():
  i18n = ToolsLocator.getI18nManager()
  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  icon = File(getResource(__file__,"images","tools-basicrastertools.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.TransparencySRSAndOverviewsRasterTools", "action", "tools-basicrastertools", None, icon)

  extension = RasterToolsExtension()
  action = actionManager.createAction(
    extension,
    "tools-basicrastertools",   # Action name
    "Basic Raster Tools",   # Text
    "tools-basicrastertools", # Action command
    "tools-basicrastertools",   # Icon name
    None,                # Accelerator
    900500000,          # Position
    i18n.getTranslation("_Basic_Raster_Tools")    # Tooltip
  )
  action = actionManager.registerAction(action)

  # Añadimos la entrada "gdal tools" en el menu herramientas
  application.addMenu(action, "tools/_Basic_Raster_Tools")
  # Añadimos el la accion como un boton en la barra de herramientas "gdaltools".
  application.addSelectableTool(action, "basicRasterTools")

def main(*args):
  #selfRegister()
  icon = File(getResource(__file__,"images","tools-basicrastertools.png")).toURI().toURL()
  print icon
  icon.openStream()
  print 'VA'
  