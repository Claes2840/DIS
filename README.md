# DIS
git repository:  https://github.com/Claes2840/DIS/tree/main

## Requirements:
Run the code below to install the necessary modules.

    pip install -r requirements.txt


## Notes
If run on Windows, there may be issues with permission. 
If such an error should occur then visit the following website under section 1 to resolve the issue:
https://www.makeuseof.com/windows-11-fix-access-denied-error/
Please note that you should add a new user called "everyone" after the last step

## Database init
First, create a database with the name MovieRoulette and update line 7 in app.py to match your local database
Then run 'create_basic_tables.sql' and remember to update the path to /tmp to your local path
 to create the tables and after that run 'create_relationship_tables.sql' and again remember to update the path to /tmp to your local path

Now all that is left is to run the command app.py in the terminal and enjoy!
