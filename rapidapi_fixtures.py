import requests
import datetime
import pandas as pd
from collections.abc import Iterator

league_ids = {"EPL":"39", "LaLiga":"140", "SerieA":"135", "Ligue1":"61", "Bundesliga":"78"}
key = "9827825cbfmshd42a2badaac6f09p18e860jsn3f7778eddb0d"

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
querystring = {f"league":{league_ids['Bundesliga']}, 
	       		"season":"2023", 
				"next":"50",
	      		 }

headers = {
	"X-RapidAPI-Key": f"{key}",
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
output = response.json()['response']


def build_iter(obj: str) -> Iterator:
	for fixture in obj:
		date = datetime.datetime.fromtimestamp(fixture['fixture']['timestamp']).strftime('%m/%d/%Y')
		weekday = datetime.datetime.fromtimestamp(fixture['fixture']['timestamp']).strftime('%a')
		home_team = fixture['teams']['home']['name']
		home_goals = fixture['goals']['home']
		away_goals = fixture['goals']['away']
		away_team = fixture['teams']['away']['name']
		yield weekday, date, home_team, home_goals, away_goals, away_team

def build_dataframe() -> pd.DataFrame:
	columns = ['weekday', 'date', 'home_team', 'home_goals', 'away_goals', 'away_team']
	alldata = list(build_iter(output))
	alldata_frame = pd.DataFrame(alldata, columns=columns)
	replace = {"Wolves": "Wolverhampton Wanderers", "West Ham": "West Ham United",
	            "Tottenham": "Tottenham Hotspur", "Sheffield Utd": "Sheffield United",
		        "Newcastle": "Newcastle United", "Luton": "Luton Town", "Brighton": "Brighton & Hove Albion",
		        "Bournemouth": "AFC Bournemouth", "Inter": "Inter Milan", "AS Roma": "Roma",
		        "Athletic Club": "Athletic Bilbao", "Granada CF": "Granada", "Borussia Monchengladbach": "Borussia M'gladbach",
		        "VfL Wolfsburg": "Wolfsburg", "VfB Stuttgart": "Stuttgart", "FSV Mainz 05": "Mainz", "1899 Hoffenheim": "Hoffenheim",
		        "FC Heidenheim": "Heidenheim", "SC Freiburg": "Freiburg", "FC Koln": "FC Cologne", "SV Darmstadt 98": "Darmstadt", 
		        "VfL BOCHUM": "Bochum", "FC Augsburg": "Augsburg"
		}
	alldata_frame = alldata_frame.replace({"home_team":replace, "away_team":replace})
	return alldata_frame


if __name__ == '__main__':

	try:
		data = build_dataframe()
		data.to_csv('data.csv', index=False)
		print(data)

	except Exception as e:
		print(str(e))
    

    