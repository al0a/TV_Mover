TV Mover 0.1 (23/02/2013)
-------------------------

I. WHAT IS IT?
	A simple Python script that does the following:
		* Scan a directory of downloaded files, looking for video content.
		* For each video file it checks vs. a pattern to see if this is a TV show (has season and episode).
		* Moves every matching file to a directory in the following structure:
		   Some root folder ► TV Shows ► Show Name ► Season ## ► file.ext
		* If changes are detected, i can also trigger an "update" command the an XBMC machine.

II. COMPATIBILITY
	* I've only tested this script on Windows 7 64 bit.
	* It runs using the uTorrent software "run program" feature, or by comment line.

III. HOW TO SETUP
	* Python
		- Install Python 2.7 from http://www.python.org/download/releases/2.7.3/
		- Install Requests package from http://docs.python-requests.org/en/latest/user/install/#install

	* First make sure you change the variables in the "Variables" (top) section of the script:
		- show_reg - The pattern to match. Feel free to add more file extensions if needed.
		- dl_path - The folder to scan files for - aka your downloads folder.
		- mv_path - The root folder to move TV Shows too - aka your library folder.
		- atv_list - The IP:Port and credentials for remote controlling XBMC. For none just use []
	
	* Running the script:	
		* (Option 1) Run from uTorrnet:	
			- Open uTorrent and go to Options->Preferences->Advanced->Run program.
			- Change the text box below the caption "Run this program when a torrent changes state" to something like
			  "C:\tv_mover.pyw" "--utor" "%S"
			- Notice that files cannot be moved while seeding (locked). TV_Mover waits for a "Finished" status.
			
		* (Option 2) Run using command line, and some more options:
			- It is possible to run the script without uTorrent, just ignore the --utor argument.
			- Description of the other arguments:
				- DRY means that this is a dry run, no changes will be made (just show predicted changes).
				- UPDATE means that the script will forcibly update XBMC libraries, regardless to file changes.
			- Running "python TV_Mover.py --help" is also supported in order to see all available options.
		
	* Setting up XBMC:
		* Enable remote control:
			- Just enable the HTTP Server - http://wiki.xbmc.org/index.php?title=Webserver
			- Here's a screenshot: http://wiki.xbmc.org/index.php?title=Settings/Services#Webserver
		* Note: make sure you understand XBMC's library structure:
			- http://wiki.xbmc.org/index.php?title=Video_library/Naming_files/TV_shows
			- Also consider using: http://forum.xbmc.org/showthread.php?tid=152000
	
IV. NEXT VERSIONS (?)
	* Add support for movie handling.
	* Consider checking shows/movies names against an online DB.
	* Consider using Python's library for XBMC controlling.
	