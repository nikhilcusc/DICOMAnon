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

from pydicom import dcmread
import logging
from Common.DicomTags import DicomTags


class Anonymizer:
    """
    Base class for anonymization of DICOM Files
    """
    def __init__(self):

        # Individual DICOM dataset to be anonymized
        self.dataset = None

        # DICOM Tag Object containing dictionary structures
        self.dicomTagObject = DicomTags()


    def _deleteTagCallback(self, dataset, dataElement):
        """
        Internal callback function to delete a given dataset's elements if it belongs to the deleteTagArray

        Returns
        _______
        None
        """

        # Get tags that should be deleted
        deletedTagArray = (self.dicomTagObject.getDeleteTagArray())

        # Delete tags if they are in array
        if dataElement.tag in deletedTagArray:
            logging.debug("The following tag has been deleted ----> " + str(dataset[dataElement.tag]))
            del dataset[dataElement.tag]


    def _dummyTagCallback(self, dataset, dataElement):
        """
        Internal callback function to set a given dataset's elements to a dummy value if it belongs to the deleteTagArray

        Returns
        _______
        None
        """

        # Get tags that need to be replaced with dummy value
        dummyTagArray = (self.dicomTagObject.getDummyTagArray())

        # Replace tags if they are in array
        if dataElement.tag in dummyTagArray:
            logging.debug("The following tag has been replaced----> " + str(dataset[dataElement.tag]))
            # Check if tags should be replaced with an integer value or 'None' string
            if dataElement.VR in self.dicomTagObject.integerVrKeys:
                dataElement.value = 0
            else:
                dataElement.value = "None"


    def anonymizeTags(self):
        """
        Used to delete and set dummy values for all relevant DICOM tags

        Returns
        _______
        None
        """

        # Walk through DICOM dataset and delete appropriate tags
        self.dataset.walk(self._deleteTagCallback)

        # Walk through DICOM dataset and set appropriate tags to dummy value
        self.dataset.walk(self._dummyTagCallback)


    def readDicomFile(self, inputFilePath):
        """
        Reads input DICOM File and returns a dictionary of DICOM tags

        Parameters
        __________
        inputFilePath: str
            Path to individual .dcm DICOM file

        Returns
        _______
        dataset: FileDataSet
            A dictionary structure representing a parsed DICOM file
        """
        self.dataset = dcmread(inputFilePath)
        logging.info('Reading DICOM files')
        return self.dataset


    def saveAnonymizedFile(self, outputFilePath):
        """
        Saves DICOM File to file location

        Parameters
        __________
        outputFilePath: str
            Path to output .dcm DICOM file

        Returns
        _______
        None
        """
        logging.info('Saving DICOM file')
        if self.dataset is None:
            raise ValueError('Must call readDicomFile before attempting to save dicom file')

        self.dataset.save_as(outputFilePath)


    def removePrivateTags(self):
        """
        Removes any private tags from DICOM file that are not part of DICOM Standard

        Parameters
        __________
        None

        Returns
        _______
        None
        """
        logging.info('Removing DICOM file private tags')
        if self.dataset is None:
            raise ValueError('Must call readDicomFile before attempting to remove private tags')

        self.dataset.remove_private_tags()
