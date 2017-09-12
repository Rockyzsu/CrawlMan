# coding: utf-8

def getheader():
    with open('request_header') as fp:
        data=fp.readlines()
    dictionary=dict()
    for line in data:
        line=line.strip()
        dictionary[line.split(":")[0]]=':'.join(line.split(":")[1:])
    return dictionary
if __name__=="__main__":
    print getheader()