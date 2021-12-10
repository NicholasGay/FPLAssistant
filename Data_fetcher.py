import pandas as pd
import numpy as np
import requests

proxies = {
    "http": None,
    "https": None,
}


def get_json(url):
    r = requests.get(url)
    json = r.json()
    return json


def fixture_list_combine(fixture_df):
    fixtures_home = fixture_df[['team_h', 'team_h_difficulty']]
    fixtures_home = fixtures_home.rename({fixtures_home.columns.array[0]: "Team",
                                          fixtures_home.columns.array[1]: "FDR"}, axis='columns')
    fixtures_away = fixture_df[['team_a', 'team_a_difficulty']]
    fixtures_away = fixtures_away.rename({fixtures_away.columns.array[0]: "Team",
                                          fixtures_away.columns.array[1]: "FDR"}, axis='columns')
    fdr_df = fixtures_home.append(fixtures_away, ignore_index=False)
    fdr_df = fdr_df.sort_values(by=fdr_df.columns.array[0], ascending=True)
    fdr_df = fdr_df.set_index('Team')
    return fdr_df


class dataGetter:
    BASE_URL = 'https://fantasy.premierleague.com/api/'

    def __init__(self):
        self.playersData = pd.DataFrame
        self.playerPos = pd.DataFrame
        self.gw_no = 0
        self.team_hist = pd.DataFrame
        self.team_data = pd.DataFrame

    def get_comprehensive_data(self):
        url = self.BASE_URL + 'bootstrap-static/'
        json = get_json(url)
        elements_df = pd.DataFrame(json['elements'])
        element_types_df = pd.DataFrame(json['element_types'])
        slim_element_types_df = element_types_df[['id', 'plural_name_short']]

        teams_df = pd.DataFrame(json['teams'])
        slim_teams_df = teams_df[['name', 'id']]
        return elements_df, slim_element_types_df, slim_teams_df

    # fixture data get
    def get_fixture(self):
        url = self.BASE_URL + 'fixtures/'
        json = get_json(url)
        fixtures_df = pd.DataFrame(json)
        fixtures_slim = fixtures_df[['team_a', 'team_h', 'team_h_difficulty', 'team_a_difficulty', 'finished', 'event']]
        fixtures_uncompleted_df = fixtures_slim[fixtures_slim.finished != True]
        fixtures_completed_df = fixtures_slim[fixtures_slim.finished == True]
        fixtures_uncompleted_df = fixtures_uncompleted_df[fixtures_uncompleted_df['event'].notnull()]
        current_fixture_event = pd.Series(fixtures_uncompleted_df['event']).values.min(initial=None)
        fixtures_nextGW = fixtures_uncompleted_df[fixtures_uncompleted_df.event == current_fixture_event + 1]
        fixtures_uncompleted = fixtures_uncompleted_df[fixtures_uncompleted_df.event == current_fixture_event]
        return fixtures_completed_df, fixtures_nextGW, current_fixture_event, fixtures_uncompleted

    def get_summary(self, id_no):
        url = self.BASE_URL + 'element-summary/' + str(id_no) + '/'
        print(url)
        json = get_json(url)
        fixture_df = pd.DataFrame(json['fixtures'])
        history_df = pd.DataFrame(json['history'])
        history_past_df = pd.DataFrame(json['history_past'])
        # to be edited
        return 0

    def getPlayer_history(self, id_no=str):
        url = self.BASE_URL + 'element-summary/' + id_no + '/'
        json = get_json(url)

        fixture_player = pd.DataFrame(json['fixtures'])
        if fixture_player.iloc[0]['is_home']:
            team_id = fixture_player.iloc[0]['team_h']
        else:
            team_id = fixture_player.iloc[0]['team_a']
        print(team_id)
        fixtures_before, fixtures_next, gw_no, fixtures_uncompleted = self.get_fixture()
        history_df = pd.DataFrame(json['history'])
        fixture_team_away = fixtures_before[fixtures_before['team_a'] == int(team_id)]
        fixture_team_away = fixture_team_away[['event', 'team_a_difficulty']]
        fixture_team_away = fixture_team_away.rename(columns={'team_a_difficulty': 'difficulty'})

        fixture_team_home = fixtures_before[fixtures_before['team_h'] == int(team_id)]
        fixture_team_home = fixture_team_home[['event', 'team_h_difficulty']]
        fixture_team_home = fixture_team_home.rename(columns={'team_h_difficulty': 'difficulty'})

        fixture_team_combine = fixture_team_away.append(fixture_team_home)
        fixture_team_combine = fixture_team_combine.sort_values(by=['event'])
        fixture_team_combine['points'] = history_df['total_points'].values
        history_past_df = pd.DataFrame(json['history_past'])

        return history_df

    def get_allData(self):
        fixtures_before, fixtures_next, gw_no, fixtures_uncompleted = self.get_fixture()
        players_data, player_pos, teams_data = self.get_comprehensive_data()
        sLength = players_data.shape[0]
        remaining_index = []
        # for incomplete fixtures
        fdr_UC_df = fixture_list_combine(fixtures_uncompleted)
        fdr_NEXT_df = fixture_list_combine(fixtures_next)
        players_data = players_data.assign(FDR=pd.Series(np.random.randn(sLength)).values)
        for i in range(players_data.shape[0]):
            team_id = players_data.team[i]
            try:
                team_fdr = fdr_UC_df.loc[team_id]['FDR']
            except KeyError:
                team_fdr = fdr_NEXT_df.loc[team_id]['FDR']

            players_data.loc[i, 'FDR'] = team_fdr
        player_pos = player_pos.set_index('id')

        # for completed fixtures
        team_hist = fixture_list_combine(fixtures_before)
        teams_data = teams_data.set_index('id')
        # assigning values
        self.playersData = players_data
        self.playerPos = player_pos
        self.gw_no = gw_no
        self.team_hist = team_hist
        self.team_data = teams_data


class Data_process:
    pass
