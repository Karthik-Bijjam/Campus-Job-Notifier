# -*- coding: utf-8 -*-
"""


"""

from bs4 import BeautifulSoup
import requests,smtplib
import pickle
from collections import Counter
from pylab import rcParams
import matplotlib.pyplot as plt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

def job_links():
    list =[]
   
    url = "https://agency.governmentjobs.com/nwmissouri/default.cfm?promotionaljobs=1"
    get_page = requests.get(url, headers=headers)
    Page = BeautifulSoup(get_page.text, 'html.parser')
    #print(Page)
    list = Page.find_all('a',class_="jobtitle")
    links = []
    count = 0   
    for job in list:
        try:
        
            page_url ="https://agency.governmentjobs.com/nwmissouri/"+job['href']
            #print(page_url)
            count = count + 1;
            #print(count)
            links.append(page_url)
        except:
                pass
    return links;
#links = job_links()
#print(links)

def job_details(links):
    
    #print('before the loop') 
    old_job_titles = []
    fresh_job_titles = []
    fresh_job_departments = []
    list_job_details = {
               "data":[]
                }
    for url in links:
        #print('after the loop')
        #print(url)
        headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        get_page = requests.get(url, headers=headers)
        individual_job_page = BeautifulSoup(get_page.text, 'html.parser')
        #getPage.raise_for_status()
        data = individual_job_page.find_all('table')
        
        details=[]
        for d in data[1].findAll('td'):      
            #print((d.text).strip())
            details.append((d.text).strip())
            
        job_details = {
                "Job Title": details[0],
                "Opening Date/Time": details[1],
                "Salary": details[2],
                "Job Type": details[3],
                "Location": details[4],
                "Department": details[5]
                }
        list_job_details['data'].append(job_details)
    

    old_job_titles = job_list();
    
    for d in list_job_details['data']:
        title = d['Job Title'] 
        department = d['Department']
        if(not old_job_titles.__contains__(title)):
            fresh_job_titles.append(title)
            fresh_job_departments.append(department)
            

    
    with open('jobs.pkl', 'wb') as f:
        pickle.dump(list_job_details,f,protocol=pickle.HIGHEST_PROTOCOL) 
    return(fresh_job_titles,fresh_job_departments)
    

def job_list():
    jobs_titles = []
    prev_list_job_details = {
               
                }
    with open('jobs.pkl', 'rb') as f:
        
        sentences = pickle.load(f)
        prev_list_job_details = sentences
    if(len(prev_list_job_details)!=0):
        
        for l in prev_list_job_details['data']:
            title = l['Job Title']
            jobs_titles.append(title)
    return jobs_titles

def comparission():        
        titles, departments = job_details(links)
        
        a = dict(Counter(departments))
        def getKeys(a): 
            list_k = [] 
            for key in a.keys(): 
                list_k.append(key) 
                
            return list_k
            
        def getValues(a): 
            list_v = [] 
            for value in a.values(): 
                list_v.append(value) 
                    
            return list_v
        keys = getKeys(a)
        values = getValues(a)
        matplotlib.rcParams.update({'font.size': 15})       
        rcParams['figure.figsize'] = 11, 10
        print(keys)
        print(values)
        fig = plt.figure()
        #length = int(len(a))
        #keys_length = int(len(keys))
        #explode_data = []
        #for a in keys:
        #    e = 0.1;
        #    explode_data.append(e)
        #explode = explode_data
        plt.pie(values, labels=keys, startangle=90, autopct='%1.1f%%')
        plt.axis('equal')  
        plt.tight_layout()
        plt.show()
        fig.savefig('plot.png')  
    



def notification():
    
    titles, departments = job_details(links)
    mailbody = ""
    for title in titles:
        mailbody += title +"\n"
    a = dict(Counter(departments))
    def getKeys(a): 
        list_k = [] 
        for key in a.keys(): 
            list_k.append(key) 
                
        return list_k
            
    def getValues(a): 
        list_v = [] 
        for value in a.values(): 
            list_v.append(value) 
                    
        return list_v
    keys = getKeys(a)
    values = getValues(a)
    
    table_0 = """</br></br></br><h2>Number of jobs per department</h2><table style= font-size="50px">
    <tr style= bgcolor="black !important", font-size= "25px" ><th>Departments </th><th>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Number of Jobs Per Department</th></tr>"""
    table_1 = """</br></br></br></table>"""
    table_data = ""
    count = 0
    for d in keys:
       
        table_data += "<tr><td><h4>"+d+ "</h4></td>"+"<td><h4>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"+ str(values[int(count)]) + "</h4></td></tr>"
        count = count + 1
    
    #msg = []
    mailbody = ""
    
    for title in titles:
        mailbody += "<h4>"+title +"</h4>" +"\n"
  
    
    sender_email = "Sender Eamil Id"
    receiver_email = "Receiver Email Id"
    password = "Sender Email Password"
    #password = input("Type your password and press enter:")
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    
    # Create the plain-text and HTML version of your message
   
    
    html_0 = """\
        <html>
        <body>
        <h1 style= bgcolor="black !important", font-size= "25px", align="center">Jobs updated in the Student Employment Opportunities Page</h1>
        
        <h2>List of jobs<br></h2>
        """
        
    html_1 = """\
   
        
        </body>
        </html>
        """
    
    
    if(len(titles)!=0):
        #msg = "Jobs Updated \n" + mailbody
        text = """\
         Jobs updated in the Student Employment Opportunities Page
        """
        html = html_0 + mailbody+"</br></br></br>"+ table_0 + table_data +  table_1 + html_1
        
        
        
        
    else:
        text = """\
        Jobs does not update in the Student Employment Opportunities Page
        """
        html = """\
        <html>
        <body>
        <h1 style= bgcolor="black", font-size= "25px", align="center">Jobs does not update in the Student Employment Opportunities Page</h1>
        </body>
        </html>
        """
     
    
    
    
    
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(
                sender_email, receiver_email, message.as_string()
                )
    
links = job_links()
job_details(links)
notification()
comparission()
