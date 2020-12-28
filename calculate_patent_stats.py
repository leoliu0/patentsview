import pandas as pd
import sqlite3

db = sqlite3.connect('patentsview.db')

print('read citation ...')
cite = pd.read_sql('select patent_id,citation_id from uspatentcitation',db)
pat = pd.read_sql('select * from patent',db)
print('read patents ...')
#  pat_assg = pd.read_csv('patent_assignee.tsv.zip',sep='\t',low_memory=False)
app = pd.read_sql('select patent_id, app_date from application',db)
#  print('read application ...')
pc = pd.read_sql('select * from uspc',db)

def cal_g_o(df,varname):
    gg = df.groupby('patnum').size()
    g = df.groupby(['patnum',varname])[varname].size().rename('x').reset_index(
                ).merge(gg.rename('total').reset_index())
    g[varname] = (g.x / g.total)**2
    g = 1 - g.groupby('patnum')[varname].sum()
    return g

pc['patent_id'] = pd.to_numeric(pc.patent_id,errors='coerce')
pc = pc[['patent_id','mainclass_id','subclass_id']].dropna()

cite = cite[['patent_id','citation_id']].drop_duplicates()

cite['citation_id'] = pd.to_numeric(cite.citation_id,errors='coerce')
cite['patent_id'] = pd.to_numeric(cite.patent_id,errors='coerce')
cite['patnum'] = pd.to_numeric(cite.citation_id,errors='coerce')

cite = cite.dropna()

fcite = cite.drop('citation_id',axis=1).groupby('patnum').patent_id.count().rename('fcite')

cite.patent_id = pd.to_numeric(cite.patent_id,errors='coerce')

general = cite.drop('citation_id',axis=1).merge(pc).dropna().drop_duplicates()

g_mainclass = cal_g_o(general,'mainclass_id').rename('generality_mainclass')
g_subclass = cal_g_o(general,'subclass_id').rename('generality_subclass')

cite['patnum'] = pd.to_numeric(cite.patent_id,errors='coerce')

cite.columns = ['citation_id', 'patent_id', 'patnum']

bcite = cite.drop('citation_id',axis=1).groupby('patnum').patent_id.count().rename('bcite')

original = cite.drop('citation_id',axis=1).merge(pc).dropna().drop_duplicates()

o_mainclass = cal_g_o(original,'mainclass_id').rename('originality_mainclass')
o_subclass = cal_g_o(original,'subclass_id').rename('originality_subclass')

pat = pat[['patnum','date','num_claims']]

pat = pat.set_index('patnum')

app.patent_id = pd.to_numeric(app.patent_id,errors='coerce')

app = app[['patent_id','date']]

app.columns = ['patnum','app_date']

app['app_date'] = pd.to_datetime(app.app_date,errors='coerce')

app = app.dropna().set_index('patnum')

pat = pat.join(app).join(fcite).join(bcite).join(g_mainclass).join(g_subclass).join(o_mainclass).join(o_subclass)

pat.date = pd.to_datetime(pat.date)

pat.fcite = pat.fcite.fillna(0)
pat.bcite = pat.bcite.fillna(0)

pat.to_sql('patentstats',db,if_exists='replace')
