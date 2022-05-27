import tkinter as tk                    
from tkinter import CENTER, END, W, Entry, Frame, Label, OptionMenu, StringVar, Variable, ttk
#from typing import Counter
#from flask import redirect
from matplotlib.pyplot import text
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import PhotoImage, Canvas
from tkinter.scrolledtext import ScrolledText

from tkinter.messagebox import NO
#from turtle import clear, width
#from click import option
#from ib_insync import Stock, Ticker

import matplotlib
from matplotlib import style
from requests import options

matplotlib.use('TkAgg') #This is the backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

from urllib.request import urlopen
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime, timedelta, date
import string
from string import digits
import nltk


#NEED TO INSTALL STOPWORDS BEFORE USING FUNCTION
#Comment it back when done
#nltk.download()
from nltk.corpus import stopwords

import csv
import pandas as pd
import numpy as np

from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
import time as timer

from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo

import pickle


#count for the dataframes
dfcount = 0 

#The size and style desired for our texts
V_LARGE_FONT = ('Verdana', 20)
LARGE_FONT = ('Verdana', 14)
NORM_FONT = ('Verdana', 12)
SMALL_FONT = ('Verdana', 10)

#Function of the tutorial, every time you click on the next page it destroys the previous one and create a new page
def tutorial():

    def page1():
        tut.destroy()
        tut1 = tk.Tk()

        def page2():
            tut1.destroy()
            tut2 = tk.Tk()

            def page3():
                tut2.destroy()
                tut3 = tk.Tk()

                def page4():
                    tut3.destroy()
                    tut4 = tk.Tk()

                    tut4.wm_title('Live Trading')
                    label5 = ttk.Label(tut4, text='This is where the magic operates.\nYou can access the most recent transcripts with a dropdown option that will display\n for you the companies that have a transcript announced on the same day.\nYou just have to click the button to get the suggestion of the algorithm!',
                                    justify='center',
                                    font=NORM_FONT)
                    label5.pack(padx=40, pady=40)
                    button5 = ttk.Button(tut4, text='Done', width=8, command=tut4.destroy)
                    button5.place(rely=0.5, relx=0.5, anchor=CENTER)
                    tut4.geometry('700x400')
                    tut4.mainloop()

                tut3.wm_title('Statistics')
                label4 = ttk.Label(tut3, text='If you want more, here are more informations\nyou can find on any company listed, scrapped on Yahoo Finance',
                                justify='center',
                                font=NORM_FONT)
                label4.pack(padx=40, pady=40)
                button4 = ttk.Button(tut3, text='Next', width=8, command=page4)
                button4.place(rely=0.5, relx=0.5, anchor=CENTER)
                tut3.geometry('700x400')
                tut3.mainloop()

            tut2.wm_title('Stock Prices')
            label3 = ttk.Label(tut2, text='In this section you can access to the evolution\nof the company chosen by its ticker with the associated last price record',
                            justify='center',
                            font=NORM_FONT)
            label3.pack(padx=40, pady=40)
            button3 = ttk.Button(tut2, text='Next', width=8, command=page3)
            button3.place(rely=0.5, relx=0.5, anchor=CENTER)
            tut2.geometry('700x400')
            tut2.mainloop()
    
        tut1.wm_title('Transcript')
        label2 = ttk.Label(tut1, text='In this part of the application, you can find two lists.\nOn one side you will find the upcoming transcripts with an EPS estimate scrapped from Yahoo Finance.\nOn the other we displayed the effect of the earning calls on the stock price with different time intervals',
                        justify='center',
                        font=NORM_FONT)
        label2.pack(padx=40, pady=40)
        button2 = ttk.Button(tut1, text='Next', width=8, command=page2)
        button2.place(rely=0.5, relx=0.5, anchor=CENTER)
        tut1.geometry('700x400')
        tut1.mainloop()
    
    tut = tk.Tk()
    tut.wm_title('Tutorial')
    label1 = ttk.Label(tut, text='''Here is a little tutorial for you to go through\nif you need any information about the application's features''',
                    justify='center',
                    font=NORM_FONT)
    label1.pack(padx=40, pady=40)

    button1 = ttk.Button(tut, text='Begin', width=8, command=page1)
    button1.place(rely=0.5, relx=0.5, anchor=CENTER)

    tut.geometry('700x400')
    tut.mainloop()

