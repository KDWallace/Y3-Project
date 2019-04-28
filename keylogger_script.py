#Keylogger program       Kiran Wallace 20.11.2018
#
#Program designed to keylog preset strings into GNUplot
#It will enter data based off the file names found in the fileNames list
#and fit a guassian and lorentzian plot to the data set.
#The program also allows for the user to modify the
#tilt and flat of background (a1,b1)


from pynput.keyboard import Key, Controller
import pyautogui as gui
from time import sleep

#function for keylogging into the console
def Msg(Message):
    key = Controller()
    sleep(0.1)
    key.type(Message)
    key.press(Key.enter)
    key.release(Key.enter)

#function for changing the background variables of a1 and b1
def changeBackground(bell,item,height,centre,width,mX,mY,pmX,pmY):
    #creates change string variable
    change = ""
    
    #loops until change is set to "no" or "n"
    #This is not case sensitive
    while change.lower() != "no" and change.lower() != "n":

        #sets the location of the mouse and clicks
        gui.click(pmX,pmY)
        #allows the user to input "yes/y" or "no/n" for the change variable
        change = input("\nDo you wish to change the background values a1,b1 (yes/no): ")

        #if the user inputs "yes"/"y", the user will be able to change the tilt (a) and background (b) variables of the curve
        if change.lower() == "yes" or change.lower() == "y":

            #initialisers
            varValues = ""
            includeVals = ""
            eqStart = ""

            #input variables
            a1 = input("\na1 = ")
            b1 = input("b1 = ")
            sleep(0.5)

            #only includes the (a) variable if it is not equal to 0
            if a1 != "0":
                varValues = "a1 = " + a1 + "; "
                includeVals = "a1,"
                eqStart = "a1*x + "

            #only includes the (b) variable if it is not equal to 0
            if b1 != "0":
                varValues += "b1 = " + b1 + "; "
                includeVals += "b1,"
                eqStart += "b1 + "

            #will add all other variables to the output string regardless
            includeVals += "c1,d1,e1"
            varValues += "c1 = " + height + "; d1 = " + centre + "; e1 = " + width
            gui.click(mX,mY)

            #depending on the type of curve, will output into the keylogger the equation for the appropriate curve
            if bell == "gaussian":
                Msg("Gaussian(x) = " + eqStart + "c1*exp(-(x-d1)**2/(2*(e1)**2))")
                Msg(varValues)
                Msg("fit Gaussian(x) '05" + item + ".txt' using 1:2:3 via " + includeVals)
                Msg("plot \"05" + item + ".txt\", Gaussian(x)")
            else:
                Msg("Lorentzian(x) = " + eqStart + "c1*e1**2/(e1**2 +(x-d1)**2)")
                Msg(varValues)
                Msg("fit Lorentzian(x) '05" + item + ".txt' using 1:2:3 via " + includeVals)
                Msg("plot \"05" + item + ".txt\", Lorentzian(x)")

