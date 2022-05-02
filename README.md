# DICOMAnon

USER INSTRUCTIONS FOR STANDALONE APPLICATION
--------------------------------------------
1) Install Orthanc PACS Simulator
    - Instructions: https://www.orthanc-server.com/resources/2015-02-09-emsy-tutorial/index.html
    - Configuration file will be located at 'C:\Program Files\Orthanc Server\Configuration\orthanc.json'
    
2) Add 'aec' as a client server of Orthanc
    -   Find the following block of code (line 311 of Orthanc Configuration file)
    
           // The list of the known DICOM modalities. This option is ignored if \
           // "DicomModalitiesInDatabase" is set to "true", in which case you \
           // must use the REST API to define modalities. \
           "DicomModalities" : { \
             /** \
              * Uncommenting the following line would enable Orthanc to \
     
    -   Add the following line to the DicomModalities array so it becomes
    
           // The list of the known DICOM modalities. This option is ignored if \
           // "DicomModalitiesInDatabase" is set to "true", in which case you \
           // must use the REST API to define modalities. \
           "DicomModalities" : { \
             "aec": [ "GETSCU", "localhost", 2000 ], \
             /** \
              * Uncommenting the following line would enable Orthanc to \

2) Clone 'DICOMAnon' github repository from https://github.com/nikhilcusc/DICOMAnon

3) Extract 'DICOM_Anon/AnonymizationApplication/AnonymizationApplication.zip' to your local machine

4) Run 'AnonymizationApplication/Anonymizer.bat'

5) Temporary files hold anonymized and query/retrieved DICOM images
    - Query/Retrieved Files: AnonymizationApplication\exe.win-amd64-3.7\ImageHeaders\Temporary\DownloadedFiles
    - Anonymized Files: AnonymizationApplication\exe.win-amd64-3.7\ImageHeaders\Temporary\AnonymizedFiles



DEVELOPER INFORMATION
---------------------

To run the UI as a developer, one can either use thes provided .bat file or do it entirely manually

Regardless of method, Temporary files hold anonymized and query/retrieved DICOM images
    - Query/Retrieved Files placed at: DICOMAnon\ImageHeaders\Temporary\DownloadedFiles
    - Anonymized Files placed at: DICOMAnon\ImageHeaders\Temporary\AnonymizedFiles

.BAT FILE METHOD

1) Clone 'DICOMAnon' github repository from https://github.com/nikhilcusc/DICOMAnon

2) Install miniconda3 from https://docs.conda.io/en/latest/miniconda.html

3) Open miniconda3 command prompt
    - Change directory to 'DICOMAnon/_venvs' folder
    = Type 'conda env create --file DICOM_Env.yml' and press enter
    - Type 'conda activate DICOM_Env'

4) Download node.js from https://nodejs.org/en/download/

5) Change directory to 'DICOMAnon/AnonymizationApplication'

6) Type 'npm run install' and press enter

7) Change directory to 'DICOMAnon' root folder

8) Double-click AnonymizerLaunch.bat and use UI



MANUAL METHOD FOR FRONT-END

To run front-end as developer, do the following (assumes .bat file method has been completed)
1) Change directory to 'DICOMAnon/AnonymizationApplication'
2) Type 'npm run serve' and press enter
3) Front-end will be hosted at http://localhost:8080/

MANUAL METHOD FOR BACK-END

To run back-end as developer, do the following:
1) Open miniconda3 command prompt
    - Change directory to 'DICOMAnon/scripts' folder
    - Type 'conda activate DICOM_Env' and press enter (assumes .bat file method has been completed)
    - Type 'uvicorn AnonymizerMiddleware:app --reload --port 5000' and press enter
2) Back end will be hosted at http://127.0.0.1:5000/
3) Documentation of API and back-end hosted at http://127.0.0.1:5000/docs



BUILD INFORMATION
---------------------

FRONT-END

To create build version of front-end, do the following (assumes .BAT FILE METHOD section completed):
1) Change directory to 'DICOMAnon/AnonymizationApplication'
2) Type 'npm run electron:build' and press enter
3) Run 'DICOMAnon/AnonymizationApplication/dist_electron/win-unpacked/vue-electron-app.exe' to launch front-end

BACK-END

To create build version of back-end, do the following (assumes .BAT FILE METHOD section completed):
1) Change directory to 'DICOMAnon/scripts'
2) Type 'python setup.py build' and press enter
3) Run 'DICOMAnon/scripts/build/exe.win-amd64-3.7/AnonymizerMiddleware.exe'
