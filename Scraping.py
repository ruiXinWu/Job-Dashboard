#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests                
from bs4 import BeautifulSoup  
import time                    
import random                  
import pandas as pd
import numpy as np
import re
import datetime
import itertools

import random
#x = [random.randint(0, 9) for p in range(0, 10)]
#print(x)


# In[49]:


base_link='https://www.indeed.com'
#headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

#we can use the function to get random header
def get_headers():
    user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    for _ in user_agent_list:
        #Pick a random user agent
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
    return headers
skill_file = pd.read_csv("ITjobs_dictionary.csv")
dic = skill_file.skills
print(get_headers())


# In[14]:


Q=['software%20engineer','data%20analyst','financial%20advisor','data%20engineer','security%20engineer','web%20developer']
#Q=['Physical%20Therapist%20Assistants','Dental%20Assistants','Home%20Health%20Aids','Nurses','Occupational%20Therapists','Childcare%20Workers']
#Q=['Physical%20Therapist%20Assistants','Dental%20Hygienists','Surgical%20Technologists','Radiation%20Therapists','Diagnostic%20Medical%20Sonographers','Phlebotomists']
#L=['Alameda%20County','Alpine%20County','Amador%20County','Butte%20County','Calaveras%20County','Colusa%20County','Contra%20Costa%20County','Del%20Norte%20County','El%20Dorado%20County','Fresno%20County','Glenn%20County','Humboldt%20County','Imperial%20County','Inyo%20County','Kern%20County','Kings%20County','Lake%20County','Lassen%20County','Los%20Angeles%20County']
#L=['Marin%20County','Mariposa%20County','Mendocino%20County','Merced%20County','Modoc%20County','Mono%20County','Monterey%20County','Napa%20County','Nevada%20County','Orange%20County','Placer%20County','Plumas%20County','Riverside%20County','Sacramento%20County','San%20Benito%20County','San%20Bernardino%20County','San%20Diego%20County','San%20Francisco%20County','San%20Joaquin%20County','San%20Luis%20Opispo%20County','San%20Mateo%20County','Santa%20Barbara%20County','Santa%20Clara%20County','Santa%20Cruz%20County','Shasta%20County','Sierra%20County']
L=['Siskiyou%20County','Solano%20County','Sonoma%20County','Stanislaus%20County','Sutter%20County','Tehama%20County','Toulumne%20County','Trinity%20County','Tulare%20County','Ventura%20County','Yolo%20County','Yuba%20County']
#L=['Alameda%20County','Alpine%20County','Amador%20County','Butte%20County','Calaveras%20County','Colusa%20County','Contra%20Costa%20County','Del%20Norte%20County','El%20Dorado%20County','Fresno%20County','Glenn%20County','Humboldt%20County','Imperial%20County','Inyo%20County','Kern%20County','Kings%20County','Lake%20County','Lassen%20County','Los%20Angeles%20County’, ’Marin%20County','Mariposa%20County','Mendocino%20County','Merced%20County','Modoc%20County','Mono%20County','Monterey%20County','Napa%20County','Nevada%20County','Orange%20County','Placer%20County','Plumas%20County','Riverside%20County','Sacramento%20County','San%20Benito%20County','San%20Bernardino%20County','San%20Diego%20County','San%20Francisco%20County','San%20Joaquin%20County','San%20Luis%20Opispo%20County','San%20Mateo%20County','Santa%20Barbara%20County','Santa%20Clara%20County','Santa%20Cruz%20County','Shasta%20County','Sierra%20County’, ’Siskiyou%20County','Solano%20County','Sonoma%20County','Stanislaus%20County','Sutter%20County','Tehama%20County','Toulumne%20County','Trinity%20County','Tulare%20County','Ventura%20County','Yolo%20County','Yuba%20County']
Q_L=[q_l for q_l in itertools.product(Q,L,[0])]

# In[50]:


#Functions for detailed page
def get_location(lst):
    location_index=[index for (index,value) in enumerate(lst) if ", " in value]
    if len(location_index)==0:
        return "Remote"
    return lst[location_index[0]]

def findLargestYearFromWord(text):
    ls = list()
    for w in text.split():
        try:
            ls.append(int(w))
        except:
            pass
    try:
        return max(ls)
    except:
        return -1

def findLargestYearFromDescription(text):
    j = 0
    for i in text:
        cur = findLargestYearFromWord(i)
        if cur != -1 and cur > j:
            j = cur
    if(j != 0):
        return j
    else:
        return None

def specific_skills_edu(text):
#    dic = ["python","java","sql","tableau"]
    O=""
    for i in dic:
        O=O+"1" if i in text else O+"0"
    return O
    
def Current_Date(N_days_Ago):
    if N_days_Ago.lower()=="today" or N_days_Ago.lower()=="just":
        return datetime.date.today()
    elif N_days_Ago.lower()=="":
        return ""
    else:
        return datetime.date.today()+datetime.timedelta(days=-int(N_days_Ago))