#list of commands added March 05 2019, a way of entering the filenames without hardcoding them
#and to allow for entries to be modified
def commands():
    while True:
        fileNames = []
        string = input("Enter a file: 05")

        #commands avaliable: "STOP","BACK","DEl" and "HELP"
        #
        #STOP command, breaks the while loop
        if string.lower() == 'stop':
            break

        #BACK command, allows the user to change an entry
        elif string.lower() == 'back':       
            if len(fileNames) > 0:
                for i in range(0,len(fileNames)):
                    print(fileNames[i],'  [',i+1,']')
                print("\n")
                string = ""
                while string == "":
                    string = input("Which place in the list would you like to change?(numer 1-"+str(len(fileNames))+"): ")
                    try:
                        val = int(string)
                        if val < 1 or val > len(fileNames):
                            print("-= Invalid input, type 'back' to leave this menu =-\n")
                        else:
                            string = input("Enter a filename to replace 05" + fileNames[val-1] + ": 05")
                            fileNames[val-1] = string
                    except:
                        print("-= Invalid input, type 'back' to leave this menu =-\n")
            else:
                print('There are no files in the list. Type \'help\' for a list of commands\n')

        #DEL command, allows the user to delete an entry
        elif string.lower() == 'del':
            if len(fileNames) > 0:
                for i in range(0,len(fileNames)):
                    print(fileNames[i],'  [',i+1,']')
                print("\n")
                string = ""
                while string == "":
                    string = input("Which place in the list would you like to remove?(numer 1-"+str(len(fileNames))+"): ")
                    try:
                        val = int(string)
                        if val < 1 or val > len(fileNames):
                            print("-= Invalid input, type 'back' to leave this menu =-\n")
                        else:
                            del fileNames[val-1]
                    except:
                        print("-= Invalid input, type 'back' to leave this menu =-\n")
            else:
                print('There are no files in the list. Type \'help\' for a list of commands\n')
                
        #PRINT command, prints all of the entries
        elif string.lower() == 'print':
            if len(fileNames) > 0:
                for i in range(0,len(fileNames)):
                    print(fileNames[i],'  [',i+1,']')
                print("\n")
            else:
                print('There are no files in the list. Type \'help\' for a list of commands\n')

        #HELP command, prints a list of avaliable commands
        elif string.lower() == 'help':
            print('-= Gaussian/Lorentzian keylogger commands =-')
            print('help \t\tGives list of commands')
            print('print\t\tPrints the list entered')
            print('back \t\tAllows you to change a value from the list of files to use')
            print('del  \t\tAllows you to delete a value from the list of files to use')
            print('stop \t\tEnds the list and continues')

        #otherwise will add the inputted string to the list
        else:
            fileNames.append(string)
    return fileNames



#main function
def main():
    key = Controller()

    #allows the user to input the file names
    print("\n-= Type 'help' for a list of commands =-\n\n")
    print("Enter the filenames you wish to use. Type 'stop' to finish the list\n")
    fileNames = commands()
    
    #loops for all values in the list
    tmp = input('Press enter to take mouse position for the GNUPlot terminal ')
    mX,mY = gui.position()
    tmp = input('Now press enter while the curser is over the python terminal ')
    pmX,pmY = gui.position()
    for item in fileNames:
        a1 = "0"
        b1 = "0"
        tmp = input("\nPress the enter key to continue: ")
        tmp = ""
        #replots the graph until the user enters 'no'
        while tmp.lower() != "no" and tmp.lower() != "n":
            sleep(0.5)
            gui.click(mX,mY)
            Msg("plot \"05" + item + ".txt\" using 1:2:3")
            gui.click(pmX,pmY)
            tmp = input("Replot?(type 'no' to move on): ")

        #allows user to enter values for the height, centre and width
        gui.click(pmX,pmY)
        height = input("\nHeight of peak: ")
        centre = input("Centre of peak: ")
        width = input("Width of peak: ")
        tmp1 = "c1 = " + height + "; d1 = " + centre + "; e1 = " + width
        sleep(0.5)
        gui.click(mX,mY)

        #plots gaussian without background
        Msg("Gaussian(x) = c1*exp(-(x-d1)**2/(2*(e1)**2))")
        Msg(tmp1)
        Msg("fit Gaussian(x) '05" + item + ".txt' using 1:2:3 via c1,d1,e1")
        Msg("plot \"05" + item + ".txt\", Gaussian(x)")
        changeBackground("gaussian",item,height,centre,width,mX,mY,pmX,pmY)
        
        tmp = input("When ready for Lorentzian fit, press enter: ")
        sleep(0.5)
        gui.click(mX,mY)
        #plots lorentzian
        Msg("Lorentzian(x) = c1*e1**2/(e1**2 +(x-d1)**2)")
        Msg(tmp1)
        Msg("fit Lorentzian(x) '05" + item + ".txt' using 1:2:3 via c1,d1,e1")
        Msg("plot \"05" + item + ".txt\", Lorentzian(x)")
        changeBackground("lorentzian",item,height,centre,width,mX,mY,pmX,pmY)

if __name__ == "__main__":
    main()
