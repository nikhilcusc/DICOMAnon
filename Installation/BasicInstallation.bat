@ECHO ON

PUSHD ..
SET dicomAnonymizationPipeline=%CD%
ECHO %dicomAnonymizationPipeline%
POPD

:: Location of miniconda intallation executable
SET minicondaDownloadPath = %USERPROFILE%\Downloads

:: Location of DICOM Pipeline conda environment
SET dicomEnv = %~sdp0..\venvs\dicom_conda_env.yml

:: Location of where miniconda will install to
SET minicondaInstallationPath = "%USERPROFILE%\AppData\Local\Continuum\miniconda3"

:: Install miniconda
ECHO Installing miniconda
CALL C:
CALL C:\Users\Adarsh\Downloads\Miniconda3-latest-Windows-x86_64.exe /S /D=%installPath0
ECHO Installed miniconda

:: Install DICOM Pipeline conda environment
powershell.exe unblock-file createDICOMCondaEnv.ps1
powershell.exe -ExecutionPolicy Bypass -Command "& '%~dp0\createDICOMCondaEnv.ps1' '%USERPROFILE%' '%dicomAnonymizationPipeline%'";

ECHO Set DICOM_PIPELINE_DIRECTORY
CALL setx DICOM_PIPELINE_DIRECTORY %dicomAnonymizationPipeline%

PAUSE