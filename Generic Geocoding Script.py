#Generic Geocoding Script
#Requires the GeoPy library and Python 2.7 to run.

#To test without having geopy installed comment out 'import geopy', 'from geopy.geocoders import Nominatim', and 'geolocator = Nominatim()' and all geocoding will fail.

#For editing csv files
import csv
import shutil
import geopy

#For geocoding
from geopy.geocoders import Nominatim
geolocator = Nominatim()

#Variables for hard coding. Comment out the three user input processing calls below these four methods to skip the command prompts.
inputFile = ""
inputHeaders = []
outputFile = ""

#Taking user input for seed file location.
def fileLocation():
        inputFile = str(raw_input("What is the location of your .csv formatted addresses?\nIt should be formated like this:\nC:\Temp\AuburnData_Clean.csv\n"))
        print "Is this the correct file location? " + str(inputFile)
        if userCheck() == False:
                fileLocation()
        else:
                return inputFile
        
#Taking user input for formating of column headers.     
def headersFormat():
        inputHeaders = str(raw_input("What are the column headers in your .csv file?\nPlease enter you response in the following format:\nAddress, ... Latitude, Longitude\n"))
        inputHeaders = inputHeaders.split(",")
        print "Are these the correct column headers? " + str(inputHeaders).strip('[]')
        if userCheck() == False:
                headersFormat()
        else:
                return inputHeaders

#Taking user input for the location of the addresses in the CSV.
def addressColumn():
        inputColumn = int(raw_input("Which column are the addresses located in your .csv file?\nPlease enter you response as an integer.\n"))
        print "Is this the correct column number for the location of the addresses? " + str(inputColumn)
        if userCheck() == False:
                addressColumn()
        else:
                return inputColumn

#Taking user input for output file name and location.
def outputLocation():
        outputFile = str(raw_input("Where do you want your output file to be placed and what do you want it named?\nPlease format your response like this:\nC:\Temp\AuburnData_Clean_geocoded.csv\n"))
        print "Is this the correct file location? " + str(outputFile)
        if userCheck() == False:
                outputLocation()
        else:
                return outputFile
        
#Having users verify their inputs.      
def userCheck():
        verifyFile = str(raw_input("Yes or No? "))
        valid = ['Yes', 'yes', 'y', 'Y', 'True', 'true', 'yse', 'Yse', 'YES']
        if verifyFile in valid:
                print "Information verified by user."
        else:
                return False

#For attempting to fix addresses that failed to geocode.
def fixIt(address):

        #Working varibles.
        isAddressFixed = False
        fixedAddress = ' '
        thisAddress = address
        print thisAddress

        #Checking for blanks
        if thisAddress == '':
                return isAddressFixed
        
        #Actual fixing.
        thisAddress = thisAddress.strip()
        thisAddress = thisAddress.upper()
        print thisAddress
        #Removing special characters that do not occur in US addresses.
        thisAddress = thisAddress.replace("~", "")
        thisAddress = thisAddress.replace("`", "")
        thisAddress = thisAddress.replace("!", "")
        thisAddress = thisAddress.replace("@", "")
        thisAddress = thisAddress.replace("#", "")
        thisAddress = thisAddress.replace("$", "")
        thisAddress = thisAddress.replace("%", "")
        thisAddress = thisAddress.replace("^", "")
        thisAddress = thisAddress.replace("&", "")
        thisAddress = thisAddress.replace("*", "")
        thisAddress = thisAddress.replace("(", "")
        thisAddress = thisAddress.replace(")", "")
        thisAddress = thisAddress.replace("_", "")
        #"-" is purposely missing from this list.
        thisAddress = thisAddress.replace("+", "")
        thisAddress = thisAddress.replace("=", "")
        thisAddress = thisAddress.replace("[", "")
        thisAddress = thisAddress.replace("]", "")
        thisAddress = thisAddress.replace("{", "")
        thisAddress = thisAddress.replace("}", "")
        thisAddress = thisAddress.replace("", "")#\
        thisAddress = thisAddress.replace("|", "")
        thisAddress = thisAddress.replace(":", "")
        thisAddress = thisAddress.replace(";", "")
        thisAddress = thisAddress.replace("'", "")
        thisAddress = thisAddress.replace(",", "")
        thisAddress = thisAddress.replace("<", "")
        thisAddress = thisAddress.replace(".", "")
        thisAddress = thisAddress.replace(">", "")
        thisAddress = thisAddress.replace("?", "")                                  
        thisAddress = thisAddress.replace("/", "")
        thisAddress = thisAddress.replace("=", "")
        print thisAddress
        #Breaking the string down.
        thisAddress = thisAddress.split(' ')
        for word in thisAddress:
                word = word.strip()

        if len(thisAddress) > 2:
                if type(thisAddress[1]) == 'int':
                        if thisAddress[1][-1] == 1:
                                thisAddress[1] = thisAddress[1] + "ST"
                        elif thisAddress[1][-1] == 2:
                                thisAddress[1] = thisAddress[1] + "ND"
                        elif thisAddress[1][-1] == 3:
                                thisAddress[1] = thisAddress[1] + "RD"
                        else:
                                thisAddress[1] = thisAddress[1] + "TH"
                elif type(thisAddress[2]) == 'int':
                        if thisAddress[1][-1] == 1:
                                thisAddress[1] = thisAddress[1] + "ST"
                        elif thisAddress[1][-1] == 2:
                                thisAddress[1] = thisAddress[1] + "ND"
                        elif thisAddress[1][-1] == 3:
                                thisAddress[1] = thisAddress[1] + "RD"
                        else:
                                thisAddress[1] = thisAddress[1] + "TH"
        #Fixing street type.
        for word in thisAddress:
                if word == "ST" or "STR" or "STRE" or "STREE" or "STRT" or "STREET":
                        word = "ST"
                elif word == "WAY" or "WY":
                        word = "WAY"
                elif word == "AVE" or "AV" or "AVEN" or "AVENU" or "AVENUE" or "AVN" or "AVNUE" or "AVENUE":
                        word = "AVE"
                elif word == "PL" or "PLACE":
                        word = "PL"
                elif word == "RD" or "ROAD" or "RAD" or "ROD" or "RAOD":
                        word = "RD"
                elif word == "BLVD" or "BOULEVARD" or "BOUL" or "BOULV":
                        word = "BOULEVARD"
                elif word == "DRIVE" or "DR":
                        word = "DR"
                elif word == "HWY" or "HIGHWAY" or "HWAY" :
                        word = "HWY"
                        
        #Putting things back where we found them.
        fixedAddress = fixedAddress.join(thisAddress)
        print fixedAddress
                  
        if fixedAddress != address:
                isAddressFixed == True
                  
        return isAddressFixed

