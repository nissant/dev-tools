# Windows Shell Scripting
## General CMD Line 
* Show file contents
	```
	> type filename.txt
	```
## Networking
* To list all the active ports. The -a switch displays all ports in use, not just the ports associated with the current user. The -n option stops a hostname lookup (which takes a long time). The -o option lists the process ID that is responsible for the port activity. The findstr command matches the header row that contains the PID string, and the port you are looking for, in a port format with the preceding colon,
	```
	> netstat -ano|findstr "PID :3000"
	```
* To kill this process (the /f is force):
	```
	> taskkill /pid 18264 /f
	```


 