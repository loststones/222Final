from calendar import weekday
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter



def hist_show(ser):
    plt.hist(ser, bins=24)
    plt.xlabel("End Hour")
    plt.ylabel("total of songs")
    plt.show()

df0 = pd.read_json("HSStreamingHistory0.json")
df1 = pd.read_json("HSStreamingHistory1.json")
df2 = pd.read_json("HSStreamingHistory2.json")
df3 = pd.read_json("HSStreamingHistory3.json")


df = pd.concat([df0, df1, df2, df3])

# Split the end time into seperate columns for date and time
'''
df[["endDate", "endTime"]] = df0["endTime"].str.split(' ', expand=True)
df[["endHour", "endMin"]] = df["endTime"].str.split(':', expand=True)
df = df.drop(["endTime", "endMin"])'''

# split the end time to just the hour and as an int
df["endHour"] = df["endTime"].str.split(' ').str[1].str.split(':').str[0].astype(int)
df["date"] = df["endTime"].str.split(' ').str[0]
df = df.drop("endTime", axis=1)
days = pd.read_csv("DaysofWeek.csv")
df = df.merge(days, on=["date"], how="inner")
# create series of the endTimes
ser = df["endHour"]
meanTime = ser.mean()
stdTime = ser.std()
print(stdTime)


# show a histogram of the data we are looking at



# The end time is stored in coordinated universal time, we are looking for values between 8pm to 2am pst.
df["endHour"] = (df["endHour"] + 24 - 7) % 24
print(df)
# that converts to 3 to 9 in coordinated universal time.

def group_day(day):
    group_by_day = df.groupby("days of week")
    df = group_by_day.get_group(day)
    return df

print()
group_by_day = df.groupby("days of week")
fri_df = group_by_day.get_group("Friday")
sat_df = group_by_day.get_group("Saturday")
sun_df = group_by_day.get_group("Sunday")
mon_df = group_by_day.get_group("Monday")
tue_df = group_by_day.get_group("Tuesday")
wed_df = group_by_day.get_group("Wednesday")
thur_df = group_by_day.get_group("Thursday")

# hist_show(ser)
# hist_show(fri_df["endHour"])
# hist_show(sat_df["endHour"])
# hist_show(sun_df["endHour"])
# hist_show(mon_df["endHour"])

weekday_df = mon_df
weekday_df.append(tue_df)
weekday_df.append(wed_df)
weekday_df.append(thur_df)
weekday_df.append(fri_df)

print(weekday_df)

weekend_df = sat_df
weekend_df.append(sun_df)

# print(weekday_df)
# print()
# print(weekend_df)

end_arr = df["endHour"].to_numpy()
print(end_arr)

# data is
# 1-tailed
# H0 Mweekend <= Mweekday
# H1: Mweekend > Mweekday
t, pval = stats.ttest_ind(weekday_df["endHour"], weekend_df["endHour"])
pval /= 2 # divide by two because 1 rejection region
print("t:", t, "pval:", pval)
alpha = 0.05
if pval < alpha:
    print("reject H0")
else:
    print("do not reject H0")



from sklearn.preprocessing import MinMaxScaler

X_train = end_arr
y_train = df["days of week"]

scaler = MinMaxScaler()
X_train = np.reshape(X_train, (-1, 1))
scaler.fit(X_train)
print(scaler.data_min_)
print(scaler.data_max_)

X_train_normalized = scaler.transform(X_train)
print(X_train_normalized)

# # train
# from sklearn.neighbors import KNeighborsClassifier
# neigh = KNeighborsClassifier(n_neighbors=3)
# neigh.fit(X_train_normalized, y_train)

# # test
# X_test = pd.Series([3, 7, 1, 4, 5], index=df.columns.drop("days of week"))
# X_test = scaler.transform([X_test])
# y_test_prediction = neigh.predict(X_test)
# print(y_test_prediction)



