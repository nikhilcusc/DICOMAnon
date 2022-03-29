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

from pydicom import dcmread

class Anonymizer:
    """
    Base class for anonymization of DICOM Files
    """
    def __init__(self):
        # Array of DICOM Tags that need to be anonymized
        # TODO: Adding 0x8  causes problems due to minimal set for DICOM image (0x8, 0x15)
        self.anonymizedTagArray = [0x10]

        # Array of DICOM Values that need to be anonymized
        self.anonymizedValueArray = ["PN"]

        # Individual DICOM dataset to be anonymized
        self.dataset = None


    def readDicomFile(self, inputFilePath, log=False):
        """
        Reads input DICOM File and returns a dictionary of DICOM tags

        Parameters
        __________
        inputFilePath: str
            Path to individual .dcm DICOM file

        log: bool
            Prints to command line as debug tool

        Returns
        _______
        dataset: FileDataSet
            A dictionary structure representing a parsed DICOM file
        """
        self.dataset = dcmread(inputFilePath)
        logging.debug('Reeading DICOM files.')
        return self.dataset


    def saveAnonymizedFile(self, outputFilePath, log=False):

        """
        Saves DICOM File to file location

        Parameters
        __________
        outputFilePath: str
            Path to output .dcm DICOM file

        log: bool
            Prints to command line as debug tool

        Returns
        _______
        None
        """
        # Save new anonymized file
        logging.debug('Saving Anonymized file.')
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
        # TODO: Add error handling for when dataset is None
        self.dataset.remove_private_tags()


    def removeTagsByGroup(self):
        """
        Removes any DICOM tags from DICOM file based on group value

        Parameters
        __________
        None

        Returns
        _______
        None
        """
        self.dataset.walk(self.deleteByTagGroupCallback)


    def deleteByTagGroupCallback(self, dataset, dataElement):
        """
        Iterates through elements in dataset and removes elements who have a tag group present in anonymizedTagArray

        Parameters
        __________
        dataset: FileDataSet
            A dictionary structure representing a parsed DICOM file

        data_element: DcmElement
            Data element within DICOM file

        Returns
        _______
        None
        """
        if dataElement.tag.group in self.anonymizedTagArray:
            del dataset[dataElement.tag]


    # TODO: Determine if this function is necessary
    # Delete elements according to Value Representation (may be useful)
    # https://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html
    def deleteByValueRepresentationCallback(self, dataset, data_element):
        """
        Call-back function that removes

        Parameters
        __________
        None

        Returns
        _______
        None
        """
        # Potentially useless if we are deleting by tags anyway
        if data_element.VR == "PN":
            data_element.value = "anonymous"