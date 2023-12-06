import json
import xmltodict
import os
path = "datascience.stackexchange.com/"
files = [f for f in os.listdir(path)]
print("files --> ", files)

try: 
    os.makedirs("data/imgs/", exist_ok = True) 
except OSError as error: 
    print("directories alread exist") 
    
try: 
    os.makedirs("json/", exist_ok = True) 
except OSError as error: 
    print("directories alread exist") 

try: 
    os.makedirs("datascience.stackexchange.com/", exist_ok = True) 
except OSError as error: 
    print("directories alread exist") 
 
# open the input xml file and read
# data in form of python dictionary 
# using xmltodict module
for filename in files:
    with open("datascience.stackexchange.com/" + filename) as xml_file:
        
        data_dict = xmltodict.parse(xml_file.read())
        # xml_file.close()
        
        # generate the object using json.dumps() 
        # corresponding to json data
        
        json_data = json.dumps(data_dict)
        
        # Write the json data to output 
        # json file
        with open("json/" + os.path.splitext(filename)[0] + ".json", "w") as json_file:
            json_file.write(json_data)
            # json_file.close()