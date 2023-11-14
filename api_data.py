#ACESSANDO OS DADOS POR API DO CDI, IPCA E IGPM
codigos_bcb = [4389, 433, 189]
indices_bcb = ['CDI', 'IPCA', 'IGPM']

df_cdi = pd.DataFrame()
df_ipca = pd.DataFrame()
df_igpm = pd.DataFrame()

def tratar_dados(cod):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados?formato=json'
    df = pd.read_json(url)
    #Convertendo Coluna de data em DateTime
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    return df

for cod, i in zip(codigos_bcb, indices_bcb):
    if i == 'CDI':
        df_cdi = tratar_dados(cod)            
    if i == 'IPCA':
        df_ipca = tratar_dados(cod)            
    if i == 'IGPM':
        df_igpm = tratar_dados(cod)            

#Convertendo a frequência da data em Mensal
#Para isso é preciso indexar a DATA
df_igpm.set_index('data', inplace=True)
df_ipca.set_index('data', inplace=True)

df_igpm.index = df_igpm.index.to_period('M')
df_ipca.index = df_ipca.index.to_period('M')

#Renomeando as colunas pelos nomes dos Índices
df_ipca.rename(columns={'valor':'IPCA'}, inplace=True)
df_igpm.rename(columns={'valor':'IGPM'}, inplace=True)
df_cdi.rename(columns={'valor':'CDI'}, inplace=True) 

#Concatenando as Colunas pela Data
df_ipca_igpm = pd.concat([df_ipca,df_igpm], axis=1)

#Eliminando as linhas com NaN
df_ipca_igpm = df_ipca_igpm.dropna(axis=0)

#Resetando o Index
df_ipca_igpm.reset_index(inplace=True)

#Filtrando os dados a partir de uma data
df_cdi = df_cdi[df_cdi['data'] >= '2002-08-01']
df_ipca_igpm = df_ipca_igpm[df_ipca_igpm['data'] >= '2023-01-01']

df_ipca_igpm['data'] = df_ipca_igpm['data'].dt.strftime('%Y-%m-%d')

######################======================#######################

#IIMPORTANDO OS DADOS DO IBOVESPA E DOLAR
tickers = ['^BVSP', 'BRL=X', 'CL=F']
indices = ['IBOV', 'Dolar', 'Crude']

def tratar_df(ticker, indice):
    ticker = yf.Ticker(ticker).history(period='12mo')
    df = pd.DataFrame()
    df['Data'] = ticker['Close'].index
    df[indice] = list(ticker['Close'])
    df['Data'] = df['Data'].dt.strftime('%Y-%m-%d')
    return df

df_ibov = pd.DataFrame()
df_dol = pd.DataFrame()
df_crude = pd.DataFrame()

for t, i in zip(tickers, indices):
    if t == '^BVSP':
        df_ibov = tratar_df(t, i)
        ibov_ult = round(df_ibov[i].iloc[-1],2)
        ibov_ult_2 = round(df_ibov[i].iloc[-2],2)
        delta_ibov = round(((ibov_ult / ibov_ult_2) - 1) * 100,2)
        atual_ibov = '{0:,}'.format(ibov_ult).replace(',','.')
    elif t == 'BRL=X': 
        df_dol = tratar_df(t,i)
        dol_ult = round(df_dol[i].iloc[-1],2)
        atual_dol = '{0:,}'.format(dol_ult).replace('.',',')
        dol_ult_2 = round(df_dol[i].iloc[-2],2)
        delta_dol = round(((dol_ult / dol_ult_2) - 1) * 100,2)
    elif t == 'CL=F':
        df_crude = tratar_df(t,i)   
        crude_ult = round(df_crude[i].iloc[-1],2)
        atual_crude = '{0:,}'.format(crude_ult).replace('.',',')
        crude_ult_2 = round(df_crude[i].iloc[-2],2)
        delta_crude = round(((crude_ult / crude_ult_2) - 1) * 100,2)