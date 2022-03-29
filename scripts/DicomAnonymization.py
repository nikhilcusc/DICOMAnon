# Copyright 2022
# All rights reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(scriptDirectory)
sys.path.append(parentDirectory)

from Common.Anonymizer import Anonymizer
from Common.Dcmtk import Dcmtk

# Output files
logFileName = 'anonymizer.log'

# Boolean defines whether input dicom images will be uploaded along with anonymized dicom files
uploadInputFiles = True

if __name__ == "__main__":

    ### Set directory paths for input and anonymization DICOM files ###

    inputDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', 'ImageHeaders\InputFiles'))
    outputDicomFileDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', 'ImageHeaders\AnonymizedFiles'))

    ### Set directory path for dcmtk library ###
    dcmtkDirectory = os.path.abspath(os.path.join(scriptDirectory, '..', r'dcmtk-3.6.6-win64-dynamic\bin'))

    ### Anonymization of input files ###
    logging.basicConfig(filename=logFileName, level=logging.DEBUG)

    anonymizer = Anonymizer()

    # iterate over files in inputDicomFileDirectory, anonymize those files, and save them in outputDicomFileDirectory
    for filename in os.listdir(inputDicomFileDirectory):

        # Get file paths to input and output locations
        inputDicomFilePath = os.path.join(inputDicomFileDirectory, filename)
        outputDicomFilePath = os.path.join(outputDicomFileDirectory, filename)

        # Read DICOM File (stored in anonymizer class as self.dataset)
        anonymizer.readDicomFile(inputDicomFilePath, log=False)

        # Remove private tags from DICOM file
        anonymizer.removePrivateTags()

        # Remove group tags based on anonymization class
        anonymizer.removeTagsByGroup()

        # Save anonymized files to output location
        anonymizer.saveAnonymizedFile(outputDicomFilePath, log=False)


    ### Push output files to Orthanc Server ###
    connection = Dcmtk(scriptDirectory, dcmtkDirectory, "localhost", "4242")

    # TODO: Define where change directory happens
    # Change directory to dcmtk library (required to run PACS commands)
    os.chdir(dcmtkDirectory)

    # Check connection with Orthanc Server is secure
    connection.cEcho(logFileName)

    # Upload input DICOM files to Orthanc as point of comparison if user desires it
    if uploadInputFiles:
        connection.cStore(inputDicomFileDirectory, individualFile=False)

    # Upload output anonymized DICOM files to Orthanc
    connection.cStore(outputDicomFileDirectory, individualFile=False)

    # TODO: Define how we return to script directory
    # Change directory back to script directory
    os.chdir(scriptDirectory)