#The style of graph for the stock price
style.use('ggplot')

#Define the type of value in the dropdown and a list of it's composents
with open('ticker_list.txt', 'r') as f:
    stock = f.readlines()

#A popupmsg function that can be used anytime we want something to be displayed when clicked. Just have to change the text
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title('!')
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side='top', fill='x', pady=10)
    B1 = ttk.Button(popup,text='Okay', width=5, command=popup.destroy)
    B1.pack()
    popup.mainloop()

#working dataframe over past transcript releases
dfpast = pd.read_pickle('dfpast.pkl')
dfpast = dfpast.values.tolist()

#Put manually the calendar when application is openned
#Replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
CSV_URL = 'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=8LC2XZN9YP6QZEW0'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)

df = pd.DataFrame(my_list, columns=my_list[0])
df.drop(df.head(1).index,inplace=True)
df = df.sort_values(by='reportDate')
earning_call = df.rename(columns={'symbol': 'Symbol',
                            'name': 'Company Name', 
                            'reportDate': 'Reporting date', 
                            'fiscalDateEnding': 'Fiscal date ending',
                            'estimate': 'EPS estimate', 
                            'currency': 'Currency'})

truncated_earning_call = earning_call.head(500)
truncated_earning_call = truncated_earning_call.values.tolist()


# root window
root = tk.Tk()
root.geometry('300x120')
root.title('Live webscrapping transcript')


# progressbar
pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=280)

# place the progressbar
pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)


def update_progress_label():
    return f"Current Progress: {pb['value']}%"


# label
value_label = ttk.Label(root, font=NORM_FONT, text=update_progress_label())
value_label.grid(column=0, row=1, columnspan=2)

def progress():
    if pb['value'] < 100:
        pb['value'] += 10
        value_label['text'] = update_progress_label()
    else:
        showinfo(message='Transcripts from last days are downloaded')
        root.destroy()

#update progress bar 1/10
progress()
root.update()


# # label
# value_label = ttk.Label(root, text=update_progress_label())
# value_label.grid(column=0, row=1, columnspan=2)

