import Data_fetcher as df
import pandas as pd
import numpy as np


class player:
    def __init__(self):
        self.name = 'No player'
        self.team = 'No Team'
        self.total_points = 0
        self.upcoming_fdr = 0
        self.ppm = 0
        self.cost = 0


def get_Subgrp(dataFrame, subgrp_id, subgrp):
    dataFrame = dataFrame[dataFrame[subgrp_id] == subgrp]
    return dataFrame


def string_construct(string, playerInfo=player()):
    # Name
    string = string + "Name: " + playerInfo.name + "\n"
    string = string + "Team: " + playerInfo.team + "\n"
    string = string + "Total Points: " + str(playerInfo.total_points) + "\n"
    string = string + "Next FDR: " + str(playerInfo.upcoming_fdr) + "\n"
    string = string + "Cost: " + str(playerInfo.cost / 10) + "\n"
    string = string + "PPM: " + "{:.2f}".format(playerInfo.ppm) + "\n\n"
    return string


class GKP:
    STARTER_PERCENTAGE_DEF = 0.7

    def __init__(self):
        self.gkp = player()

    def select_gkp(self):
        # Get all data
        allData = df.dataGetter()
        allData.get_allData()

        gkp = get_Subgrp(allData.playersData, 'element_type', 1)
        total_minutes_possible = (allData.gw_no - 1) * 90
        starter_minutes = self.STARTER_PERCENTAGE_DEF * total_minutes_possible
        starter_gkp = gkp[gkp.minutes >= starter_minutes]
        starter_gkp = starter_gkp[starter_gkp.chance_of_playing_next_round != 0]
        starter_gkp = starter_gkp.sort_values(by='now_cost', ascending=True)
        min_gkp_price = starter_gkp['now_cost'].iloc[0]
        selected_cheap_gkp = starter_gkp[starter_gkp['now_cost'] == min_gkp_price]
        sLength = len(selected_cheap_gkp.index)
        selected_cheap_gkp = selected_cheap_gkp.assign(TOTAL_FDR=pd.Series(np.random.randn(sLength)).values)
        for i in range(len(selected_cheap_gkp.index)):
            team_id = selected_cheap_gkp.iloc[i][1]
            fdr_history = allData.team_hist[allData.team_hist.index == team_id]
            selected_cheap_gkp.loc[selected_cheap_gkp.index[i], 'TOTAL_FDR'] = fdr_history['FDR'].sum()
        # to
        selected_cheap_gkp = selected_cheap_gkp.sort_values(by='total_points', ascending=False)
        # set goalkeeper recommendations
        self.gkp.name = selected_cheap_gkp['second_name'].iloc[0]
        team_id = selected_cheap_gkp['team'].iloc[0]
        self.gkp.team = allData.team_data.loc[team_id, 'name']
        self.gkp.total_points = selected_cheap_gkp['total_points'].iloc[0]
        self.gkp.upcoming_fdr = selected_cheap_gkp['FDR'].iloc[0]
        self.gkp.cost = min_gkp_price
        self.gkp.ppm = self.gkp.total_points / (self.gkp.cost / 10)

        Result = "Goalkeeper: \n"
        Result = string_construct(Result, self.gkp)
        return Result


