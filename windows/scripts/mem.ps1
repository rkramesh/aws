$strComputer = $Host
Clear
$RAM = WmiObject Win32_ComputerSystem
$MB = 1024

"Installed Memory: " + [int]($RAM.TotalPhysicalMemory /$MB) + " MB"