#Getting previous transcripts
def Get_transcript():

            callParticipantsList = []
            preparedRemarksContentList = []
            questionAnswerContentList = []
            companyNameList = []
            tickerList = []
            dateList = []
            timeList=[]
            quarterList=[]

            #update progress bar 2 /10
            progress()
            root.update()

            listofurls = []

            #go to each page and get a list of link to single transcripts
            for x in range(1,3):
                url = 'https://www.fool.com/earnings-call-transcripts/?page='+str(x)
                response = requests.get(url)
                page = response.text

                #update progress bar 3, 4
                progress()
                root.update()


                soup = BeautifulSoup(page, "lxml")
                for a in soup.find(class_="content-block listed-articles recent-articles m-np").find_all('a', href=True):
                    listofurls.append('https://www.fool.com'+str(a['href']))

            truncatedList = listofurls[:]
            truncatedList = list(set(truncatedList))


            #update progress bar 5/10
            progress()
            root.update()

            for x in truncatedList:

                url = str(x)
                response = requests.get(url)
                page = response.text
                soup = BeautifulSoup(page, "lxml")

                try:
                    companyName = [soup.find(class_='tailwind-article-body').find_all('p')[1].find('strong').text]

                    for x in companyName:
                        companyNameList.append(x)

                except:
                    companyNameList.append(0)
                    
                #I use error habdling as some pages have different acces path to data
                try:
                    ticker = [soup.find(class_='tailwind-article-body').find_all('p')[1].find(class_='ticker-symbol').text.replace(')',"").replace('(',"")]

                    for x in ticker:
                        tickerList.append(x)

                except:
                    tickerList.append(0)

                try:
                    dateL = [soup.find(class_='tailwind-article-body').find_all('p')[1].find(id='date').text]

                    for x in dateL:
                        dateList.append(x)

                except:
                    dateList.append(0)

                try:
                    time = [soup.find(class_='tailwind-article-body').find_all('p')[1].find(id='time').text]

                    for x in time:
                        timeList.append(x)
                except:
                    timeList.append(0)

                try: 

                    quarter = [' '.join(soup.find(class_='md:w-3/4 md:pr-48px').find('header').text.split()[-5:-3])]

                    for x in quarter:
                        quarterList.append(x)
        
                except:
                    quarterList.append(0)

                namesList = []
                rolesList = []

                try:
                    for name in (soup.find(class_='tailwind-article-body').find_all('h2')[-1].find_all_next('strong')):
                        namesList.append(name.text)
                    for role in (soup.find(class_='tailwind-article-body').find_all('h2')[-1].find_all_next('em')):
                        rolesList.append(role.text)
                    callParticipants = [list(zip(namesList, rolesList))]
                    for x in callParticipants:
                        callParticipantsList.append([x])
                except:
                    callParticipantsList.append([0])

                try:
                    toc = []
                    for x in soup.find(class_='tailwind-article-body').find_all('h2'):
                        #take a list of all the categories of the call in h2 (html)
                        toc.append(x.text)

                    if 'Questions & Answers:' or 'Questions and Answers:'in toc:
                        qanda = []
                        #doesn't work if start immediately with QA see netflix case Q1 2022
                        for div in soup.find(class_='tailwind-article-body').find_all('h2')[2].find_all_next('p'):
                            #check why find_all_next stays blank
                            #creates a list for all paragraphs happening for the QA part of the call
                            qanda.append(div.text)

                        for x in qanda:
                            if 'Duration:' in x:
                                #if duration of call is mentionned store its location inside in duration Placement
                                durationPlacement = qanda.index(x)
                            
                        # we need to get rid of bottom text, as duration is at the end we delete what comes after
                        questionAnswerContentList.append(qanda[:durationPlacement])


                    else:
                        #if non-existing QA append 0
                        questionAnswerContentList.append(0)  
                except: 
                        questionAnswerContentList.append(0)

                try:
                    preparedRemarks = []
                    prIndex = []
                    #select all content in p after word operator
                    for div in soup.find(class_='tailwind-article-body').find_all('p')[4:]:
                        #add the content of each paragraph to a list
                        preparedRemarks.append(div.text)
                    #prev prindex here, only showed first line now moved it to top and it works fine
                    for x in preparedRemarks:
                        # or or '[Operator instructions]'
                        if 'Operator' in x:
                            #find index of operator and store it in prIndex
                            prIndex.append(preparedRemarks.index(x))
                        else:
                            None
                    if len(prIndex) == 0:
                        None
                    else:
                        #operator starts the QA section always so we can stop prepared remarks just before second occurence of word operator
                        preparedRemarksContent = [preparedRemarks[:prIndex[1]]]

                    for x in preparedRemarksContent:
                        preparedRemarksContentList.append(x)
                except:
                    preparedRemarksContentList.append(0)

            #update progress bar 6/10
            progress()
            root.update()

            happy_data = pd.DataFrame(
                                        {'Ticker': tickerList[:],
                                        'Company': companyNameList[:], 
                                        'Quarter': quarterList[:], 
                                        'Date': dateList[:],
                                        'Time': timeList[:], 
                                        'Prepared comments': preparedRemarksContentList[:], 
                                        'Q&A': questionAnswerContentList[:],
                                        'Call participant': callParticipantsList})

            #cleaning data for missing values
            for i in list(happy_data.columns):
                happy_data = happy_data[happy_data[i] != 0]

            #update progress bar 7/10
            progress()
            root.update()


            # rename

            full_data = happy_data

            full_data = full_data.set_index('Ticker').sort_index()[['Company', 'Quarter', 'Date', 'Time', 'Prepared comments', 'Q&A', 'Call participant']]

            
            #droping empty values
            full_data = full_data.drop(full_data.loc[full_data['Date']==''].index)
            TickerList = list(full_data.index)
            DateList = list(full_data.Date)


            #update progress bar 7/10
            progress()
            root.update()

            def to_abb(x):

                """
                Function tranforms strings variables of data to a standardized written form
                Not pretty code, but it makes the following standardization possible
                """

                x=x.replace(',', '').replace('.', '')
                x=x.replace('January', 'Jan').replace('February','Feb')
                x=x.replace('March', 'Mar').replace('April', 'Apr')
                x=x.replace('June', 'Jun').replace('July', 'Jul')
                x=x.replace('August', 'Aug').replace('September', 'Sep')
                x=x.replace('October', 'Oct').replace('November', 'Nov')
                x=x.replace('December', 'Dec')
                return x

            for i in range(len(DateList)):
                #removing the boring comma in date format and formating month to abbreviated form
                temp = to_abb(str(DateList[i]))
                DateList[i] = temp
                #changing format from string to timestamps
                DateList[i] = datetime.strptime(DateList[i], '%b %d %Y')

            full_data['Date'] = DateList

            #update progress bar 8/10
            progress()
            root.update()

            full_data.reset_index(inplace=True)

            # we merge prepared comment and Q&A in case we need an analysis of the full trancript
            full_data['merged'] = full_data['Prepared comments'] + full_data['Q&A']

            # attempt to clean names/functions/numbers 
            #looks like it works for now
            def clean_text(dataframe, column, names):

                ''' 
                this function cleans all the stopwords, numbers,  names and functions from a text. 
                dataframe :  name of dataframe to clean
                column : column of dataframe to clean
                names :  list of names to clean from text (it also includes positions of employees)

                '''

                stop_words = stopwords.words('english')
                list_to_append = []

                for i in range(len(dataframe)):

                    NamesList = []
                    temp_name_list = []
                    cleanedNames_text = []

                    temp_list_name = str(dataframe[names][i][0]).translate(str.maketrans('', '', string.punctuation)).lower().split(" ")

                    #create a list of names/functions without initials
                    for x in temp_list_name:
                        if len(x) > 2:
                            NamesList.append(x)
                        NamesList.append('operator')
                        NamesList.append('instructions')

                    dataframe.at[i, names] = NamesList


                    #use created list to take out all the names and functions from text of Q/A or prepared comments
                    #first take out punctuation and upper case letters

                    temp_list_text = str(dataframe[column][i]).translate(str.maketrans('', '', string.punctuation)).lower()
                    temp_list_text = temp_list_text.translate(str.maketrans('', '', digits)).split(" ")
                    cleanedNames_text = [word for word in temp_list_text if word not in NamesList]
                    cleanedstopwords_text = [word for word in cleanedNames_text if word not in stop_words]
                    #the next 2 lines would be used if we only want to keep english words
                    #allcleaned = [word for word in cleanedstopwords_text if word not in set(nltk.corpus.words.words())]
                    #dataframe.at[i, column] = " ".join(allcleaned)
                    list_to_append.append(" ".join(cleanedstopwords_text))

                #when we appended all text to list, we append new column (list_to_append) to dataframe
                dataframe['Cleaned Prepared comments'] = list_to_append

            
            clean_text(full_data, 'Prepared comments', 'Call participant')

            #update progress bar 9/10
            progress()
            root.update()

            clean_text(full_data, 'merged', 'Call participant')

            today = date.today()
            todays_transcript = pd.DataFrame()
            todaysminus_1_transcript = pd.DataFrame()
            todaysminus_2_transcript = pd.DataFrame()
            todaysminus_3_transcript = pd.DataFrame()
            
            #update progress bar 10/10
            progress()
            root.update()

            for i in range(len(full_data)):

                if full_data.iloc[i]['Date'].strftime('%Y-%m-%d') == str(today):
                    todays_transcript = pd.concat([todays_transcript, full_data.iloc[[i]]])
                elif full_data.iloc[i]['Date'].strftime('%Y-%m-%d') == str(today - timedelta(days=1)):
                    todaysminus_1_transcript = pd.concat([todaysminus_1_transcript, full_data.iloc[[i]]])
                elif full_data.iloc[i]['Date'].strftime('%Y-%m-%d') == str(today - timedelta(days=2)):
                    todaysminus_2_transcript = pd.concat([todaysminus_2_transcript, full_data.iloc[[i]]])
                else:
                    todaysminus_3_transcript = pd.concat([todaysminus_3_transcript, full_data.iloc[[i]]])

            past4days = full_data.sort_values(by='Date')



            return past4days

