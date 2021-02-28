import pandas as pd
import datetime as dt
DATA_LOCATION = 'https://energyweb-datasets.s3.nl-ams.scw.cloud/data.csv'
COLUMN_TO_PREDICT = 'kWh'

df = pd.read_csv(DATA_LOCATION)
print(df)

means_by_hour = df.groupby(df.index % 24).mean()
print(means_by_hour)
current_prediction = means_by_hour.iloc[dt.datetime.now().hour][COLUMN_TO_PREDICT]

print(current_prediction)