import os
import subprocess

# TODO: Add doxygen comments for everything
class Dcmtk:
    def __init__(self, scriptDirectory, dcmtkDirectory, peer, port):
        self.scriptDirectory = scriptDirectory
        self.dcmtkDirectory = dcmtkDirectory
        self.peer = peer
        self.port = port

    def runByCmdExe(self, command):
        """
        Opens windows cmd terminal, runs command on command line and returns
        :param command: list
            List of strings that will be put into command line interface
        :return:
        TODO: Add handling for stdout
        """
        try:
            commandPrompt = subprocess.Popen(
                "cmd.exe", stdin=subprocess.PIPE, bufsize=0
            )
            commandPrompt.stdin.write(
                "{}\n".format(" ".join(command) + "\n").encode("utf-8")
            )
            commandPrompt.stdin.close()
        except Exception as e:
            raise Exception(
                "ERROR: Failed to execute " + str(command) + "Exception: " + e
            )

    # Send CEcho command
    def cEcho(self, logFileName):
        # TODO: Make so that this command doesn't lock logFile
        # TODO: Define better structure for log levels
        self.runByCmdExe(["echoscu", self.peer, self.port, "-ll", "debug", ">", self.scriptDirectory + logFileName])
        # TODO: Use echo errorlevel to assert that we always return 0 (i.e. PACS is connected)
        # runByCmdExe(["echo", "%errorlevel%"])

    # C-Store
    def cStore(self, filePath):
        # TODO: Add file output log
        self.runByCmdExe(["storescu", self.peer, self.port, filePath, "-xs", "--propose-lossless", "-ll", "info"])

    def readHelpFunction(self, command):
        os.chdir(self.dcmtkDirectory)
        # TODO: Add functionality to read help files for all 4 commands (echoscu, storescu, storescp, dcmdump)
        # runByCmdExe(["echoscu", "-h"])
        print(command)
        os.chdir(self.scriptDirectory)


