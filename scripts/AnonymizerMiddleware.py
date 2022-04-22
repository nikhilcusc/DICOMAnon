import uvicorn
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import Schemas
import logging
import asyncio
import argparse
import os
import sys
import logging

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(scriptDirectory)
sys.path.append(parentDirectory)

### Set directory path for dcmtk library ###
dcmtkDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', r'dcmtk-3.6.6-win64-dynamic\bin'))

from Common.Anonymizer import Anonymizer
from Common.Dcmtk import Dcmtk
from Common.AddDcmExt import addDCMextension

# Output files
logFileName = 'anonymizer.log'

# Boolean defines whether input dicom images will be uploaded
# DEMO ONLY
uploadInputFiles = False

# Boolean defines whether anonymized dicom images will be uploaded
uploadAnonymizedFiles = True

inputDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', 'ImageHeaders\InputFiles'))
inputDicomFileDirectory = inputDicomFileDirectory.replace("\\", "/")

outputDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', 'ImageHeaders\AnonymizedFiles'))

downloadedDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', 'ImageHeaders\DownloadedFiles'))


"""
Version Format: X.Y.Z
X: Major version: Incremented whenever major changes are made like
   architectural change.
Y: Minor version: Incremented whenever minor changes are made which does not
   breaks the API  (i.e. new endpoints' added, or changes in the endpoints
   behaviour).
Z: Patch version: Incremented with bug fixes.
"""
ANONYMIZER_VERSION = "0.0.1"

"""
Anonymizer Backend end Restful server and websocket.

Run cmd:
    uvicorn AnonymizerMiddleware:app --reload --port 5000

Documentation:
    http://127.0.0.1:5000/docs#/
"""

description = """
Anonymization Backend Server

## Rest

Rest server to communicate with Anonymization framework.

"""

app = FastAPI(
    title="AnonymizerMiddleware", description=description, version=ANONYMIZER_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=Schemas.ServerPing)
async def isServerRunning():
    """
    Simple command for externals to check if the server is running.
    """
    return {
        "message": "Anonymizer server is Running",
        "version": ANONYMIZER_VERSION,
    }

@app.post("/anonymize")
async def postAnonymizeData(inputDicomKey: List[UploadFile] = File(...)):
    """
    Copies input files to 'InputFiles' directory, anonymizes them, saves in 'AnonymizedFiles' directory, and pushes to Orthanc Server
    """
    print("In Anonymizer python code")

    anonymizer = Anonymizer()

    for f in os.listdir(inputDicomFileDirectory):
        os.remove(os.path.join(inputDicomFileDirectory, f))

    for f in os.listdir(outputDicomFileDirectory):
        os.remove(os.path.join(outputDicomFileDirectory, f))

    for file in inputDicomKey:
        # inputDicomFilePath = cwd + "/ImageHeaders/InputFiles/" + file.filename
        # outputDicomFilePath = cwd + "/ImageHeaders/AnonymizedFiles/" + file.filename
        inputDicomFilePath = inputDicomFileDirectory + "/" + file.filename
        outputDicomFilePath = outputDicomFileDirectory + "/" + file.filename

        contents = await file.read()
        with open(inputDicomFilePath, "wb") as f:
            f.write(contents)
            f.close()

        # Read DICOM File (stored in anonymizer class as self.dataset)
        anonymizer.readDicomFile(inputDicomFilePath)

        # Remove private tags from DICOM file
        anonymizer.removePrivateTags()

        # Remove/modify tags based on DicomTags class
        anonymizer.anonymizeTags()

        # Save anonymized files to output location
        anonymizer.saveAnonymizedFile(outputDicomFilePath)

    print("All files in Input DICOM Directory have been anonymized")

    ### Push output files to Orthanc Server ###
    connection = Dcmtk(scriptDirectory, dcmtkDirectory, "localhost", "4242")

    # Check connection with Orthanc Server is secure
    runStatus = connection.cEcho()
    logging.debug('cEcho run status ' + str(runStatus))
    if runStatus == 0:
        print('FATAL ERROR: Could not connect to Orthanc server')
        return "Fail"
    else:
        # Upload output anonymized DICOM files to Orthanc
        runStatus = connection.cStore(outputDicomFileDirectory, individualFile=False)
        if runStatus == 0:
            print('FATAL ERROR: Could not store anonymized images in Orthanc server')
            return "Fail"
        else:
            print("Anonymized images pushed to Orthanc server")

    return "Done"

@app.post("/query/{patientId}")
async def postQueryData(patientId: str):
    """
    Simple command to post query data
    """
    print("In Query python code")
    print(patientId)

    for f in os.listdir(downloadedDicomFileDirectory):
        os.remove(os.path.join(downloadedDicomFileDirectory, f))

    ### Save downloaded files from Orthanc Server ###
    connection = Dcmtk(scriptDirectory, dcmtkDirectory, "localhost", "4242")

    runStatus = connection.cGet(patientId, downloadedDicomFileDirectory)
    if runStatus == 0:
        print('FATAL ERROR: Could not download images from the Orthanc server. One of the possible reasons could be incorrect  patientID')
        return "Fail"
    else:
        print("Input images downloaded from Orthanc server and saved in "+ downloadedDicomFileDirectory)

    # add dcm extension to all downloaded files
    addDCMextension(downloadedDicomFileDirectory)
    return "Done"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="set log level to DEBUG instead of FATAL",
    )

    args = parser.parse_args()
    logLevel = logging.DEBUG if args.verbose else logging.FATAL

    logging.basicConfig(level=logLevel)
    uvicorn.run(app=app, host="127.0.0.1", port=5000)
