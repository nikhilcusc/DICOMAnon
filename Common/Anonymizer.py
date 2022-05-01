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
import re
import sys

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(scriptDirectory)
sys.path.append(parentDirectory)

from pydicom import dcmread # part of DICOM_Env conda environment
import logging
from Common.DicomTags import DicomTags


class Anonymizer:
    """
    Base class for anonymization of DICOM Files
    """
    def __init__(self, tagList):

        # Individual DICOM dataset to be anonymized
        self.dataset = None

        # DICOM Tag Object containing dictionary structures
        self.dicomTagObject = DicomTags()

        # DICOM Tag Element Array
        self.tagArray = tagList


    def _deleteTagCallback(self, dataset, dataElement):
        """
        Internal callback function to delete a given dataset's elements if it belongs to the deleteTagArray

        Returns
        _______
        None
        """

        # Get entire list of tags that should be deleted
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
        # Replace tags if they are in array
        if dataElement.tag in self.tagArray:
            logging.debug("The following tag has been replaced----> " + str(dataset[dataElement.tag]))
            # Check if tags should be replaced with an integer value or 'None' string
            if dataElement.VR in self.dicomTagObject.integerVrKeys:
                dataElement.value = 0
            else:
                dataElement.value = "None"


    def addDcmextension(self, directory):
        """
        Function to add a .dcm extension to each file within a given directory

        Parameters
        __________
        directory: str
            Path to directory of DICOM images

        Returns
        _______
        None
        """

        # Counter of how many files had .dcm extension attached
        renameCounter = 0
        logging.debug('Adding extension to files in ' + directory)

        # Iterate through directory and append .dcm extension
        for file in os.listdir(directory):
            head, tail = os.path.splitext(file)
            fileNameTail = re.search("[0-9]{5,}", tail[1:])
            if fileNameTail == None:
                continue
            if fileNameTail.start() == 0:  # if the last part of file name starts with numbers
                src = os.path.join(directory, file)
                dst = os.path.join(directory, file + '.dcm')

                if not os.path.exists(dst):  # check if the file doesn't exist
                    os.rename(src, dst)
                    renameCounter += 1

        logging.debug('Added extension to ' + str(renameCounter) + ' files')


    def anonymizeTags(self):
        """
        Used to delete and set dummy values for all relevant DICOM tags

        Returns
        _______
        None
        """
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
