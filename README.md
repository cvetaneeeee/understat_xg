# understat.com
Repo scraping xG data from understat.com

## main.py

1. I recommend cloning this repo in a virual environment, then install the packages in requirements.txt with pip install -r requirements.txt
2. Set up a free service account in google cloud and store the credentials in a keys.json file, then place it in the repo
3. Copy the service account email, create a google spreadsheet and share it with the service account to give it access
4. Copy your sheet ID and sheet name and paste them in lines 75 and 76 in the code
5. Put the path to your credentials on line 74. If you've name your credentials keys.json and placed the file in this repo, the path should just read keys.json
6. Adjust the indexes in the build_url function to scrape xG data for another season or league


# rapidapi.com - api-football api

## rapidapi_fixtures.py

1. Sign up for api-football on rapidapi.com and get your key and put it in the code in the key variable
2. Adjust the query string to your preference - modify the league, the season and toggle between 'next' and 'last' key word to get 'next' or 'last' 'N' fixtures