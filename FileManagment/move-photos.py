import os 
import re 
import platform
import datetime
import calendar
import shutil 


source = "F:\ANAS\My Work\Scripts\Screenshots"

target = "F:\ANAS\My Work\Scripts\FileManagment"

EXTS = ["jpg", "png", "jpeg", "mov", "mp4"]
DATE_PATTERN = ".*(20\d\d)-?([01]\d)-?([0123]\d).*"



files = os.listdir(source)

def get_folder(year, monthNumber):
    
    monthName = calendar.month_name[int(monthNumber)]
    
    return  f"{year}\{monthNumber} {monthName}"
    

def created_date(path_to_file):
    
    if platform.system() == 'windows':
        timestamp = os.path.getctime(path_to_file)
        
    else:
        
        stat = os.stat(path_to_file)
        
        try:
            timestamp = stat.st_birthtime
            
        except AttributeError:
            
            timestamp = stat.st_mtime
            
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        

def get_date(folder, file):
    
    match_obj = re.match(DATE_PATTERN, file)

    if (match_obj):
        year = match_obj[1]

        month = match_obj[2]

    else:
        
        DateCreated = created_date(f"{folder}/{file}")
        
        match_obj = re.match(DATE_PATTERN, DateCreated)
        
        if(match_obj):
        
            year = match_obj[1]

            month = match_obj[2]
        
        else:
            year = "0"
            
            month = "0"
            print(f"Unable to get date: {file}")
        
    return {"year": year, "month":month}

    
for file in files:
    if (file.lower().endswith(tuple(EXTS))):
        
        date = get_date(source, file)

        year = date["year"]
        month = date["month"]


        if (year == "0" or month == "0"):

            continue;

        folder = get_folder(year, month)

        target_folder = f"{target}\{folder}"

        if (not os.path.exists(target_folder)):

            os.makedirs(target_folder)

        source_file = f"{source}\{file}"

        target_file = f"{target_folder}\{file}"

        if (not os.path.exists(target_file)):

            shutil.move(source_file, target_file)


        elif (os.stat(source_file).st_size == os.stat(target_file).st_size):
            print(f"Duplicate file, deleting: {file}")

            os.remove(source_file)

        else:
            # Might want to rename and move here 
            print(f"Duplicated file, different size: {file}")
        
        
