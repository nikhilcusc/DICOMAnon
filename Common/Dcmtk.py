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
        None
        """
        try:
            commandPrompt = subprocess.Popen(
                "cmd.exe", stdin=subprocess.PIPE, bufsize=0
            )
            commandPrompt.stdin.write(
                "{}\n".format(" ".join(command) + "\n").encode("utf-8")
            )
            
            commandPrompt.stdin.close()
            output, unused_error = commandPrompt.communicate()
            logging.debug('cmd output is ' + str(output) + '\n unused error is ' + str(unused_error))
        except Exception as e:
            raise Exception(
                "ERROR: Failed to execute " + str(command) + "Exception: " + e
            )
         


    def cEcho(self, logFileName):
        """
        Sends C-ECHO command to assert connection with PACS Server

        Parameters
        __________
        logFileName: file
            Path to log file which stores output from executed command line

        Returns
        _______
        None
        """
        # TODO: Make so that this command doesn't lock logFile
        # TODO: Define better structure for log levels
        self.runByCmdExe([self.dcmtkDirectory + "\echoscu", self.peer, self.port, "-ll", "debug", ">", self.scriptDirectory + logFileName])
        # TODO: Use echo errorlevel to assert that we always return 0 (i.e. PACS is connected)
        # runByCmdExe(["echo", "%errorlevel%"])


    def cStore(self, filePath, individualFile = True):
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
        None
        """
        # TODO: Add file output log
        if individualFile:
            self.runByCmdExe([self.dcmtkDirectory + "\storescu", self.peer, self.port, filePath, "-xs", "--propose-lossless", "-ll", "info"])
        else:
            self.runByCmdExe(
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


