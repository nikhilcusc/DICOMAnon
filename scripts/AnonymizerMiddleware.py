import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import argparse
import os
import sys
import logging

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(scriptDirectory)
sys.path.append(parentDirectory)

from Common.Anonymizer import Anonymizer
from Common.Dcmtk import Dcmtk

# Check whether dcmtk library exists in same directory of script or back a directory
# Dcmtk library will be in same directory of script if running cx_frozen back-end
testDcmtkDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', r'dcmtk-3.6.6-win64-dynamic'))
if(os.path.isdir(testDcmtkDirectory)):
    ### Set directory path for dcmtk library ###
    dcmtkDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', r'dcmtk-3.6.6-win64-dynamic\bin'))
else:
    ### Set directory path for dcmtk library ###
    dcmtkDirectory = os.path.abspath(os.path.join(scriptDirectory, r'dcmtk-3.6.6-win64-dynamic\bin'))

# Check whether image headers folder exists in same directory of script or back a directory
# Image Headers library will be in same directory of script if running cx_frozen back-end
testImageHeaders = os.path.abspath(os.path.join(scriptDirectory, '..', 'ImageHeaders'))
if(os.path.isdir(testImageHeaders)):
    inputDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', 'ImageHeaders\Temporary\InputFiles'))
    inputDicomFileDirectory = inputDicomFileDirectory.replace("\\", "/")

    outputDicomFileDirectory = os.path.abspath(
    os.path.join(scriptDirectory, '..', 'ImageHeaders\Temporary\AnonymizedFiles'))

    downloadedDicomFileDirectory = os.path.abspath(
    os.path.join(scriptDirectory, '..', 'ImageHeaders\Temporary\DownloadedFiles'))
else:
    inputDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, 'ImageHeaders\Temporary\InputFiles'))
    inputDicomFileDirectory = inputDicomFileDirectory.replace("\\", "/")

    outputDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, 'ImageHeaders\Temporary\AnonymizedFiles'))

    downloadedDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, 'ImageHeaders\Temporary\DownloadedFiles'))


"""
Version X.Y
X: Major architectural change
Y: Minor patches
"""
ANONYMIZER_VERSION = "1.0"

description = """
Anonymizer Backend end Restful server

Can run the below command for development (automatically reloads upon save)
uvicorn AnonymizerMiddleware:app --reload --port 5000

Documentation for back-end: http://127.0.0.1:5000/docs#/
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

# Global variable for anonymizer class
anonymizer = Anonymizer([])

@app.post("/anonymize")
async def postAnonymizeData(inputDicomKey: List[UploadFile] = File(...)):
    """
    Copies input files to 'InputFiles' directory, anonymizes them, saves in 'AnonymizedFiles' directory,
    and pushes to Orthanc Server

    Parameters
    __________
    inputDicomKey: file object array
        Array of file objects to anonymize

    Returns
    _______
    "Done" if success". "Fail" otherwise
    """
    for f in os.listdir(inputDicomFileDirectory):
        os.remove(os.path.join(inputDicomFileDirectory, f))

    for f in os.listdir(outputDicomFileDirectory):
        os.remove(os.path.join(outputDicomFileDirectory, f))

    # Iterate through every file in directory
    for file in inputDicomKey:
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


@app.post("/updateAnonymizationTable")
async def updateAnonymizationTable(payload: dict=Body(...)):
    """
    Updates anonymizer's local array of group element tags

    Parameters
    __________
    payload: two-dimensional array
        Array of DICOM tags (group, element array) to anonymize

    Returns
    _______
    "Done" if success"
    """
    anonymizer.tagArray.clear()
    rawArray = payload.get('anonymizationArray')
    anonymizer.tagArray = rawArray
    return "Done"


@app.post("/query/{patientId}")
async def postQueryData(patientId: str):
    """
    Post Query/Receive G-GET command to Orthanc server based on patientId

    Parameters
    __________
    patientId: str
        Patient ID that must be query/retrieved

    Returns
    _______
    "Done" if success". "Fail" otherwise
    """

    for f in os.listdir(downloadedDicomFileDirectory):
        os.remove(os.path.join(downloadedDicomFileDirectory, f))

    ### Save downloaded files from Orthanc Server ###
    connection = Dcmtk(scriptDirectory, dcmtkDirectory, "localhost", "4242")

    runStatus = connection.cGet(patientId, downloadedDicomFileDirectory)
    if runStatus == 0:
        print('FATAL ERROR: Could not download images from the Orthanc server. One of the possible reasons could be incorrect patientID')
        return "Fail"
    else:
        print("Input images downloaded from Orthanc server and saved in "+ downloadedDicomFileDirectory)

    # add dcm extension to all downloaded files
    anonymizer.addDcmextension(downloadedDicomFileDirectory)

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
