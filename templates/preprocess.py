import pandas as pd
import datetime
import numpy as np
from collections import deque

file_path = "../data/load_solar.xlsx"
df = pd.read_excel(file_path)
df = df.set_index('Datetime')

df = df.resample('1T').interpolate(method='polynomial', order=3, limit=14)

# Create a new DataFrame with the extended range
index_extension = pd.date_range(df.index[-1], periods=15, freq='T')[1:]
df_extension = pd.DataFrame(index=index_extension, columns=df.columns)

df_extension['Verbrauch_netto'] = df['Verbrauch_netto'][-1] + np.random.randn(14) * 0.01
df_extension['TotalPV'] = df['TotalPV'][-1] + np.random.rand(14) * 0.01

# Concatenate the original DataFrame with the extended DataFrame
df_interpolated = pd.concat([df, df_extension])

# Interpolate the extended range
df_interpolated = df_interpolated.interpolate(method='polynomial', order=3)

df_interpolated = pd.concat([df_interpolated, df_interpolated, df_interpolated, df_interpolated, df_interpolated, df_interpolated, df_interpolated, df_interpolated])

# file_path = "../data/fahrplan_postauto.xlsx"
file_path = "../data/Anzeige_des_Ladestands_MoDo_ELMO_V3_Eurobus_E-Maxi_2024.xlsx"
file_path = "../data/Anzeige_des_Ladestands-ELMO_PU_Steffen_2024_MF_HVZ-und_Tagesdienste_gemischt.xlsx"
schedule = pd.read_excel(file_path)

schedule.head()

buslines = schedule['Umlauf'].unique()
nbuses = len(buslines)

# Create an empty dataframe with a 1-minute resolution time index
schedule_id = schedule[schedule['Umlauf'] == buslines[0]].copy()

schedule_id['Zeit von'] = pd.to_datetime(schedule_id['Zeit von'].astype(str), format='%H.%M', errors='coerce')
schedule_id['Zeit bis'] = pd.to_datetime(schedule_id['Zeit bis'].astype(str), format='%H.%M', errors='coerce')

schedule_id['Zeit von'] = pd.to_datetime(schedule_id['Zeit von']) + pd.DateOffset(years=123)
schedule_id['Zeit bis'] = pd.to_datetime(schedule_id['Zeit bis']) + pd.DateOffset(years=123)

starttime = schedule_id['Zeit von']

start_date = pd.to_datetime(schedule_id['Zeit von'].min()).date()
end_date = pd.to_datetime(schedule_id['Zeit bis'].max()).date()
start_time = pd.to_datetime(start_date)
end_time = pd.to_datetime(end_date) + pd.DateOffset(days=7,hours=23, minutes=59)
index = pd.date_range(start=start_time, end=end_time, freq='1min')
data_1day = pd.DataFrame(index=index)


