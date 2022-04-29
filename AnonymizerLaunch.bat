@echo off
:: 
:: Please change the following two variables for your local machine
::
:: pathToProject should be set to the folder path of your cloned git repository
:: pathToMiniconda should be set to the folder path of your miniconda3 application
::
:: USER VARIABLES
set pathToProject=C:\Users\Adarsh\Documents\USC\BME528\FinalProject\DICOMAnon\
set pathToMiniconda=C:\Users\Adarsh\miniconda3\



:: PROGRAM VARIABLES
set "pathToDicomEnv=envs\DICOM_env"
set "frontEndFolder=AnonymizationApplication"
set "backEndFolder=scripts"
set "activateFolder=Scripts\activate.bat"

set "fullFrontEndPath=%pathToProject%%frontEndFolder%"
set "fullEnvironmentPath=%pathToMiniconda%%pathToDicomEnv%"
set "fullActivatePath=%pathToMiniconda%%activateFolder%"
set "fullBackEndPath=%pathToProject%%backEndFolder%"


title Front-end
start cmd.exe /k "cd /d %fullFrontEndPath% && %fullActivatePath% %fullEnvironmentPath% && mode con: cols=100 lines=20 && npm run serve"
title Back-end
start cmd.exe /k "cd /d %fullBackEndPath% && %fullActivatePath% %fullEnvironmentPath% && mode con: cols=100 lines=20 && uvicorn AnonymizerMiddleware:app --reload --port 5000"