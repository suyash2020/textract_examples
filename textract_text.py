# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:08:35 2020
@author: suyash
"""
#Detects text in a document stored in an S3 bucket.
import boto3
from textract_parser.src_python import trp

s3BucketName = '007bucket21'
documentName = "sample_BPO0.jpg"

textract = boto3.client(service_name = "textract",
                        region_name = "eu-west-1")

response = textract.analyze_document(Document=
                                         {'S3Object':
                                          {'Bucket':s3BucketName,
                                           'Name':documentName
                                           }
                                          },
                                        FeatureTypes=["TABLES","FORMS"] )

print("\nTEXT\n==========")
text = ""
for item in response["Blocks"]:
    if item["BlockType"]=="LINE":
        print('\033[94'+item["Text"]+'\033[0m')
        text = text+ " "+item["Text"]    


# using textract parser library
doc = trp.Document(response)

# iterate over the elements of the document
for page in doc.pages:
    # Print lines and words 
    for line in page.lines:
        print("Line: {}--{}".format(line.text, line.confidence))
        for word in line.words:
            print("Word: {}--{}".format(word.text, word.confidence))
 
# Print tables

    for table in page.tables:
        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                print("Table[{}][{}] = {}-{}".format(r, c, cell.text, 
                                                     cell.confidence))


# Print fields
    for field in page.form.fields:
        print("Field: Key: {}, Value: {}".format(field.key.text, field.value.text))


# Search fields by key
    key = "subject"
    fields = page.form.searchFieldsByKey(key)
    for field in fields:
        print("Field: Key: {}, Value: {}".format(field.key, field.value))

    # Get field by key
    key = "subject:"
    field = page.form.getFieldByKey(key)
    if(field):
        print("Field: Key: {}, Value: {}".format(field.key, field.value))
