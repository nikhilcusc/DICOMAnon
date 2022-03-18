import os
from pydicom import dcmread
import sys

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(scriptDirectory)
sys.path.append(parentDirectory)

from Common.Anonymizer import Anonymizer
from Common.Dcmtk import Dcmtk

# Output files
logFileName = "\log.txt"

if __name__ == "__main__":

    ### SET DIRECTORY PATHS ###

    inputDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', 'ImageHeaders'))
    inputDicomFilePath = inputDicomFileDirectory + "\image01.dcm"

    outputDicomFilePath = inputDicomFileDirectory + "\output.dcm"

    dcmtkDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', r'dcmtk-3.6.6-win64-dynamic\bin'))

    ### Anonymization ###

    anonymizer = Anonymizer()

    anonymizer.readDicomFile(inputDicomFilePath, log=False)

    anonymizer.removePrivateTags()

    anonymizer.removeTagsByGroup()

    anonymizer.saveAnonymizedFile(outputDicomFilePath, log=False)


    ### DICOM PUSH ###
    connection = Dcmtk(scriptDirectory, dcmtkDirectory, "localhost", "4242")

    # TODO: Define where change directory happens
    os.chdir(dcmtkDirectory)

    connection.cEcho(logFileName)

    connection.cStore(inputDicomFilePath)

    connection.cStore(outputDicomFilePath)

    # TODO: Define how we return to script directory
    os.chdir(scriptDirectory)


