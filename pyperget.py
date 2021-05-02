import argparse
import sys
import re
import gzip
import os
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import wget
from urllib.request import urlopen
import urllib.request

# Function to check url validity
def check_validity(url):
    try:
        urllib.request.urlopen(url)
        print("Valid URL")
    except IOError:
        print ("Invalid URL")
        sys.exit()

# Download both txt and txt.gz files from pipermail webpage and return list of downloaded files
def get_files(url):
    links = []
    html = urlopen(url).read()
    html_page = bs(html, features="lxml") 
    files = []
    base = urlparse(url)   
    for link in html_page.find_all('a'):
        current_link = link.get('href')
        
        
        if current_link.endswith('txt.gz'):
            files.append(current_link)
            links.append(base.scheme + "://" + base.netloc + base.path  + current_link)
    
        elif current_link.endswith('txt'):
            files.append(current_link)
            links.append(base.scheme + "://" + base.netloc + base.path  + current_link)
    
    for link in links:
        try:    
            wget.download(link)
            print("\n" + link + "\n")
        except:
            print("\n Unable to download file, did you forget a trailing /?\n")
    files.reverse()
    
    return(files)

#Gunzip files if necessary and convert files to mbox
def mbox_conversion(files, output):
    output_name = output + '.mbox'
    #Extract files and concatenate into mbox format
    with open(output_name, 'w+') as outfile:
        for file in files:
            if file.endswith('.gz'):
                with gzip.open(file, 'rb') as f:
                    for line in f:
                        outfile.write(line.decode())
                os.remove(file)
            else:
                with open(file, 'rb') as f:
                    for line in f:
                        outfile.write(line.decode())
                os.remove(file)        
    
    
    with open(output_name, 'r') as outfile:              
        res = [re.sub(' at ', '@', i, flags=re.IGNORECASE)
            if 'from' in i[:4].lower() else i for i in outfile.readlines()]
    
    with open(output_name, 'w') as outfile:
        
        for line in res:
            outfile.write(line)
            
# Define arguments for script            
def pass_args():

    parser = argparse.ArgumentParser(description = "Download a pipermail archive and convert it to mbox") 
    parser.add_argument('-u', '--url', help = "Pipermail directory location. Example: http://hostname.tld/directory/. Don't forget the trailing /")
    parser.add_argument('-o', '--output', help = "Output file name (without.mbox)", default ='output')
    args = parser.parse_args()
    
    return(args)
        
   
# Set up arguments and provide help message
def main():
    args = pass_args()
    check_validity(args.url)
    mbox_conversion(get_files(args.url), args.output)

main()

