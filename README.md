\#Blender Diffusion Neural Style Transfer



1. Install the Add-on



* Download latest release of zip file
* In Blender, go to Edit > Preferences > Get Extensions
* Click install and select downloaded zip file
* Enable the add-on by checking the box



2\. Install Python Dependencies (Crucial)



* In Edit > Preferences > Add-ons: find "Diffusion Style Transfer" and expand the details
* If status is "Dependencies missing", click the install button
* The installation process may take several minutes, wait until the progress is done
* CRITICAL: you must close and restart Blender after installation



3\. Troubleshooting: 



* If Install Dependencies runs successful, but even after a restart of Blender the status never changes to "Dependencies Installed"
* likely because Python library (torch) requires specific C++ runtime library that is often missing on Windows Systems
* -> Solution:
* Download and install latest Visual Studio Redistributable for Windows X64 on website: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-supported-redistributable-version
* Run the installer and choose the Repair option
* Restart your computer (Highly Recommended)
* Re-open Blender: Dependencies should now be recognized instantly
