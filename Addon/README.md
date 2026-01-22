\#Blender Diffusion Neural Style Transfer



1. Install the Add-on



* Download latest release of zip file
* In Blender, go to Edit > Preferences > Get Extensions
* Click install and select downloaded zip file
* Enable the add-on by checking the box



2\. Install Python Dependencies and Setup (Crucial)



* In Edit > Preferences > Add-ons: find "Diffusion Style Transfer" and expand the details
* If status is "Setup required", click the install button
* The installation process may take several minutes, wait until the progress is done (You can watch the installation progress by opening the System Console under Window > Toggle System Console)
* CRITICAL: you must close and restart Blender after installation





3\. Generation



* Open the Image Editor or UV Editor Window
* Expand the Sidepanel
* You should find the Tab "NST" where the tool is located
* Hover over the parameters to get an explanation
* INFO: The first time of generating a content or style image will take about 1min longer per image than later generations
* Warning: if picture size is bigger than 2048, generation times will take longer
* For more Progress Feedback during the generation, you can open the System Console
* CRITICAL: Do not cancel the generation process as this will lead to errors



4\. Uninstallation and Cleanup



* To uninstall the add-on go to Edit-> Preferences -> Get Extensions: expand "Diffusion NST", click on the little arrow and uninstall
* to completely clean any remaining saves do the following:
* Go into your specified output image folder and delete the latents\_forward folder completely: this were saves to speed up regeneration of images