for day in range (8):
    if 0 <= day <= 3:
        True    
    
    if day == 4:
        file_path = "../data/Anzeige_des_Ladestands_Freitag_ELMO_V3_Eurobus_E-Maxi_2024.xlsx"
        file_path = "../data/Anzeige_des_Ladestands-ELMO_PU_Steffen_2024_MF_HVZ-und_Tagesdienste_gemischt.xlsx"
        
        schedule = pd.read_excel(file_path)
        schedule.head()
        buslines = schedule['Umlauf'].unique()
        nbuses = len(buslines)

    if day == 5:
        file_path = "../data/Anzeige_des_Ladestands_Samstag_Eurobus_E-Maxi_2024.xlsx"
        file_path = "../data/Anzeige_des_Ladestands-ELMO_PU_Steffen_2024_MF_HVZ-und_Tagesdienste_gemischt.xlsx"
        schedule = pd.read_excel(file_path)
        schedule.head()
        buslines = schedule['Umlauf'].unique()
        nbuses = len(buslines)

    if day == 6:
        file_path = "../data/Anzeige_des_Ladestands_Sonntag_V1_Eurobus_E-Maxi_2024.xlsx"
        file_path = "../data/Anzeige_des_Ladestands-ELMO_PU_Steffen_2024_MF_HVZ-und_Tagesdienste_gemischt.xlsx"
        schedule = pd.read_excel(file_path)
        schedule.head()
        buslines = schedule['Umlauf'].unique()
        nbuses = len(buslines)

    if day == 7:
        file_path = "../data/Anzeige_des_Ladestands_MoDo_ELMO_V3_Eurobus_E-Maxi_2024.xlsx"
        file_path = "../data/Anzeige_des_Ladestands-ELMO_PU_Steffen_2024_MF_HVZ-und_Tagesdienste_gemischt.xlsx"
        schedule = pd.read_excel(file_path)
        schedule.head()
        buslines = schedule['Umlauf'].unique()
        nbuses = len(buslines)

    for i in range (nbuses):
        schedule_id = schedule[schedule['Umlauf'] == buslines[i]].copy()

        #schedule_id['Zeit von'] = pd.to_datetime(schedule_id['Zeit von'].astype(str), format='%H.%M', errors='coerce')
        #schedule_id['Zeit bis'] = pd.to_datetime(schedule_id['Zeit bis'].astype(str), format='%H.%M', errors='coerce')

        time = schedule_id['Zeit von']

        hours1 = (np.floor(time))
        minutes1 = (np.round((time%1)*100))
        time1delta = hours1.copy()

        for j, row in schedule_id.iterrows():
            if day == 7 and hours1[j] > 23:
                time1delta[j] = datetime.timedelta(days=-1, hours=hours1[j], minutes=minutes1[j])
            else:
                time1delta[j] = datetime.timedelta(days=day, hours=hours1[j], minutes=minutes1[j])

        time = schedule_id['Zeit bis']
        
        hours2 = (np.floor(time))
        minutes2 = (np.round((time%1)*100))
        time2delta = hours2.copy()

        for j, row in schedule_id.iterrows():
            if day == 7 and hours2[j] > 23:
                time2delta[j] = datetime.timedelta(days=-1, hours=hours2[j], minutes=minutes2[j])
            else:
                time2delta[j] = datetime.timedelta(days=day, hours=hours2[j], minutes=minutes2[j])

        schedule_id['Zeit von'] = start_time + time1delta
        schedule_id['Zeit bis'] = start_time + time2delta

        if day == 0:
            data_1day['availability_id%d' %i] = 1
            data_1day['E_trip_rel_id%d' %i] = 0
            data_1day['E_trip_abs_id%d' %i] = 0

        # Set values to 1 for the time range where 'Ladetyp' is equal to 'BH'        
        bh_times = schedule_id[schedule_id['Ladetyp'] != 'BH'][['Zeit von', 'Zeit bis']]
        for _, row in bh_times.iterrows():
            start = row['Zeit von']
            end = row['Zeit bis']
            if end < start:
                data_1day.loc[start:end_time, 'availability_id%d' %i] = 0
                data_1day.loc[start_time:end, 'availability_id%d' %i] = 0
            else:
                data_1day.loc[start:end, 'availability_id%d' %i] = 0

        total_sum = 0
        end_previous = start_time

        for index, row in schedule_id.iterrows():
            end = row['Zeit bis']
            data_1day.loc[end, 'E_trip_rel_id%d' %i] = row['Entladung auf das Segment (kWh)']

            if row['Ladung auf dem Abschnitt (kWh)'] > 0:
                total_sum = 0
            else:
                if end < end_previous:
                    data_1day.loc[end_previous:end_time, 'E_trip_abs_id%d' %i] = total_sum
                    data_1day.loc[start_time:end, 'E_trip_abs_id%d' %i] = total_sum
                else:
                    if end_previous > start_time:
                        data_1day.loc[end_previous:end, 'E_trip_abs_id%d' %i] = total_sum

                total_sum += row['Entladung auf das Segment (kWh)']

            end_previous = end

            # if row['Ladetyp'] != 'BH':
            #     start = row['Zeit von']
            #     end = row['Zeit bis']
                
            #     # try:
            #     #     print(schedule_id['Zeit von'][index+1])
            #     #     start_next_trip = schedule_id['Zeit von'][index+1]
            #     # except:
            #     #     start_next_trip = start

            #     # if end < start_next_trip:
            #     #     end = start_next_trip

            #     if end < start:
            #         data_1day.loc[start:end_time, 'availability_id%d' %i] = 0
            #         data_1day.loc[start_time:end, 'availability_id%d' %i] = 0
            #     else:
            #         data_1day.loc[start:end, 'availability_id%d' %i] = 0


# Check if the index is not NaT
index_not_na = pd.notna(data_1day.index)

# Filter the DataFrame using the index_not_na mask
data_1day = data_1day[index_not_na]

data_1day['Verbrauch_netto'] = df_interpolated['Verbrauch_netto'].to_numpy()
data_1day['TotalPV'] = df_interpolated['TotalPV'].to_numpy()

#data_1day = data_1day.rename_axis('Datetime')

data_1day.reset_index(inplace=True)
data_1day.rename(columns={'index': 'Datetime'}, inplace=True)

data_1day = data_1day[:][240:-1200]

# data_1day.to_excel('../data/Anzeige_des_Ladestands_Mo-So_Eurobus_E-Maxi_2024_2.xlsx', index=False)
data_1day.to_excel('../data/Anzeige_des_Ladestands-ELMO_PU_Steffen_2024_MF_HVZ-und_Tagesdienste_gemischt_Mo-So.xlsx', index=False)

# shift_data = data_1day.pop(240)
# data_1day = pd.concat([data_1day[:][240:], data_1day[:][:239]], ignore_index=True, sort=False)

# data_1day[:][239:-1200]

# print(data_1day)
# print(data_1day[:][240:-1199])

stop=1