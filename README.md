# App_Flash_Detector
A python script to send an email when an app starts flashing

This was initially written to send me an email when a long-running query would finish from Toad Data Point so I didn't have to check my computer during times I was away. The app icon flashes when a query is finished so this behavior acts as the trigger for the email send. For now, the script can be triggered from the command line with 'python email_script.py' to begin monitoring and once the icon change is detected and the email is automatically sent, the script will stop running. 