#get detail page url    
def get_detail_page(home_page,headers):
    headers1={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'}
    r=requests.get(home_page,headers=headers1) #the home page must come from keyword search, instead of the general-entry home page
    soup_href=BeautifulSoup(r.text,'html.parser').select('.jobTitle.jobTitle-newJob > a')
    detail_pages=["https://www.indeed.com"+i['href'] for i in soup_href]
    return detail_pages

#given detail page url, return dataframe of detail information
def details(url,q_l):
    soup=BeautifulSoup(requests.get(url,headers=headers).text,'html.parser')
    
#we have to check the length of all the soup.select ,as it might be empty.    
    Title=""
    soup_title=soup.select('.jobsearch-JobInfoHeader-title-container > h1')
    if len(soup_title)>0:
        Title=soup_title[0].text
    
    
    #Company=soup.select('.icl-u-lg-mr--sm.icl-u-xs-mr--xs > a')[0].get_text()
    
    
    Company=""
    soup_Company=soup.select(".icl-u-lg-mr--sm.icl-u-xs-mr--xs > a")
    if len(soup_Company)>0:
        Company=soup_Company[0].get_text()
    
    
    
    Description=""
    soup_Description=soup.select('#jobDescriptionText')
    if len(soup_Description)>0:
        Description=soup_Description[0].get_text()
        
        
    Location=""
    soup_Location=soup.select('.jobsearch-CompanyInfoContainer')
    if len(soup_Location)>0:
        Location=get_location(soup_Location[0].get_text("|").split("|"))
    
    
    Salary=""
    soup_Salary=soup.select('.jobsearch-JobDescriptionSection-sectionItem')
    if len(soup_Salary)>0:
        text =soup_Salary[0].get_text()
        Salary = re.findall(r'\$[\d|\,]+', text)
        Salary = [int(temp.strip('$').replace(",","")) for temp in Salary]
        if(sum(Salary)==0):
            Salary=0
        else:
            Salary = sum(Salary)/len(Salary)
        if text.find("year") != -1:
            if text.lower().find("k")!=-1:
                Salary = Salary * 1000
        if text.find("hour") != -1:
            Salary = Salary * 40 *52
        #Salary = int(round(float(Salary.strip('$').replace(",",""))))
        #print(f"Salary: {Salary}")
        
    #<span class="">$75,000 - $85,000 a year</span>
    #soup_Salary=soup.select('<div class="jobsearch-JobDescriptionSection-sectionItem"><div class="jobsearch-JobDescriptionSection-sectionItemKey icl-u-textBold">Salary</div><span class="icl-u-xs-mr--xs">$170,752 - $200,000 a year</span></div>')
    #<div id="jobDetailsSection" class="jobsearch-JobDescriptionSection-section"><div class="jobsearch-JobDescriptionSection-title"><h2 class="jobsearch-JobDescriptionSection-title--main icl-u-textBold" tabindex="-1" id="jobDetails">Job details</h2></div><div class="jobsearch-JobDescriptionSection-sectionItem"><div class="jobsearch-JobDescriptionSection-sectionItemKey icl-u-textBold">Salary</div><span class="icl-u-xs-mr--xs">$75,000 - $85,000 a year</span></div><div class="jobsearch-JobDescriptionSection-sectionItem"><div class="jobsearch-JobDescriptionSection-sectionItemKey icl-u-textBold">Job Type</div><div>Full-time</div></div></div>
    
    #Experience=""
    text=re.findall('[0-9].*years.*experience.*.|[0-9].*year.*experience.*|[a-z]+:.*[0-9].*years|.*[a-z]+:.[0-9].year', Description, flags=re.IGNORECASE) 
    Experience = findLargestYearFromDescription(text)
    
    N_days_Ago=""
   
    
    
    
    
    
    N_days_Ago=""
    soup_N_days_Ago=soup.select('p.jobsearch-HiringInsights-entry--bullet > span.jobsearch-HiringInsights-entry--text')
    if(len(soup_N_days_Ago)>0):
        N_days_Ago=soup_N_days_Ago[0].get_text().split()[1]
    Date=N_days_Ago
    Grain=pd.DataFrame({"Title":[Title],"Company":Company,"Location":[Location],"Date":Date,"Salary":Salary,"Experience":Experience})
    Grain=Grain[["Title","Company","Location","Date","Salary","Experience"]]
    temp=0
    for ii in dic:
        Grain[ii]=specific_skills_edu(Description)[temp]
        temp+=1
    Grain["Title_key"]=q_l[0].replace("%20",' ')
    Grain["Location_key"]=q_l[1].replace("%20",' ')
    
    #drop duplicate content for each page result
    Grain=Grain.drop_duplicates()
    Grain=Grain[Grain['Date']!=""]
    for i in Grain['Date']:
        Grain['Date']=Current_Date(i)
    return Grain


# In[ ]:





# In[51]:


results=pd.DataFrame()

for q_l in Q_L:
    #1 page needs 10 steps,here we scrap at most 5 pages
    for j in range(0,400,10):
        #home page
        headers=get_headers()
        first_home_page_url="https://www.indeed.com/jobs?q={}&l={}&radius=100&fromage=1&start={}".format(q_l[0],q_l[1],j)
        first_home_page_parsed=BeautifulSoup(requests.get(first_home_page_url,headers=headers).text,'html.parser')
        print(first_home_page_url)
        #for loop is to use all detail pages in a home page
        #we get random headers to scrap each page
        for detail_page_url in get_detail_page(first_home_page_url,headers):
            #print(detail_page_url)
            
            #using "detail" function above, append each detail dataframe in results dataframe
            results=results.append(details(detail_page_url,q_l))
            
            #time.sleep(random.randint(0, 9))
        #if next page button is unavailable in the homepage, it means there is no next page, we go out of the loop
        next_page=first_home_page_parsed.find("a",{"aria-label":"Next"})
        if(next_page is None):
            break
      


# In[37]:


results


# In[7]:



titlekey1=Q[0]
city1=L[0]
results.to_csv("testing_ruixin3.csv")  


# In[ ]:





# In[6]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




                    
 


# In[ ]:




