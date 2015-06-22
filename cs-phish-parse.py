#!/usr/bin/python

import csv
import argparse

##This script is used to parse TSV files exported from Cobalt Strike's phishing module.  
##The spearfishes and weblog files are required.
##An optional exclude list can be used to remove certain email addresses from calculations

#checks for args
parser = argparse.ArgumentParser(description='This script will parse multiple Cobalt Strike Phishing campaigns. Inputs need to be TSV files exported by Cobalt Strike.')
parser.add_argument('-w', '--weblog', help='Weblog TSV file',required=True)
parser.add_argument('-s','--spearphishes', help='Spearphishes TSV file', required=True)
parser.add_argument('-e','--excludeaddress', help='Exclude address file; one per line', required=False)
parser.add_argument('-x','--excludesubject', help='Exclude subject file; one per line', required=False)
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

    
####
#Functions
####
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

#gets a column in the TSV file
def getList(listy,dictvalue):
    tmpList=[]
    for x in listy:
        tmpList.append(x[dictvalue])
    return filter(None,sorted(list(tmpList)))

#like get list but with a condition for the values
def getUniqueListByKey(listy,key,dictvalue,keyvalue):
    tmpList=[]
    for x in listy:
        if x[key] == keyvalue:
            tmpList.append(x[dictvalue])
    return filter(None,sorted(list(set(tmpList))))

#removes rows from TSV file
def removeDictFromList(listy,key,value):
    index=0
    while index<len(listy):
        dictx=listy[index]
        if dictx[key] == value:
            listy.remove(dictx)
        else:
            index+=1

#######################################
#Main
#######################################

#excluding things
if args.excludeaddress:
    with open(args.excludeaddress,'r') as f:
        excludeList = [word.strip() for word in f] #strip the new line /n 
    #remove excluded emails
    #remove lines in listspearphises that contain the exlcude subject
    for x in excludeList:
        #first get tokens that will be exluded so they can be removed from listWeblog
        excludetokens = getUniqueListByKey(listSpearfishes,"_to","_token",x)
        #remove lines containing excluded subjects
        removeDictFromList(listSpearfishes,"_to",x)
        #remove the tokens from weblog associated with those emails 
        for y in excludetokens:
            removeDictFromList(listWeblog,"_token_wl",y)

if args.excludesubject:
    with open(args.excludesubject,'r') as f:
        excludeList = [word.strip() for word in f] #strip the new line /n 
    #remove lines in listspearphises that contain the exlcude subject
    for x in excludeList:
        #first get tokens that will be exluded so they can be removed from listWeblog
        excludetokens = getUniqueListByKey(listSpearfishes,"_subject","_token",x)
        #remove lines containing excluded subjects
        removeDictFromList(listSpearfishes,"_subject",x)
        #remove the tokens from weblog associated with those subjects
        for y in excludetokens:
            removeDictFromList(listWeblog,"_token_wl",y)

    

#derive needed values from lists
#set gives unique list
subjectList = set(getList(listSpearfishes,"_subject"))
tokensUniq = set(getList(listWeblog,"_token_wl"))
tokensTot = getList(listWeblog,"_token_wl")
targetsTot = set(getList(listSpearfishes,"_to"))
#show the goods
print len(tokensUniq)
print len(targetsTot)
print "-" * 50
print "Number of campaigns: %i" % len(subjectList)
print "Overall unique click rate: %5.2f%%" % (len(tokensUniq) / float(len(targetsTot))*100)
for subj in subjectList:
    totTargets, uniqClicks, totClicks = calcThings(subj)
    print "-" * 50
    print "Campaign '%s' " % subj
    print "-" * 50
    print "Total emails sent: %i" % totTargets
    print "Total unique targets: %i" % len(getUniqueListByKey(listSpearfishes,"_subject","_to",subj))
    print "Unique targets who clicked: %i" % uniqClicks
    print "Unique click rate: %5.2f%%" % ((uniqClicks / float(len(getUniqueListByKey(listSpearfishes,"_subject","_to",subj))))*100) 
    print "Total clicks: %i" % totClicks


