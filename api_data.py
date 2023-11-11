import pandas as pd

codigo_bcb = 4389

url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb}/dados?formato=json'

df = pd.read_json(url)
df['data'] = pd.to_datetime(df['data'], dayfirst=True)

# applying the groupby function on df
df = df.resample('D').bfill()

print(df)