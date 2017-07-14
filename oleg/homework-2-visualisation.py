import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

%matplotlib inline

import datetime

init_notebook_mode(connected=True)


f = pd.read_csv('c:/temp/mlcourse_open-master/data/howpop_train.csv')
df.drop(filter(lambda c: c.endswith('_lognorm'), df.columns), axis=1, inplace=True)
df.published = pd.to_datetime(df.published)
df['year'] = [d.year for d in df.published]
df['month'] = [d.month for d in df.published]
df['day'] = [d.day for d in df.published]
df['hour'] = [d.hour for d in df.published]
df['dayofweek'] = [d.isoweekday() for d in df.published]

df_ym = df[['url', 'year', 'month']].groupby(['year', 'month']).count()
df_ym.reset_index(inplace=True)
#df_ym.plot(x = ['year', 'month'], y='url', figsize=(10,4))
print(df_ym[df_ym.url == df_ym.url.max()])
df_ym['yearmonth'] = [datetime.datetime(d[0],d[1],1) for d in df_ym.values]
iplot(go.Figure(data=[go.Scatter(x=df_ym.yearmonth, y=df_ym.url)]))

df_2015_03 = df[(df.year == 2015) & (df.month == 3)]
df_2015_03 = df_2015_03[['url', 'domain', 'day']]
df_2015_03_d = df_2015_03.groupby(['day', 'domain']).count()
df_2015_03_d.reset_index(inplace=True)
df_2015_03_habr = df_2015_03_d[df_2015_03_d.domain=='habrahabr.ru'][['day', 'url']].rename(columns={'url': 'habr'})
df_2015_03_geek = df_2015_03_d[df_2015_03_d.domain=='geektimes.ru'][['day', 'url']].rename(columns={'url': 'geek'})
df_2015_03_habr_geek = df_2015_03_habr.set_index('day').join(df_2015_03_geek.set_index('day'))
df_2015_03_habr_geek['total'] = df_2015_03_habr_geek.habr + df_2015_03_habr_geek.geek
#df_2015_03_habr_geek.plot()
iplot(go.Figure(data=[go.Scatter(x=df_2015_03_habr_geek.index, y=df_2015_03_habr_geek.habr),
                      go.Scatter(x=df_2015_03_habr_geek.index, y=df_2015_03_habr_geek.geek),
                      go.Scatter(x=df_2015_03_habr_geek.index, y=df_2015_03_habr_geek.total)]))




df_grp_hour = df[['hour', 'url', 'views', 'comments']].groupby('hour')
df_total = df_grp_hour.sum()
df_total.columns = ['count_views', 'count_comments']

df_total['mean_comments']=df_grp_hour['comments'].mean().astype(int)
df_total['mean_views']=df_grp_hour['views'].mean().astype(int)
df_total['count_url']=df_grp_hour['url'].count()
layout={ "yaxis": { "type": "log" }}
#layout={}
iplot(go.Figure(data=[go.Scatter(x=df_total.index, y=df_total.count_views, name='count_views'),
                      go.Scatter(x=df_total.index, y=df_total.count_comments, name='count_comments'),
                      go.Scatter(x=df_total.index, y=df_total.mean_views, name='mean_views'),
                      go.Scatter(x=df_total.index, y=df_total.mean_comments, name='mean_comments'),
                      go.Scatter(x=df_total.index, y=df_total.count_url, name='count_url'),                                                                      ],                                                                                                                                 layout=layout ))



df_group_author = df[['author', 'votes_minus', 'url']].groupby('author')
df_author = df_group_author.sum()
df_author.columns = ['total_votes_minus']
df_author['total_articles'] = df_group_author['url'].count()
df_author.fillna(0, inplace=True)
df_author['votes_by_article'] = df_author.total_votes_minus / df_author.total_articles
df_author.votes_by_article = df_author.votes_by_article.astype(int)
df_author[df_author.total_articles > 500].sort_values(by='votes_by_article', ascending=False)[:10]


df.groupby('author')[['votes_minus']].mean().sort_values('votes_minus', ascending=False).head(10)


df['mon_yr'] = [str(p)[:7] for p in df.published]
top10month = df.mon_yr.value_counts()[:10]
df_march_2015 = df[df.mon_yr == '2015-03']
sns.countplot(x='day', data = df_march_2015, hue='domain')

sns.countplot(x='dayofweek', data = df_march_2015, hue='domain')

sns.countplot(x = 'hour', hue = 'dayofweek', data = df[df.dayofweek.isin([1, 6])])



