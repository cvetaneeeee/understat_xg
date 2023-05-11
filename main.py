import json
import gspread
import requests
import datetime
import pandas as pd
from collections.abc import Iterator
from time import perf_counter
from bs4 import BeautifulSoup
from google.oauth2 import service_account


start = perf_counter()
base_url = 'https://understat.com/league/'
leagues = ['La_liga', 'EPL', 'Bundesliga', 'Serie_A', 'Ligue_1']
current_year = datetime.datetime.now().year
seasons = list(range(2014, current_year))


def build_url() -> str:
    # change season or league to be scraped by adjusting the indexes
    url = base_url + leagues[1] + '/' + str(seasons[-1])
    return url


def get_data(url: str) -> str:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    scripts = soup.find_all('script')
    coded_data = scripts[2].string
    return coded_data


def parse_json() -> dict:
    string = get_data(build_url())
    index_start = string.index("('")+2
    index_end = string.index("')")
    json_data = string[index_start:index_end].encode('utf8').decode('unicode_escape')
    data = json.loads(json_data)
    return data


def build_iter(func: dict) -> Iterator:
    for team_id in func.keys():
        team_name = func[team_id]['title']
        for row in func[team_id]['history']:
            h_a = row['h_a']
            xg = row['xG']
            xga = row['xGA']
            games_played = 1
            yield team_name, h_a, xg, xga, games_played


def build_frame() -> pd.DataFrame:
    columns = ['team', 'h_a', 'xG', 'xGA', 'games_played']
    alldata = list(build_iter(parse_json()))
    alldata_frame = pd.DataFrame(alldata, columns=columns)
    return alldata_frame


def push_to_gsheets(key_path: str, spreadsheet: str, sheet: str, df: pd.DataFrame) -> None:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_file(key_path, scopes=scope)
    client = gspread.authorize(credentials)
    sh = client.open_by_key(spreadsheet)
    sh.values_clear(f"{sheet}!A:Z")
    sh.worksheet(sheet).resize(rows=2)
    sh.worksheet(sheet).resize(cols=5)
    sh.worksheet(sheet).update([df.columns.values.tolist()] + df.values.tolist())


if __name__ == '__main__':

    path = "path to your credentials"
    spreadsheetId = "your spreadsheet ID"
    sheetName = "your sheet name"

    try:
        dataframe = build_frame()
        push_to_gsheets(path, spreadsheetId, sheetName, dataframe)

        end = perf_counter()
        print(f'Finished scraping data in {end-start} seconds!')

    except Exception as e:
        print(str(e))
