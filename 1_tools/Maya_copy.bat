::@echo off 

set "SCRIPT_PATH=O:/pythons/"
set "PYTHONPATH = %SCRIPT_PATH%;%PYTHONPATH%"

set "MAYA_PLUG_IN_PATH=%SCRIPT_PATH%plugins/;%MAYA_PLUG_IN_PATH%"
set "MAYA_SHELF_PATH=%SCRIPT_PATH%shelf;%MAYA_SHELF_PATH%"

set "MAYA_DISABLE_CIP=1"
set "MAYA_DISABLE_CER=1"

start "" "C:/Program Files/Autodesk/Maya2024/bin/maya.exe"

::exit 