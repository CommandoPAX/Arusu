#Handler responsible for logging errors
import datetime
import time

#Should only work on Linux based system for now
    
def LogError(Cogname : str, CogFunct : str, Error : Exception) : #Function that will handle logging all errors
    try :
        filename = str(datetime.date.today()) + ".txt"
        #We create a file using the format Date_Time_txt
        try :
            with open("Logs/" + filename, "a") as file :
                file.write(str(Error)) #We log the error in the file
        except :
            with open("Logs/" + filename, "w") as file :
                file.write(str(Error)) #We log the error in the file
    except Exception as e :
        #If we get an error we try to log it
        try : 
            filename = str(datetime.date.today()) + "_" + str(time.localtime()) + "_" + "ErrorHandler" + ".txt"
            with open("Logs/" + filename, "a") as file :
                file.write(e) #We log the error in the file
        except Exception as e2 :
            print('--------------------------------------------------------------------------')
            print("Could not log error nor error in Error Handler, fix needed ASAP")
            print(e)
            print('--------------------------------------------------------------------------')