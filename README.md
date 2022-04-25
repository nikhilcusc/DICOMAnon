# DICOMAnon
------------------------------
To run Development application, do the following:
1) Activate DICOM_Env virtual environment, cd to Common directory, run "uvicorn AnonymizerMiddleware:app --reload --port 5000"
2) Activate DICOM_Env virtual environment, cd to AnonymizerApplication directory, type "npm run serve"
3) Need to install Orthanc PACS Simulator as well and add 'aec' as client
4) Documentation for back-end: http://127.0.0.1:5000/docs#/
------------------------------
