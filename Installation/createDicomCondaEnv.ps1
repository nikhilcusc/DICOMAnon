Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
write-output "Powershell script is executing"

# User Profile
$userprofile = $args[0]

# Location of miniconda installation path
$installationPath = [IO.Path]::Combine($userprofile, 'AppData\Local\Continuum\miniconda3')

# Add to environment PATH variable
$Env:PATH += $installationPath + ";"

# Location of DICOM Project folder
$dicomFolder = $args[1]
$condaPath = join-path "$installationPath" "condabin"

$condaBatFile = "conda.bat"
$dicomFolderPath = Split-Path -Path $dicomFolder -Qualifier

# Change to dicomFolderPath and create environment
Set-Location $dicomFolderPath
start-process $condaPath\$condaBatFile -ArgumentList "env", "create", "--file", "C:\Users\Adarsh\Documents\USC\BME528\FinalProject\DICOMAnonymizationPipeline\_venvs\DICOM_Env.yml" -Wait
Write-Output "Created DICOM environment"