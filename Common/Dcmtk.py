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

import subprocess
import logging

class Dcmtk:
    """
    Base class for communication with PACS Server (Orthanc)
    """
    def __init__(self, scriptDirectory, dcmtkDirectory, peer, port):
        # Directory where main .py file is run from
        self.scriptDirectory = scriptDirectory

        # Directory where dcmtk library exists
        self.dcmtkDirectory = dcmtkDirectory

        # IP address on machine for Orthanc Server
        self.peer = peer

        # Port number on machine for Orthanc Server
        self.port = port


    def runByCmdExe(self, command):
        """
        Runs any command on command line based on passed in parameters

        Parameters
        __________
        command: arr
            Array of strings that are joined together before being executed on command line

        Returns
        _______
        runStatus
        """
        runStatus=1
        try:
            commandPrompt = subprocess.Popen(
                "cmd.exe", stdin=subprocess.PIPE, bufsize=0,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            commandPrompt.stdin.write(
                "{}\n".format(" ".join(command) + "\n").encode("utf-8")
            )
            
            output, unused_error = commandPrompt.communicate()
            output = str(output)
            logging.debug('\n\ncmd output is ' + output)
            fCount = output.count('Failed')
            if ('Error') in output or fCount>1:
                #logging.error("ERROR: Failed to execute " + str(command))
                raise Exception('Failed to execute command')

        except Exception as e:
            logging.error("ERROR: Failed to execute " + str(command))
            #raise Exception("ERROR: Failed to execute " + str(command) + "Exception: " + e)
            runStatus=0

        commandPrompt.stdin.close()
        commandPrompt.stdout.close()
        commandPrompt.stderr.close()
        return runStatus


    def cEcho(self):
        """
        Sends C-ECHO command to assert connection with PACS Server

        Parameters
        __________
       
        Returns
        _______
        runStatus
        """
        return self.runByCmdExe([self.dcmtkDirectory + "\echoscu", self.peer, self.port])


    def cStore(self, filePath, individualFile=True):
        """
        Sends C-STORE command to upload file/s into PACS Server

        Parameters
        __________
        filePath: file
            Path to input DICOM file or file directory which is to be uploaded into PACS Server

        individualFile: bool
            True means filePath is individualFile. False means filePath is file directory containing many .dcm

        Returns
        _______
        runStatus
        """
        if individualFile:
            return self.runByCmdExe([self.dcmtkDirectory + "\storescu", self.peer, self.port, filePath, "-xs", "--propose-lossless", "-ll", "info"])
        else:
            return self.runByCmdExe(
                [self.dcmtkDirectory + "\storescu", self.peer, self.port, filePath, "+sd", "-xs", "--propose-lossless", "-ll", "info"])


    def readHelpFunction(self, command):
        """
        Sends command to get help information for provided command and display on command line

        Parameters
        __________
        command: str
            Command that user wants information on

        Returns
        _______
        None
        """
        self.runByCmdExe([self.dcmtkDirectory + command, "-h"])


    def cGet(self, patientID, outputDir):
        """
        Sends C-GET command to retrieve file/s from PACS Server
        
        Needs the following entry in the DicomModalities section of your Orthanc configuration file
        "getscu" : [ "GETSCU", "localhost", 2000 ]
        Please make sure to restart Orthanc with the updated configuration file.

        Parameters
        __________
        outputDir: string
            Path to location where DICOM files are to be downloaded

        Returns
        _______
        runStatus
        """
        return self.runByCmdExe([self.dcmtkDirectory + "\getscu", self.peer, self.port, '-aec ORTHANC', '-k "0008,0052=PATIENT"', '-k "0010,0020='+ str(patientID) + '"',  ' -v -od', outputDir + '\\'])