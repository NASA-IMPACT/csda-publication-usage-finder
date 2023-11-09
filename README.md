# csda-publication-usage-finder
Tool to assist with finding publications on the web which use CSDA data.

Webscrapping and buildilng a tool - to find the publications that we are using CSDA data.


# WIP - Work In Progress

## Features / Actions (What the code does)
- Webscraping tool that can search specific websites to gather Citations (Digital Object Identifier), Acknowledgement Statements, (Possibly other meta info (URL, dates, the publication itself))
  - List(s) of keywords to search on
  - List(s) of websites 
    - Consider Targeted Audience (Who is using the data)
      - Mainly target gov agencies
  - Possible Websites
    - Google Scholar
    - Other Publication Sites
    - SciHub -- Digital Object Identifier
      - Ask for other sites or other methods people have previously used to do these searches manually.

- Citations should be unique - we may need to combine citations that are actually the same but have slight differences.		
- Analytics
  - Which Vendors are using the data
		

## Outputs
- Application Logs (As the application runs, it has a log and/or log group it outputs to)
  - Normal Operation Logs
  - Error Reports
- Raw Data (The JSON data for the citation objects)
- Notifcation System
  - Run Report - after each run the system should notifiy us (email address / slack channel) that it completed (maybe store reports in S3)
  - Notified about differences between the same publication at different time points
    - If the Author revises the publication (Maybe compare diff between publications)
- Report that is easy for management to digest


## Consider The Environment
- Local
  - Locally -with PyEnv - Perhaps docker in the future
  - As we install libraries to make this work, we will create a requirements.txt
- Deployment
  - This process will be deployed within an existing Airflow Container with Task Scheduler (possibly Monthly)

## Other Notes / Future Advancements
- Infomration Type Analysis - Identifying Target Audience, Classificaiton, Characteration of the Publication, Assesment of Type
  - Maybe use AI / Language processing to get an interpretation of the webpage.



## Getting Started
- Create a new Python environment - currently this is running on python 3.8.13
- Example using pyenv and virtualenv.  `pyenv virtualenv 3.8.13 venv.3_8_13_envname`  (Note: This can also be achieved using anaconda)
- Upgrade pip: 
  - `pip install --upgrade pip`
- Install the libs found in the requirements.txt file.




## Draft Items
- Leftover from when I was trying this with Selenium 
  - (UPDATE: Selenium may not be a good way to go - Consider removing) Note: Installing Selenium and Webdriver Manager solves many of these requirements.  `pip install selenium==4.15.2` and `pip install webdriver-manager==4.0.1`
  - scholarly - This is not looking good either.





