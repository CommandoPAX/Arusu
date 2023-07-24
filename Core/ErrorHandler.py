#Handler responsible for logging errors
import datetime

#Should only work on Linux based system for now
    
def LogError(CogName : str, CogFunct : str, Error : Exception) : #Function that will handle logging all errors
    try :
        filename = str(datetime.date.today()) + ".log"
        ErrMsg = str(datetime.datetime.now()) + " " + f"{CogName} | {CogFunct} : " + str(Error) + '\n' # \n not working, the fuck
        f = open("Logs/" + filename, "a+")
        f.write(ErrMsg)
        f.close()
    except Exception as e :
        print('--------------------------------------------------------------------------')
        print("Could not log error nor error in Error Handler, fix needed ASAP")
        print(e)
        print('--------------------------------------------------------------------------')