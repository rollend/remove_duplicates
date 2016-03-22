# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:25:57 2016

@author: Shen.Xu

This script use dict key to find duplicate contents within csv file, 
create a new file to store non-duplicate contents (no infect on contents order and file name). 
Folders are created according to parsed folder structure, root file path added suffix of cleaned.
Usage: Put the py file in the root folder you wish to clean then run the file. 
Approximate run time:  5.0GB about 4 mintues
Reminder: Leave enough spaces, log file stored in new root folder 
"""
import os
import pickle
import functools
#import tkinter
#import tkinter.filedialog
#import getpass
#from tkinter.filedialog  import askdirectory   
import inspect
import timeit

yourpath=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory


#Get directory size
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

#Map directory structure by walk through, return nested dict for create new folders and list of files to find location of file 
def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    list_of_files={}
    i=0
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = functools.reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
        for file in files:
            if file.endswith(".csv"):
                #results += '%s\n' % os.path.join(path, file)
                list_of_files[i] = os.path.join(path, file)
                i=i+1   
    #with open(yourpath+'/allfilename.p', 'wb') as handle:
      #pickle.dump(dir, handle)
    return dir, list_of_files

#Fuction to remove all none value keys in order to have a clean directory structure
def remove_keys_with_none_values(item):
    if not hasattr(item, 'items'):
        return item
    else:
        return {key: remove_keys_with_none_values(value) for key, value in item.items() if value is not None}

#Recursive create the folders using nested dict (directory tree)
def create_folders(directory, current_path):        
    if len(directory):
        for direc in directory:
            create_folders(directory[direc], os.path.join(current_path, direc))
    else:
        os.makedirs(current_path)

#Actual code read each file, retain non duplicate contents then store in a new file
def remove_duplicates(rootdir):
    dir, input_file = get_directory_structure(rootdir)
    logname = yourpath+"_cleaned"+'/duplicated.log' 
    results=str()
    num=[]
    num_total=[]
    total=0
    total_instances=0
    for line in input_file:
        rFile = open(input_file[line], "r")
        wFile = open(yourpath+"_cleaned"+rFile.name.replace(yourpath,''), "w")
        allLine = rFile.readlines()
        rFile.close()
        h = {}
        for i in allLine:
            if i not in h:
                h[i]=1
                wFile.write(i)
        results += '%s\n' % (os.path.dirname(input_file[line])+","+os.path.basename(input_file[line])+","+str(len(allLine))+","+str(len(allLine)-len(h)))
        num.append(len(allLine)-len(h))
        num_total.append(len(allLine))
        print(input_file[line]+","+str(len(allLine))+","+str(len(allLine)-len(h)))
        wFile.close()
        #os.remove(input_file[line])
    with open(logname, 'w') as logfile:
        logfile.write(results)
    for value in num:
        total += value
    for value in num_total:
        total_instances +=value
    print("Total files checked:"+str(len(input_file))+"\n" \
    "Total instance checked:"+str(total_instances)+"\n" \
    "Total instances removed:"+str(total))
    

#Convert size of folder into human readable format
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


if __name__ == '__main__':
    start = timeit.default_timer()
    newpath = yourpath+"_cleaned"    
    #create new folder with suffix    
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    dir, input_file = get_directory_structure(yourpath)
    list_of_folders= remove_keys_with_none_values(dir)
    list_of_folders[yourpath+"_cleaned"]=list_of_folders.pop(os.path.basename(yourpath))
    create_folders(list_of_folders,'')    
    remove_duplicates(yourpath)
    print("From File Size:"+str(sizeof_fmt(get_size(yourpath)))+"\n" \
    "To File Size:"+str(sizeof_fmt(get_size(yourpath+"_cleaned")))+"\n"\
    "Total reduced:"+str(sizeof_fmt(get_size(yourpath)-get_size(yourpath+"_cleaned")))+"\n"\
    "Job Done")
    stop = timeit.default_timer()
    print("Total time spent:"+str(stop-start)+"sec")
          
    


    
