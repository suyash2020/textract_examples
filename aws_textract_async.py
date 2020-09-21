# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 23:30:51 2020

@author: suyash
"""

import boto3
import time
from textract_parser.src_python import trp

#def getJobResults(jobId):
s3bucketName = "007bucket21"
documentName = "sample_BPO.pdf"


def startJob(s3bucketName,objectName):
    response = None
    client = boto3.client("textract",
                          region_name = "eu-west-1")
    
    response = client.start_document_text_detection(
                            DocumentLocation = 
                            {
                                "S3Object":
                                    {
                                     "Bucket":s3bucketName,
                                     "Name":objectName
                                    }
                            }
                                                    )
    return response["JobId"]

def isJobComplete(jobId):
    time.sleep(5)
    client = boto3.client("textract",region_name = "eu-west-1")
    response = client.get_document_text_detection(JobId = jobId)
    status = response['JobStatus']
    print("Job status: {}".format(status))
    
    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_text_detection(JobId = jobId)
        status = response["JobStatus"]
        print("Job Status {}".format(status))
    return status

def getJobResults(jobId):
    pages = []
    time.sleep(5)
    client = boto3.client("textract",region_name = "eu-west-1")
    response = client.get_document_text_detection(JobId = jobId)
    
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if("NextToken" in response):
        nextToken = response["NextToken"]
    
    while(nextToken):
        time.sleep(5)
        response = client.get_document_text_detection(JobId = jobId,
                                                      NextToken = nextToken)
    return response



        
jobId = startJob(s3bucketName, documentName)
print("Started job with id: {}".format(jobId)) 

if(isJobComplete(jobId)):
    response = getJobResults(jobId)


doc = trp.Document(response)

# iterate over the elements of the document
for page in doc.pages:
    # Print lines and words 
    for line in page.lines:
        print("Line: {}--{}".format(line.text, line.confidence))
        for word in line.words:
            print("Word: {}--{}".format(word.text, word.confidence))
    
    for table in page.tables:
        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                print("Table[{}][{}] = {}-{}".format(r, c, cell.text, cell.confidence))


    
# print detected text
for resultPage in response:
    for item in resultPage["Blocks"]:
        if item["BlockType"]=="Line":
            print("\n033[94m"+item["Text"]+"\033[0m")
        