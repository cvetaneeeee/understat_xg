# understat_xg
Repo scraping xG data from understat.com

1. Set up a free service account in google cloud and store the credentials in a keys.json file, then place it in the repo
2. Copy the service account email, create a google spreadsheet and share it with the service account to give it access
3. Copy your sheet ID and sheet name and paste them in lines 74 and 75 in the code
4. Put the path to your credentials on line 73. If you've name your credentials keys.json and placed the file in this repo, the path should just read keys.json
5. Adjust the indexes in the build_url function to scrape xG data for anothe season or league 
