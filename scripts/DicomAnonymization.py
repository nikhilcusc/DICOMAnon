import os
from pydicom import dcmread
import sys
import logging

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
    logging.basicConfig(filename='anonymizer.log', level=logging.DEBUG)
    ### Anonymization ###

    anonymizer = Anonymizer()

    anonymizer.readDicomFile(inputDicomFilePath, log=False)

    anonymizer.removePrivateTags()

    anonymizer.removeTagsByGroup()
    logging.debug('Anonymization complete!')

    anonymizer.saveAnonymizedFile(outputDicomFilePath, log=False)
    logging.info('Anonymized DICOM saved')
    # TODO: creates output files even if anonymization fails, we should have a check before saving output dicom

    ### DICOM PUSH ###
    connection = Dcmtk(scriptDirectory, dcmtkDirectory, "localhost", "4242")

    connection.cEcho(logFileName)
    
    connection.cStore(inputDicomFilePath)
    logging.info('Unanonymized DICOM pushed to PACS')
    connection.cStore(outputDicomFilePath)
    logging.info('Anonymized pushed to PACS')


