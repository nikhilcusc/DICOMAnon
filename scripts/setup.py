import sys
from cx_Freeze import setup, Executable

##########
#### Run "python setup.py build" in order to build cx_freeze of AnonymizerMiddleware back-end
##########

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "packages": ["argparse", "ctypes", "jinja2", "logging.config", "os", "pydicom", "re", "sys", "typing", "uvicorn", "fastapi",],
    "include_files": ["../Common", "../dcmtk-3.6.6-win64-dynamic", "../ImageHeaders","C:/Users/Adarsh/miniconda3/envs/DICOM_Env/Library/bin"],
    "excludes": []}


setup(
    name="Anonymization",
    version="0.1",
    description="DICOM Anonymization application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("AnonymizerMiddleware.py")],
)