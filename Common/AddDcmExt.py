import os
import re
import logging

def addDCMextension(directory):
    renameCounter=0
    logging.debug('Adding extension to files in ' + directory)
    for file in os.listdir(directory):
        head, tail = os.path.splitext(file)
        if re.search("[0-9]{5,}",tail[1:]).start()==0: # if the last part of file name starts with numbers
            src = os.path.join(directory, file)
            dst = os.path.join(directory, file + '.dcm')
            
            if not os.path.exists(dst): # check if the file doesn't exist
                os.rename(src, dst)
                renameCounter+=1
    logging.debug('Added extension to ' + str(renameCounter) + ' files')
               
          