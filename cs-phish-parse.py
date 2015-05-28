#!/usr/bin/python

import csv
import argparse

#checks for args
parser = argparse.ArgumentParser(description='This script will parse multiple Cobalt Strike Phishing campaigns. Inputs need to be TSV files exported by Cobalt Strike.')
parser.add_argument('-w', '--weblog', help='Weblog TSV file',required=True)
parser.add_argument('-s','--spearphishes', help='Spearphishes TSV file', required=True)
args = parser.parse_args()

#spearfishes list variables
keysSpearfishes=['_to','_to_name','_server','_status','_time','_token','_template','_subject','_url','_attachment']
listSpearfishes=[]

#weblog list variables
keysWeblog=['_host','_created_at','_method','_uri','_response','_size','_handler','_user_agent','_token_wl','_primary']
listWeblog=[]

#parse spearphises file into dict-list
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
            if tmpdict["_token"] in tokensTot:
                totClicks+=1
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

#derive needed variables from lists
subjectList = getUniqueList(listSpearfishes,"_subject")
tokensUniq = getUniqueList(listWeblog,"_token_wl")
tokensTot = getList(listWeblog,"_token_wl")
#show the goods
print "Number of campaigns: %i" % len(subjectList)
for subj in subjectList:
    totTargets, uniqClicks, totClicks= calcThings(subj)
    print "-" * 50
    print "Campaign '%s' " % subj
    print "-" * 50
    print "Total emails sent: %i" % totTargets
    print "Total unique targets: %i" % len(getUniqueListBySubj(listSpearfishes,"_to",subj))
    print "Unique targets who clicked: %i" % uniqClicks
    print "Unique click rate: %5.2f%%" % ((uniqClicks / float(len(getUniqueListBySubj(listSpearfishes,"_to",subj))))*100) 
    print "Total clicks: %i" % totClicks