past4days = Get_transcript()

# ###updating loading bar
# for i in range(1,9):
#     timer.sleep(0.05)
#     progress()
#     root.update()

root.mainloop()

#Creating the bone structure of the application which will be the parent of all the subpages
class EarningDrift(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, 'Post Earnings Announcement Drift Strategy Algorithm')

        #the container that will populate all of our elements
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        #or if you have a lot of things to put in a page you use this functionnality
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Here is the code in order to add things in the mac tab
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save settings', command=lambda: popupmsg('Not supported yet!'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='Tutorial', command=tutorial)
        menubar.add_cascade(label='Help', menu=helpmenu)

        tk.Tk.config(self, menu=menubar)

        #Now this is where your are going to add all the pages created with the loop
        self.frames = {}

        for F in (StartPage, Disclaimer, HomePage, PageOneFuture, PageOnePast, PageTwo, Stats, LiveTranscript):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)
    
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

#Now we create the instance which will show up as a starting page
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Welcome to the PEAD application', font=V_LARGE_FONT)
        label.place(rely=0.3, relx=0.5, anchor=CENTER)

        button1 = ttk.Button(self, text='Next', width=8, command=lambda: controller.show_frame(Disclaimer))
        button1.place(rely=0.5, relx=0.5, anchor=CENTER)

