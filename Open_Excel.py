import pandas as pd
import pickle
import re
def clean_name(name):
    return re.sub(r'^\d+\.?\s*', '', str(name)).title()

if __name__=='__main__':
    df = pd.read_excel('boys_names.xlsx')
    #df.columns=['Names']
    boy_names_names_list = df['Names'].dropna().apply(clean_name).tolist()
    boy_names_set=set(boy_names_names_list)
    with open ('boy_names_set.pkl','wb') as f:
        pickle.dump(boy_names_set,f)
        
    gdf=pd.read_excel('girls_names.xlsx')
    girls_names_list=gdf['Names'].dropna().apply(clean_name).to_list()
    print(girls_names_list)
    girl_name_set=set(girls_names_list)
    with open('girl_names_set.pkl','wb') as f:
        pickle.dump(girl_name_set,f)
    
   