class DEF:
    STARTER_PERCENTAGE_DEF = 0.7

    def __init__(self):
        # Get all data
        self.allData = df.dataGetter()
        self.allData.get_allData()

        self.lowPlayer = player()
        self.midPlayer = player()
        self.highPlayer = player()

    def sortPPM(self, dataF):
        footballer = player()
        dataF = dataF.assign(PPM=dataF['total_points'] / dataF['now_cost'] * 10)
        dataF = dataF.sort_values(by='PPM', ascending=False)
        footballer.name = dataF['second_name'].iloc[0]
        team_id = dataF['team'].iloc[0]
        footballer.team = self.allData.team_data.loc[team_id, 'name']
        footballer.total_points = dataF['total_points'].iloc[0]
        footballer.upcoming_fdr = dataF['FDR'].iloc[0]
        footballer.ppm = dataF['PPM'].iloc[0]
        footballer.cost = dataF['now_cost'].iloc[0]
        return footballer

    def select_DEF(self):
        defenders = get_Subgrp(self.allData.playersData, 'element_type', 2)
        low_cost = defenders[defenders['now_cost'] < 51]
        self.lowPlayer = self.sortPPM(low_cost)

        mid_cost = defenders[defenders['now_cost'] < 61]
        mid_cost = mid_cost[mid_cost['now_cost'] > 50]
        self.midPlayer = self.sortPPM(mid_cost)

        high_cost = defenders[defenders['now_cost'] > 60]
        self.highPlayer = self.sortPPM(high_cost)

        # create string
        Result = "LOW BRACKET:\n"
        Result = string_construct(Result, self.lowPlayer)

        Result = Result + "MID BRACKET: \n"
        Result = string_construct(Result, self.midPlayer)

        Result = Result + "HIGH BRACKET: \n"
        Result = string_construct(Result, self.highPlayer)
        return Result

    def select_DEF_top3(self, max_price=str):
        defenders = get_Subgrp(self.allData.playersData, 'element_type', 2)
        try:
            max_price_int = float(max_price) * 10

            defender_filtered = defenders[defenders['now_cost'] < max_price_int]

            self.highPlayer = self.sortPPM(defender_filtered)
            defender_filtered = defender_filtered[defender_filtered['second_name'] != self.highPlayer.name]

            self.midPlayer = self.sortPPM(defender_filtered)
            defender_filtered = defender_filtered[defender_filtered['second_name'] != self.midPlayer.name]

            self.lowPlayer = self.sortPPM(defender_filtered)

            Result = "First:\n"
            Result = string_construct(Result, self.highPlayer)

            Result = Result + "Second: \n"
            Result = string_construct(Result, self.midPlayer)

            Result = Result + "Third: \n"
            Result = string_construct(Result, self.lowPlayer)
            return Result
        except ValueError:
            return "Enter a number please"
        except IndexError:
            return "Price too low"


class MID:
    STARTER_PERCENTAGE_DEF = 0.7

    def __init__(self):
        # Get all data
        self.allData = df.dataGetter()
        self.allData.get_allData()

        self.lowPlayer = player()
        self.midPlayer = player()
        self.highPlayer = player()

    def sortPPM(self, dataF):
        footballer = player()
        try:
            dataF = dataF.assign(PPM=dataF['total_points'] / dataF['now_cost'] * 10)
            dataF = dataF.sort_values(by='PPM', ascending=False)
            footballer.name = dataF['second_name'].iloc[0]
            team_id = dataF['team'].iloc[0]
            footballer.team = self.allData.team_data.loc[team_id, 'name']
            footballer.total_points = dataF['total_points'].iloc[0]
            footballer.upcoming_fdr = dataF['FDR'].iloc[0]
            footballer.ppm = dataF['PPM'].iloc[0]
            footballer.cost = dataF['now_cost'].iloc[0]
        except IndexError:
            pass
        return footballer

    def select_MID(self):
        mid_fielder = get_Subgrp(self.allData.playersData, 'element_type', 3)
        mid_fielder = mid_fielder.sort_values(by='now_cost', ascending=True)

        # Remove high FDR options
        mid_fielder = mid_fielder[mid_fielder['FDR'] < 4]

        low_cost = mid_fielder[mid_fielder['now_cost'] < 72]
        # low_cost = low_cost.assign(PPM=low_cost['total_points'] / low_cost['now_cost'] * 10)
        self.lowPlayer = self.sortPPM(low_cost)

        mid_cost = mid_fielder[mid_fielder['now_cost'] < 98]
        mid_cost = mid_cost[mid_cost['now_cost'] > 71]
        # mid_cost = mid_cost.assign(PPM=mid_cost['total_points'] / mid_cost['now_cost'] * 10)
        self.midPlayer = self.sortPPM(mid_cost)

        high_cost = mid_fielder[mid_fielder['now_cost'] > 97]
        # high_cost = high_cost.assign(PPM=high_cost['total_points'] / high_cost['now_cost'] * 10)
        self.highPlayer = self.sortPPM(high_cost)

        # create string
        Result = "LOW BRACKET:\n"
        Result = string_construct(Result, self.lowPlayer)

        Result = Result + "MID BRACKET: \n"
        Result = string_construct(Result, self.midPlayer)

        Result = Result + "HIGH BRACKET: \n"
        Result = string_construct(Result, self.highPlayer)
        return Result

    def select_Mid_top3(self, max_price=str):

        mid = get_Subgrp(self.allData.playersData, 'element_type', 3)
        try:
            max_price_int = float(max_price)*10

            mid_filtered = mid[mid['now_cost'] < max_price_int]

            self.highPlayer = self.sortPPM(mid_filtered)
            defender_filtered = mid_filtered[mid_filtered['second_name'] != self.highPlayer.name]

            self.midPlayer = self.sortPPM(defender_filtered)
            defender_filtered = defender_filtered[defender_filtered['second_name'] != self.midPlayer.name]

            self.lowPlayer = self.sortPPM(defender_filtered)

            Result = "First:\n"
            Result = string_construct(Result, self.highPlayer)

            Result = Result + "Second: \n"
            Result = string_construct(Result, self.midPlayer)

            Result = Result + "Third: \n"
            Result = string_construct(Result, self.lowPlayer)
            return Result
        except ValueError:
            return "Enter a number please"
        except IndexError:
            return "Price too low"


