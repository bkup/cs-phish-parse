#!/usr/bin/python

import csv
import sys

##This script is used to parse TSV files exported from Agressors's phishing module.  
##Re-written on 11/3/15 to support CS 3.0

#get file path to data
filepath = raw_input("Specifiy the data path: ")

#check for required files
try:
    with open(filepath + "/campaigns.tsv") as file:
        pass
except IOError as e:
    print "Unable to find campaigns.tsv"
    sys.exit()

try:
    with open(filepath + "/sentemails.tsv") as file:
        pass
except IOError as e:
    print "Unable to find sentemails.tsv"
    sys.exit()

try:
    with open(filepath + "/webhits.tsv") as file:
        pass
except IOError as e:
    print "Unable to find webhits.tsv"
    sys.exit()

try:
    with open(filepath + "/tokens.tsv") as file:
        pass
except IOError as e:
    print "Unable to find tokens.tsv"
    sys.exit()

#initialize lists
keysMaster = ['cid','subject','total_sent','total_id','unique_id']
listMaster=[]

listTokens=[]
listTokensUniq=[]

#gather number of campaigns 
with open(filepath + "/campaigns.tsv",'r') as f:
    #next(f) # skip headings
    reader = csv.DictReader(f,delimiter='\t')
    for row in reader:
        listMaster.append(dict(zip(keysMaster,(row['cid'], row['subject']))))

#intialize other keys
for x in listMaster:
    x["total_sent"] = 0 
    x["total_id"] = 0
    x["unique_id"] = 0

#get the total emails sent
count = 0
for x in listMaster: 
    with open(filepath + "/sentemails.tsv",'r') as f:
        reader = csv.DictReader(f,delimiter='\t')
        for row in reader:
            if x['cid'] == row['cid']:
                if "SUCCESS" in row['status']:
                    count += 1
    x['total_sent'] = count
    count = 0

#get list of tokens that clicked
with open(filepath + "/webhits.tsv",'r') as f:
    reader = csv.DictReader(f,delimiter='\t') 
    for row in reader:
        if row['token']: #check for nulls
            listTokens.append(row['token'])

#get unique list of tokens
listTokensUniq = set(listTokens)

#run through all tokens and compare to total and unique hit lists
countTot = 0
countUniq = 0
for x in listMaster:
    with open(filepath + "/tokens.tsv",'r') as f:
        reader = csv.DictReader(f,delimiter='\t')
        for row in reader:
            if x['cid'] == row['cid']:
                countTot += listTokens.count(row['token'])
                if row['token'] in listTokensUniq:
                    countUniq += 1
    x['total_id'] = countTot
    x['unique_id'] = countUniq
    countTot = 0
    countUniq = 0

#show the goods
print "-" * 50
print "Number of campaigns: %i" % len(listMaster)
for x in listMaster:
    print "-" * 50
    print "Campaign '%s' " % x['subject']
    print "-" * 50
    print "Total emails sent: %i" % x['total_sent']
    print "Unique targets who clicked: %i" % x['unique_id']
    print "Unique click rate: %5.2f%%" % ((x['unique_id'] / float(x['total_sent'])) * 100)
    print "Total clicks: %i" % x['total_id']