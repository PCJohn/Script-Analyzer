'''
This module handles the script files management. It has methods to scrape the scripts off www.imsdb.com and load saved scripts
 
Author: Prithvijit Chakrabarty (prithvichakra@gmail.com)
'''

from bs4 import BeautifulSoup as bs44
from bs4 import BeautifulSoup as bs
import urllib2
import os
import nltk
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
import random

DESC_TAG = 'DESCRIPTION'

#Method to download all scripts from all genres hosted at www.imsdb.com
#This is quite crude and specific to parsing the imsdb format
def get_scripts():
    save_to = 'C:\\School\\My Work\\Computer\\Datasets\\cornell_movie_dialogs_corpus\\Scripts2\\'
    script_list = urllib2.urlopen('http://www.imsdb.com/all%20scripts/')
    soup = bs.BeautifulSoup(script_list)
    count = 0
    lost = []
    for link in soup.findAll('a'):
        url = link.get('href')
        if url.startswith('/Movie Scripts/'):
            name = (url.split('/')[2])[:-11].strip()
            name = name.replace(':','')
            name = name.replace('?','')
            file_name = name
            name = '-'.join([n.strip() for n in name.split(' ')])
            print '--',name
            try:
                html = urllib2.urlopen('http://www.imsdb.com/scripts/'+name+'.html').read()
                sp = bs44(html,"html.parser")
                text = sp.get_text()
                
                lines = [''.join([i if ord(i)<128 else ' ' for i in line]) for line in text.splitlines()]
                filtered = []
                started = False
                for line in lines:
                    if line.upper().strip() == 'ALL SCRIPTS':
                        started = True
                    elif line.startswith('Writers : '):
                        started = False
                    if started == True:
                        filtered.append(line)

                script = '\n'.join(filtered)
                print file_name
                with open(save_to+file_name+'.txt','a') as sc_file:
                    sc_file.write(script)
            except urllib2.HTTPError:
                count = count+1
                lost.append(file_name)
    print lost

#Method to load script(s). Returns a list of tuples: (movie name,lines of script)
#Setting count = N will return N random scripts
#Specifiying a name will load only that script
def load_scripts(path,count=None,name=None):
    scripts = []
    if not name is None:
        return [(name,open(path+name).readlines())]
    files = os.listdir(path)
    if count is None:
        count = len(files)
    else:
        random.shuffle(files)
    for sc_file in files[:count]:
        scripts.append((sc_file,open(path+sc_file).readlines()))
    return scripts

#Auxiliary method to remove all non-ASCII characters in text - cleans unknown characters
def clean(text):
    return ''.join([c if ord(c)<128 else '' for c in text])