#User input processing calls. Comment out these method calls to skip user input.                
inputFile = fileLocation()
inputHeaders = headersFormat()
addressColumn = addressColumn()
outputFile = outputLocation()
fixedAddress = ''

#For trouble shooting.
print "\ninputFile = " + str(inputFile) + "\ninputHeaders = " + str(inputHeaders) + "\noutputFile = " + str(outputFile) + "\n\n*****Begin Processing*****\n"    

#Where the geocoding is done.
def actualGeocoding():

        #Blank list for holding addresses.
        addresses = []

        #Filling list with addresses from input file.
        with open (inputFile) as csvFile:
                csv_data = csv.reader(csvFile)
                for row in csv_data:
                        addresses.append(row[addressColumn])

        #Reporting the number of addresses to the user.
        totalAddresses = str(len(addresses))
        print "Processing " + totalAddresses + " rows in file.\n" + str(float(totalAddresses)/float(60)/float(60)) + " hours remaining before processing is complete.\n" +  str(float(totalAddresses)/float(60)) + " minutes remaining before processing is complete.\n"
        rowsPassed = 0
        rowsSkipped = 0
        rowsFailed = 0

        #Varibles for organizing geocoding results.
        latitude = []
        longitude = []
        a = 1

        #Loop for geociding addresses and storing the results includes error handling.
        oldValue = ""
        for value in addresses:
                try:
                        if value == oldValue:
                                latitude.append((location.latitude))
                                longitude.append((location.longitude))
                                print "Current row in input file SKIPPED: " + str(a) + " Processed row " + str(a) + " of " + totalAddresses + "."
                                rowsSkipped += 1
                                a+=1
                        else:
                                location = geolocator.geocode([value])
                                latitude.append((location.latitude))
                                longitude.append((location.longitude))
                                print "Current row in input file PASSED: " + str(a) + " Processed row " + str(a) + " of " + totalAddresses + "."
                                oldValue = value
                                rowsPassed += 1
                                a+=1
                except:
                        if fixIt(value):
                                location = geolocator.geocode([fixedAddress])
                                latitude.append((location.latitude))
                                longitude.append((location.longitude))
                                print "Current row in input file PASSED: " + str(a) + " Processed row " + str(a) + " of " + totalAddresses + "."
                                oldValue = value
                                rowsPassed += 1
                                a+=1
                        else:
                                latitude.append((" "))
                                longitude.append((" "))
                                print "Current row in input file FAILED: " + str(a) + " Processed row " + str(a) + " of " + totalAddresses + "."
                                rowsFailed += 1
                                a+=1

        #Open the original csv and grab all the data, place it in a var called data, and close the file again.                
        f = open(inputFile)
        data = [item for item in csv.reader(f)]
        f.close()

        #Create a blank arraycalled new_data
        new_data = []               

        #For each item in data append a location, then add the complete item to the new data variable
        for i, item in enumerate(data):
                try:
                        item.append(latitude[i])
                        item.append(longitude[i])
                        new_data.append(item)
                except:
                        item.append(" ")
                        new_data.append(item)
                         
        #Open the new csv and write the header row followed by a row for each object in the new_data array      
        f = open(outputFile, 'w')
        csv.writer(f, lineterminator='\n').writerow(inputHeaders)
        csv.writer(f, lineterminator='\n').writerows(new_data)
        f.close()

        #End processing message.
        print "\n*****Processing Complete*****\n\n" + str(rowsPassed) + " out of " + totalAddresses + " rows were successfully geocoded.\n" + str(rowsSkipped) + " out of " + totalAddresses + " were duplicates and geocoded successfully.\n" + str(rowsFailed) + " out of " + totalAddresses + " rows failed to geocode successfully.\n" + str(100 * (float(rowsPassed)+float(rowsSkipped))/float(totalAddresses)) + "% of total addresses successfully geocoded."

#Geoprocessing call.
actualGeocoding()
