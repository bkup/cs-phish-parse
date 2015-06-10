#!/usr/bin/python

import csv
import argparse

##This script is used to parse TSV files exported from Cobalt Strike's phihsing module.  
##The spearfishes and weblog files are required.
##An optional exclude list can be used to remove certain email addresses from calculations

#checks for args
parser = argparse.ArgumentParser(description='This script will parse multiple Cobalt Strike Phishing campaigns. Inputs need to be TSV files exported by Cobalt Strike.')
parser.add_argument('-w', '--weblog', help='Weblog TSV file',required=True)
parser.add_argument('-s','--spearphishes', help='Spearphishes TSV file', required=True)
parser.add_argument('-e','--exclude', help='Exclude address file; one per line', required=False)
args = parser.parse_args()

#Each line in the TSV gets made into a dictionary item and added to the overall list
#spearfishes list variables
keysSpearfishes=['_to','_to_name','_server','_status','_time','_token','_template','_subject','_url','_attachment']
listSpearfishes=[]

#weblog list variables
keysWeblog=['_host','_created_at','_method','_uri','_response','_size','_handler','_user_agent','_token_wl','_primary']
listWeblog=[]

#parse spearphishes file into dict-list
with open(args.spearphishes,'r') as f:
    next(f) # skip headings
    reader=csv.reader(f,delimiter='\t')
    for to,to_name,server,status,time,token,template,subject,url,attachment in reader:
        tmp=[to,to_name,server,status,time,token,template,subject,url,attachment]
        listSpearfishes.append(dict(zip(keysSpearfishes,tmp)))

#parse weblog file into dict-list
with open(args.weblog,'r') as f:
    next(f) # skip headings
    reader=csv.reader(f,delimiter='\t')
    for host,created_at,method,uri,response,size,handler,user_agent,token_wl,primary in reader:
        tmp=[host,created_at,method,uri,response,size,handler,user_agent,token_wl,primary]
        listWeblog.append(dict(zip(keysWeblog,tmp)))

#read in exclude list if it exists
if args.exclude:
    with open(args.exclude,'r') as f:
        excludeList = [word.strip() for word in f] #strip the new line /n 
    #remove excludes
    tmptok=[]
    for dictx in listSpearfishes:
        if dictx["_to"] in excludeList:
            tmptok.append(dictx["_to"])
            listSpearfishes.remove(dictx)
    

def calcThings(subj):
    totTargets=0
    uniqClicks=0
    totClicks=0
    #iterate through whole list
    for tmpdict in listSpearfishes:
        if tmpdict["_subject"] == subj:
            totTargets+=1
            if tmpdict["_token"] in tokensUniq:
                uniqClicks+=1
                totClicks+=tokensTot.count(tmpdict["_token"])

    return totTargets,uniqClicks,totClicks

def getUniqueList(listy,dictvalue):
    tmpList=[]
    for x in listy:
        tmpList.append(x[dictvalue])
    return filter(None,sorted(list(set(tmpList))))

def getList(listy,dictvalue):
    tmpList=[]
    for x in listy:
        tmpList.append(x[dictvalue])
    return filter(None,sorted(list(tmpList)))

#only works for listSpearfishes
def getUniqueListBySubj(listy,dictvalue,subj):
    tmpList=[]
    for x in listy:
        if x["_subject"] == subj:
            tmpList.append(x[dictvalue])
    return filter(None,sorted(list(set(tmpList))))

#######################################

#derive needed values from lists
subjectList = getUniqueList(listSpearfishes,"_subject")
tokensUniq = getUniqueList(listWeblog,"_token_wl")
tokensTot = getList(listWeblog,"_token_wl")
targetsTot = getUniqueList(listSpearfishes,"_to")
#show the goods
print "-" * 50
print "Number of campaigns: %i" % len(subjectList)
print "Overall unique click rate: %5.2f%%" % (len(tokensUniq) / float(len(targetsTot))*100)
for subj in subjectList:
    totTargets, uniqClicks, totClicks = calcThings(subj)
    print "-" * 50
    print "Campaign '%s' " % subj
    print "-" * 50
    print "Total emails sent: %i" % totTargets
    print "Total unique targets: %i" % len(getUniqueListBySubj(listSpearfishes,"_to",subj))
    print "Unique targets who clicked: %i" % uniqClicks
    print "Unique click rate: %5.2f%%" % ((uniqClicks / float(len(getUniqueListBySubj(listSpearfishes,"_to",subj))))*100) 
    print "Total clicks: %i" % totClicks


