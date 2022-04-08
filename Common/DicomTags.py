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


class DicomTags:
    """
    DICOM Tag dictionaries with Group and Element number
    Anonymization tags based on Section 3.15 Appendix E of DICOM Standard
    Tags are either deleted or set to a dummy value based on Table E.1-1a. De-identification Action Codes

    """
    def __init__(self):

        # These tags will be deleted during the anonymization process
        self.deleteTags = [
            {"Group": 0x10, "Element": 0x12},
        ]

        # These tags will be set to a dummy value during the anonymization process
        self.dummyTags = [
            {"Group": 0x10, "Element": 0x0010}, # Patient Name
            {"Group": 0x10, "Element": 0x0020}, # Patient ID
            {"Group": 0x10, "Element": 0x0030}, # Patient's Birth Date
            {"Group": 0x10, "Element": 0x0040}, # Patient's Sex
            {"Group": 0x10, "Element": 0x1000}, # Other Patient IDs
            {"Group": 0x10, "Element": 0x1001}, # Other Patient Names
            {"Group": 0x10, "Element": 0x1005}, # Patient's Birth Name
            {"Group": 0x10, "Element": 0x1080}, # Military Rank
            {"Group": 0x10, "Element": 0x1010}, # Patient's Age
            {"Group": 0x10, "Element": 0x2154}, # Patient's Telephone Numbers
            {"Group": 0x10, "Element": 0x2155}, # Patient's Telecom Information
            {"Group": 0x10, "Element": 0x2180}, # Occupation
            {"Group": 0x10, "Element": 0x21B0}, # Additional Patient's History
            {"Group": 0x10, "Element": 0x2297}, # Responsible Person
            {"Group": 0x10, "Element": 0x2298}, # Responsible Person Role
            {"Group": 0x10, "Element": 0x2299}, # Responsible Organization
            {"Group": 0x10, "Element": 0x4000}, # Patient Comments

            {"Group": 0x08, "Element": 0x0020}, # Study Date
            {"Group": 0x08, "Element": 0x0030}, # Study Time
            {"Group": 0x08, "Element": 0x0050}, # Accession Number
            {"Group": 0x08, "Element": 0x0080}, # Institution Name
            {"Group": 0x08, "Element": 0x0081}, # Institution Address
            {"Group": 0x08, "Element": 0x0090}, # Referring Physician's Name
            {"Group": 0x08, "Element": 0x0096}, # Referring Physician's Identification sequence
            {"Group": 0x08, "Element": 0x1048}, # Physician(s) of Record
            {"Group": 0x08, "Element": 0x1049}, # Physician(s) of Record Identification Sequence
            {"Group": 0x08, "Element": 0x1060}, # Name of Physician(s) Reading Study
            {"Group": 0x08, "Element": 0x1062}, # Physician Reading Study Identification Sequence
        ]

        # These 'Value Representation' keys within a data element signify the element can be represented by an integer
        # See Section 3.5, 6.2 of DICOM Standard
        self.integerVrKeys = ["AT", "FL", "FD", "OB", "OD", "OF", "OL", "OV", "OW", "SL", "SQ", "SS", "SV",
                              "UL", "UN", "US", "UV"]


    def getDeleteTagArray(self):
        """
        Appends each element's group and element value within deleteTags to nested array

        Parameters
        __________

        Returns
        _______
        appendedArray: arr
            Array of DICOM tag elements, each containing a group and element value
        """

        appendedArray = []

        for element in self.deleteTags:
            miniArray = []
            miniArray.append(element["Group"])
            miniArray.append(element["Element"])
            appendedArray.append(miniArray)

        return appendedArray


    def getDummyTagArray(self):
        """
        Appends each element's group and element value within dummyTags to nested array

        Parameters
        __________

        Returns
        _______
        appendedArray: arr
            Array of DICOM tag elements, each containing a group and element value
        """

        appendedArray = []

        for element in self.dummyTags:
            miniArray = []
            miniArray.append(element["Group"])
            miniArray.append(element["Element"])
            appendedArray.append((miniArray))

        return appendedArray