class FWD:
    STARTER_PERCENTAGE_DEF = 0.7

    def __init__(self):
        # Get all data
        self.allData = df.dataGetter()
        self.allData.get_allData()

        self.lowPlayer = player()
        self.midPlayer = player()
        self.highPlayer = player()

    def sortPPM(self, dataF):
        footballer = player()
        dataF = dataF.assign(PPM=dataF['total_points'] / dataF['now_cost'] * 10)
        dataF = dataF.sort_values(by='PPM', ascending=False)
        footballer.name = dataF['second_name'].iloc[0]
        team_id = dataF['team'].iloc[0]
        footballer.team = self.allData.team_data.loc[team_id, 'name']
        footballer.total_points = dataF['total_points'].iloc[0]
        footballer.upcoming_fdr = dataF['FDR'].iloc[0]
        footballer.ppm = dataF['PPM'].iloc[0]
        footballer.cost = dataF['now_cost'].iloc[0]
        return footballer

    def select_FWD(self):
        fwd = get_Subgrp(self.allData.playersData, 'element_type', 4)
        fwd = fwd.sort_values(by='now_cost', ascending=True)

        # Remove high FDR options
        fwd = fwd[fwd['FDR'] < 4]

        low_cost = fwd[fwd['now_cost'] < 72]

        mid_cost = fwd[fwd['now_cost'] < 99]
        mid_cost = fwd[fwd['now_cost'] > 71]

        high_cost = fwd[fwd['now_cost'] > 98]

        list_of_elements = ['goals_scored', 'second_name', 'total_points', 'assists', 'now_cost', 'FDR',
                            'ict_index', 'ict_index_rank']

        self.lowPlayer = self.sortPPM(low_cost)
        self.midPlayer = self.sortPPM(mid_cost)
        self.highPlayer = self.sortPPM(high_cost)
        Result = "LOW BRACKET:\n"
        Result = string_construct(Result, self.lowPlayer)

        Result = Result + "MID BRACKET: \n"
        Result = string_construct(Result, self.midPlayer)

        Result = Result + "HIGH BRACKET: \n"
        Result = string_construct(Result, self.highPlayer)

        return Result


class CUSTOM:
    def __init__(self, name=str):
        # Get all data
        self.allData = df.dataGetter().getPlayer_history(name)
        self.customPlayer = player()

    def getPlayer(self):
        print(self.allData)
        print('ok')
