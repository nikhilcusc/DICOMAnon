from pydicom import dcmread
import logging

# TODO: Add doxygen comments for everything
class Anonymizer:
    def __init__(self):
        self.anonymizedTagArray = [0x10]  # TODO: Adding 0x8  causes problems due to minimal set for DICOM image (0x8, 0x15)
        self.anonymizedValueArray = ["PN"]
        self.dataset = None # TODO: Does this need to be more than a variable when handling series of images

    # Read input DICOM file
    def readDicomFile(self, inputFilePath, log=False):
        self.dataset = dcmread(inputFilePath)
        if log:
            print(self.dataset)
        return self.dataset

    def saveAnonymizedFile(self, outputFilePath, log=False):
        # Save new anonymized file
        if log:
            print(self.dataset)
        self.dataset.save_as(outputFilePath)

    # Remove any private tags not part of DICOM Standard
    def removePrivateTags(self):
        # TODO: Add error handling for when dataset is None
        logging.debug('Removing private tags!')
        self.dataset.remove_private_tags()

    # Iterating through elements in dataset
    # Delete elements who have tags present in anonymizedTagArray
    def removeTagsByGroup(self):
        logging.debug('Removing tags by group!')
        self.dataset.walk(self.deleteByTagGroupCallback)

    # Delete elements according to Value Representation (may be useful)
    # https://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html
    def deleteByValueRepresentationCallback(self, dataset, data_element):
        # Potentially useless if we are deleting by tags anyway
        if data_element.VR == "PN":
            data_element.value = "anonymous"

    # Delete elements by tag group (i.e. 0x8 or 0x10 for PHI)
    def deleteByTagGroupCallback(self, dataset, data_element):
        if data_element.tag.group in self.anonymizedTagArray:
            del dataset[data_element.tag]