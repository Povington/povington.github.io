## Feel Free to take a look at what I've been working on below:


Here's a quick  [Code Review](https://youtu.be/B3gvz-9SsJYI) performed on an authentication page I've been working on. Check it out!

You can take a look at the full authentication page project [here.](https://github.com/Povington/povington.github.io/tree/master/Authentication%20Page)

### Other Projects

Take a look below to see a few other scripts and apps that I have created.

For example, here's a neat powershell script I created. 

```$Action = New-ScheduledTaskAction -Execute 'Powershell.exe' -Argument '
#Generate Unique name for log file
$RootName = "Log-"
$LogDate = Get-Date -Format FileDate
$FileName = $RootName + $LogDate
$(
#Declare path
$Path = "$env:temp"
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
Clear-RecycleBin -Confirm:$false ) *>&1 > C:\Users\username\Desktop\$FileName.txt #Temp path for testing '

$Trigger = New-ScheduledTaskTrigger -daily -DaysInterval 5 -At 9am
Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName "Temp Folder Management" -Description "Removes files older than 24 hours that are not in use"

```
You can access the above script [here](https://github.com/Povington/povington.github.io/blob/master/TempFolderManagement.ps1)

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/Povington/povington.github.io/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