#This is the disclaimer page
class Disclaimer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""DISCLAIMER
        This application does not promise any type of warranty concerning startegies given by the algorithm.
        You are the only one responsible for the outcome of your transactions. So use it at your own risk.
        But most importantly, have fun!""", font=LARGE_FONT)
        label.place(rely=0.3, relx=0.5, anchor=CENTER)

        button1 = ttk.Button(self, text='Agree', width=8, command=lambda: controller.show_frame(HomePage))
        button1.place(rely=0.5, relx=0.4, anchor=CENTER)

        button2 = ttk.Button(self, text='Disagree', width=8, command=quit)
        button2.place(rely=0.5, relx=0.6, anchor=CENTER)

#This is the home page where you get access to all our features
class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Welcome to the user interface', font=V_LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Future Transcript Calendar', width=18, command=lambda: controller.show_frame(PageOneFuture))
        button1.place(rely=0.3, relx=0.5, anchor=CENTER)

        button2 = ttk.Button(self, text='Past Transcript Calendar', width=18, command=lambda: controller.show_frame(PageOnePast))
        button2.place(rely=0.35, relx=0.5, anchor=CENTER)

        button3 = ttk.Button(self, text='Stock Prices', width=18, command=lambda: controller.show_frame(PageTwo))
        button3.place(rely=0.45, relx=0.5, anchor=CENTER)

        button4 = ttk.Button(self, text='Statistics', width=18, command=lambda: controller.show_frame(Stats))
        button4.place(rely=0.5, relx=0.5, anchor=CENTER)

        button5 = ttk.Button(self, text='Live Transcript', width=18, command=lambda: controller.show_frame(LiveTranscript))
        button5.place(rely=0.6, relx=0.5, anchor=CENTER)

class PageOneFuture(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Future Transcript Calendar', font=V_LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Back to Welcome Page', width=18, command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text='Past Transcript Calendar', width=18, command = lambda: controller.show_frame(PageOnePast))
        button2.pack()


        #Here is the first dataframe with its loop
        frame = ttk.Treeview(self, height= 20)
        frame['columns'] = ('Symbol', 'Company Name', 'Reporting date', 'Fiscal date ending', 'EPS estimate', 'Currency')
        frame.column('#0', width=0, stretch=NO)
        frame.column('Symbol', anchor=W, width=150, minwidth=150)
        frame.column('Company Name', anchor=W, width=400, stretch=NO)
        frame.column('Reporting date', anchor=CENTER, width=250, stretch=NO)
        frame.column('Fiscal date ending', anchor=CENTER, width=250, stretch=NO)
        frame.column('EPS estimate', anchor=CENTER, width=200, stretch=NO)
        frame.column('Currency', anchor=CENTER, width=150, stretch=NO)
        frame.heading('#0', text='')
        frame.heading('Symbol', text='Ticker', anchor=W)
        frame.heading('Company Name', text='Company Name', anchor=W)
        frame.heading('Reporting date', text='Reporting Date', anchor=CENTER)
        frame.heading('Fiscal date ending', text='Fiscal date ending', anchor=CENTER)
        frame.heading('EPS estimate', text='EPS estimate', anchor=CENTER)
        frame.heading('Currency', text='Currency', anchor=CENTER)

        frame.tag_configure('oddrow', background='grey15')
        frame.tag_configure('evenrow', background='grey20')

        count = 0
        for record in truncated_earning_call:
            if count%2==0:
                frame.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3],
                            record[4], record[5]), tags=('evenrow'))
            else:
                frame.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3],
                            record[4], record[5]), tags=('oddrow'))
            count += 1
        
        frame.pack(fill=tk.BOTH, expand=True)

class PageOnePast(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Past Transcript Calendar', font=V_LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Back to Welcome Page', width=18, command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text='Future Transcript Calendar', width=18, command = lambda: controller.show_frame(PageOneFuture))
        button2.pack()

        frame = ttk.Treeview(self, height= 20)
        frame['columns'] = ('Ticker', 'Dates of Report', '% surprise EPS', '% surprise Revenue',
                            'pct_t10_', 'pct_t30', 'pct_t60')


        #Here is the second dataframe
        frame.column('#0', width=0, stretch=NO)
        frame.column('Ticker', anchor=W, width=150, minwidth=150)
        frame.column('Dates of Report', anchor=CENTER, width=250, stretch=NO)
        frame.column('% surprise EPS', anchor=CENTER, width=200, stretch=NO)
        frame.column('% surprise Revenue', anchor=CENTER, width=200, stretch=NO)
        frame.column('pct_t10_', anchor=CENTER, width=200, stretch=NO)
        frame.column('pct_t30', anchor=CENTER, width=200, stretch=NO)
        frame.column('pct_t60', anchor=CENTER, width=200, stretch=NO)

        frame.heading('#0', text='')
        frame.heading('Ticker', text='Ticker', anchor=W)
        frame.heading('Dates of Report', text='Dates of Report', anchor=CENTER)
        frame.heading('% surprise EPS', text='% Surprise EPS', anchor=CENTER)
        frame.heading('% surprise Revenue', text='% Surprise Revenue', anchor=CENTER)
        frame.heading('pct_t10_', text='% 10 days', anchor=CENTER)
        frame.heading('pct_t30', text='% 30 days', anchor=CENTER)
        frame.heading('pct_t60', text='% 60 days', anchor=CENTER)

        frame.tag_configure('oddrow', background='grey15')
        frame.tag_configure('evenrow', background='grey20')

        count = 0
        for record in dfpast:
            if count%2==0:
                frame.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], round(float(record[2]), 2), round(float(record[3]),2),
                            round(float(record[4]),2), round(float(record[5]),2), round(float(record[6]),2)), tags=('evenrow'))
            else:
                frame.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], round(float(record[2]), 2), round(float(record[3]),2),
                            round(float(record[4]),2), round(float(record[5]),2), round(float(record[6]),2)), tags=('oddrow'))
            count += 1
        
        frame.pack(fill=tk.BOTH, expand=True)
    
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Stock prices', font=V_LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Back to Welcome Page', width=18, command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text='Statistics', width=18, command=lambda: controller.show_frame(Stats))
        button2.pack()

        entry = AutocompleteCombobox(self, 
                                    width=30, 
                                    font=LARGE_FONT,
                                    completevalues=stock, 
                                    )
        entry.get()
        entry.pack()


        #This piece of code is for the stock price chart
        f = Figure(figsize=(11,5), dpi=100)
        a = f.add_subplot(111)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)            
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #The function that will take the ticker as an input and return the data, display it on the graph
        def Get_stock():
            try:
                ticker = entry.get()
                ltick = len(ticker)
                a.clear()
                data = yf.Ticker(ticker[0:ltick-1])
                data = data.history(period='3mo')
                data = pd.DataFrame(data)
                data.reset_index(inplace=True)
                df2 = data[['Date','Close']].groupby('Date').sum()
                df2.plot(kind='line', legend=True, ax=a, color='#183A54',marker=',', fontsize=10)
                title = 'Last price recorded ' + str(data['Close'][60].round(4))
                a.set_title(title)
                canvas.draw()
            except: 
                popupmsg('Nothing is found for this ticker. Check typing. The stock may also be delisted')

        button3 = ttk.Button(self, text='Apply', width=8, command=Get_stock)
        button3.pack()

class Stats(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Stock specific statistics', font=V_LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Back to Welcome Page', width=18, command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text='Stock prices', width=18, command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        autoboxinfo = AutocompleteCombobox(self,  
                                    width=30, 
                                    font=LARGE_FONT,
                                    completevalues=stock
                                    )
        autoboxinfo.get()
        autoboxinfo.pack()


        #Same as stock price but this time we ask for some information on a chosen company
        def Get_stock_stats():
            try:
                framestat.delete(*framestat.get_children())
                tickset = autoboxinfo.get()
                lengthtickset = len(tickset) 
                datainfo = yf.Ticker(tickset[0:lengthtickset-1]).info
                datainfo = pd.DataFrame.from_dict(datainfo, orient='index').T
                datainfo =  datainfo[['shortName','longBusinessSummary',
                                    'country','industry','recommendationKey',
                                    'numberOfAnalystOpinions','targetLowPrice',
                                    'targetMedianPrice','targetHighPrice','forwardEps',
                                    'priceToBook','beta','averageDailyVolume10Day']]
                
                disp_business_sum.delete('1.0', END)
                business_sum = str(datainfo.iloc[0]['longBusinessSummary'])
                disp_business_sum.insert('1.0', business_sum)
                datainfo = datainfo.values.tolist()

                count = 0

                for record in datainfo :
                    framestat.insert(parent='', index='end', iid=count, text='', values=(record[0],
                                    record[2],record[3], record[4],record[5],record[6],record[7],
                                    record[8],record[9],record[10],record[11],record[12]))
                    count += 1
                framestat.pack(fill=tk.BOTH)
                label_sum.pack()
                disp_business_sum.pack(fill=tk.BOTH, expand=True)
                return datainfo
                
            except:
                popupmsg('Nothing is found for this ticker. Check typing. The stock may also be delisted')
        label_sum = ttk.Label(self, text='Business description', font=V_LARGE_FONT)
        framestat = ttk.Treeview(self, height= 5)
        framestat['columns'] = ('shortName',
                                    'country','industry','recommendationKey',
                                    'numberOfAnalystOpinions','targetLowPrice',
                                    'targetMedianPrice','targetHighPrice','forwardEps',
                                    'priceToBook','beta','averageDailyVolume10Day')
        framestat.column('#0', width=0, stretch=NO)
        framestat.column('shortName', anchor=W, width=120, minwidth=120)
        framestat.column('country', anchor=W, width=100, stretch=NO)
        framestat.column('industry', anchor=W, width=100, stretch=NO)
        framestat.column('recommendationKey', anchor=CENTER, width=100, stretch=NO)
        framestat.column('numberOfAnalystOpinions', anchor=CENTER, width=150, stretch=NO)
        framestat.column('targetLowPrice', anchor=CENTER, width=100, stretch=NO)
        framestat.column('targetMedianPrice', anchor=CENTER, width=100, stretch=NO)
        framestat.column('targetHighPrice', anchor=CENTER, width=100, stretch=NO)
        framestat.column('forwardEps', anchor=CENTER, width=100, stretch=NO)
        framestat.column('priceToBook', anchor=CENTER, width=100, stretch=NO)
        framestat.column('beta', anchor=CENTER, width=80, stretch=NO)
        framestat.column('averageDailyVolume10Day', anchor=CENTER, width=150, stretch=NO)
        
        framestat.heading('#0', text='')
        framestat.heading('shortName', text='Name', anchor=W)
        framestat.heading('country', text='Country', anchor=W)
        framestat.heading('industry', text='Industry', anchor=W)
        framestat.heading('recommendationKey', text='Recommendation', anchor=CENTER)
        framestat.heading('numberOfAnalystOpinions', text='NumberOfAnalystOpinions', anchor=CENTER)
        framestat.heading('targetLowPrice', text='TargetLowPrice', anchor=CENTER)
        framestat.heading('targetMedianPrice', text='TargetMedianPrice', anchor=CENTER)
        framestat.heading('targetHighPrice', text='TargetHighPrice', anchor=CENTER)
        framestat.heading('forwardEps', text='ForwardEps', anchor=CENTER)
        framestat.heading('priceToBook', text='PriceToBook', anchor=CENTER)
        framestat.heading('beta', text='Beta', anchor=CENTER)
        framestat.heading('averageDailyVolume10Day', text='AverageDailyVolume10Day', anchor=CENTER)

        disp_business_sum = tk.Text(
                        self,
                        font=LARGE_FONT, wrap='word'
                        )
        # disp_business_sum.pack(fill=tk.BOTH, expand=True)


        button3 = ttk.Button(self, text='Apply', width=8, command=Get_stock_stats)
        button3.pack()

class LiveTranscript(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Live Transcript', font=V_LARGE_FONT)
        label.pack(pady=10, padx=10)

        # todays_transcript, t_1_transcript, t_2_transcript, t_3_transcript, past4days = Get_transcript()
        # past4days.to_pickle('past4days.pkl')
        # past4days = pd.read_pickle('past4days.pkl')
        tickerspast4days = list(past4days['Ticker'])

        button1 = ttk.Button(self, text='Back to Welcome Page', width=18, command=lambda: controller.show_frame(HomePage))
        button1.pack()

        tickerinfo = AutocompleteCombobox(self,  
                                    width=30, 
                                    font=LARGE_FONT,
                                    completevalues=tickerspast4days
                                    )
        tickerinfo.pack()

        disp_tf = tk.Text(
                        self,
                        font=NORM_FONT, wrap='word', height=30
                        )
        disp_tf.pack(fill=tk.BOTH)

        label2 = ttk.Label(self, text='Model 90days prediction', font=LARGE_FONT)
        label2.pack()

        disp_pred = tk.Text(
                        self,
                        font=V_LARGE_FONT,
                        height=1,
                        width=7,
                        )
        disp_pred.pack()

        label3 = ttk.Label(self, text='Negative if returns < -6.8%\nNeutral if -6.8% < returns < 12.55%\nPositive if returns > 12.55%', font=LARGE_FONT)
        label3.pack()

        model_90days_quantile_no_mkt = pickle.load(open('90days_quantile_no_mkt', 'rb'))

        #load_model_model_8_mkt_quantile = pickle.load(open('model_8_mkt_quantile_score.sav', 'rb'))

        def get_analysis():
            #Getting transcript and displaying it
            disp_tf.delete('1.0', END)
            tickerstr = tickerinfo.get()
            #We select the required transcript and get prepared comment and Q&A
            transcriptarray = past4days[past4days['Ticker'] == tickerstr].values[0][5:7]
            #Convert it to a displayable format
            transcriptlist = ['PREPARED COMMENTS'] + transcriptarray[0]+ ['QUESTION AND ANSWERS'] + transcriptarray[1]
            transcriptdisplayed = '\n\n'.join(transcriptlist)
            #Insert it in the widget
            disp_tf.insert('1.0', transcriptdisplayed)

            #Getting predicition and displaying it
            disp_pred.delete('1.0', END)

            clean_transcript = past4days[past4days['Ticker'] == tickerstr]['Cleaned Prepared comments']
            invest_suggestion = model_90days_quantile_no_mkt.predict(clean_transcript)[0]

            if invest_suggestion == -1:
                invest_suggestion  = 'Negative'
                
            elif invest_suggestion == 0:
                invest_suggestion  = 'Neutral'

            else:
                invest_suggestion = 'Positive'

            disp_pred.insert('1.0', invest_suggestion)   
            disp_pred.update()         

        button2 = ttk.Button(self, text='Get Transcript', width=18, command=get_analysis)
        button2.place(relx=0.05, rely=0.72)

app = EarningDrift()
app.geometry('1400x850')
app.mainloop()
