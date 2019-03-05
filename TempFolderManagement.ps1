$Action = New-ScheduledTaskAction -Execute 'Powershell.exe' -Argument '

#Generate Unique name for log file
$RootName = "Log-"
$LogDate = Get-Date -Format FileDate
$FileName = $RootName + $LogDate

$(
#Declare path
$Path = "C:\Windows\Temp"

#Get total size of directory, count folders, and count files recursively
$TotalSize = "{0:N2} MB" -f ((Get-ChildItem $Path -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum /1MB)
$NumFolders = Get-ChildItem $Path -Directory | Measure-Object | %{$_.Count}
$NumFiles = Get-ChildItem $Path -File -Recurse | Measure-Object | %{$_.Count}

#Prints found values
"Total Size:" , $TotalSize, "Folders:" , $NumFolders, "Files:" , $NumFiles | Out-String 

#Declare Date time period for Deletion
$Today = Get-Date
$DaysAgo = "-1"
$ToDelete = $Today.AddDays($DaysAgo)

#deletes files whos creation date is more than 24 hours ago.
Get-ChildItem $Path -Recurse | Where-Object { $_.CreationTime -lt $ToDelete } | Remove-Item -Recurse -ErrorAction SilentlyContinue

#Gets new total size of directory, new count of folders, and new count of files recursively. 
$NewTotalSize = "{0:N2} MB" -f ((Get-ChildItem $Path -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum /1MB)
$NewNumFolders = Get-ChildItem $Path -Directory | Measure-Object | %{$_.Count}
$NewNumFiles = Get-ChildItem $Path -File -Recurse | Measure-Object | %{$_.Count}

#Prints new found values
"New Total Size:" , $NewTotalSize, "NFolders:" , $NewNumFolders, "NFiles:" , $NewNumFiles | Out-String 

#Silently clears recycle bin
Clear-RecycleBin -Confirm:$false ) *>&1 > C:\Users\jacpurs\Desktop\$FileName.txt #Temp path for testing '

$Trigger = New-ScheduledTaskTrigger -daily -DaysInterval 5 -At 9am
Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName "Temp Folder Management" -Description "Removes files older than 24 hours that are not in use"


