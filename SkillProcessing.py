import pandas as pd
#read the scraping csv file
df1=pd.read_csv("testing_ruixin3.csv")

#skill dataframe
df_skill=df1.iloc[:,7:60]
df_skill

Date=df1['Date']
Title_key=df1['Title_key']
Location_key=df1['Location_key']

# get distinct date
Date=Date.drop_duplicates()
Date=Date.reset_index(drop=True)

#get distincet title
Title_key=Title_key.drop_duplicates()
Title_key=Title_key.reset_index(drop=True)

#get distinct location
Location_key=Location_key.drop_duplicates()
Location_key=Location_key.reset_index(drop=True)

#get dustinct skill
Skill=df_skill.columns

results=pd.DataFrame()
#each title, location, date, skill, we compute their count, and sum, we can then calculate the percentage, and make 
#it a dataframe
for t in Title_key:
    for l in Location_key:
        for d in Date:
            for s in Skill:
                count=0
                sum=0
                for i in range(0,len(df_skill)):
                    if(df1['Title_key'][i]==t and df1['Location_key'][i]==l and df1['Date'][i]==d):
                        count=count+df1[s][i]
                        sum=sum+1
                if(sum==0):
                    continue
                else:
                    percentage=count/sum
                Grain=pd.DataFrame({"Title_key":[t],"Location_key":[l],"Date":d,"Skill":s,"Percentage":percentage})
                Grain=Grain[["Title_key","Location_key","Date","Skill","Percentage"]]
                results=results.append(Grain)

results.to_csv("skill1.csv") 