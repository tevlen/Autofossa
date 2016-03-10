import sys
from decimal import *
import pickle

def menu():
    print ("What module would you like to run?")
    print ("1.  Markov Model Configuration")
    print ("2.  Simulation Parameter Configuration")
    print ("3.  Simulations")
    print ("4.  Exit")
    selection = input("Type 1-4 to select module, and hit 'Enter'.\r")
    if selection =="1":
        Models()
    elif selection == "2":
        Parameters()
    elif selection == "3":
        Simulation()
    elif selection == "4":
        print("Are you sure you want to quit?")
        confirm = input("Y/N\r").lower()
        while confirm != "y" and confirm != "n":
            confirm = input("Y/N\r").lower()
        if confirm == "y":
            sys.exit()
        else:
            print("returning to menu")
    else:
        print("invalid selection")    
        
def Models():
    print ("Entering Model Configuration menu")
    print("1.  Generate new Markov Model")
    print("2.  Modify Existing Markov Model")
    print("3.  Copy Existing Markov Model")
    print("4.  View Existing Markov Model")
    print("5.  Return to Main Menu")
    selection = input("Type 1-5 to make selection, and hit 'Enter'.\r")
    while selection != "1" and selection != "2" and selection != "3" and selection != "4" and selection != "5":
        print("Invalid selection\r")
        selection = input("Type 1-5 to make selection, and hit 'Enter'.\r")
    if selection == "1":
        Model_gen()
    elif selection == "2":
        Model_mod()
    elif selection == "3":
        Model_copy()
    elif selection == "4":
        Model_view()
    elif selection == "5":
        print ("Returning to main menu\r")
        menu()
    else:
        print("We're sorry.  An error has occured.  Please restart program.  This should not happen.")
        sys.exit()

def Model_gen():
    print("Entering Model Generator")
    name = input("Please name your model\r")
    states = []
    conductances = {}
    openloop = 1
    numopen = 0
    numclosed = 0
    while openloop == 1:
        mybool = input("Generate open state? (Y/N)\r").lower()
        while mybool != "n" and mybool != "y":
            print("Invalid selection\r")
            mybool = input("Generate open state?  (Y/N)\r")
        if mybool == "y":
            stringnum = str(numopen)
            mystring = "O" + stringnum
            states.append(mystring)
            numopen = numopen +1
            output_string = "Please input Conductance of " + mystring +", a number greater than 0, and up to 1\r"
            conductance = input(output_string)
            cnotset = 0
            while cnotset ==0:
                work = 0
                try:
                    conductance = float(conductance)
                    work = 1
                except ValueError:
                    print ("Input is not a number.  Please Try again\r")
                if work == 1:
                    #conductance = Decimal(conductance)
                    print ("conductance is ", conductance, "\r")
                    if conductance > 1:
                        print("Input must be less than or equal to one.  Please try again\r")
                    elif conductance <= 0:
                        print("Input must be greater than zero.  Please try again\r")
                    else:
                        conductances = {mystring:conductance}
                        cnotset = 1
                if cnotset == 0:
                    conductance = input(output_string)
        else:
            openloop = 0
    closedloop = 1
    while closedloop == 1:
        mybool = input("Generate closed state? (Y/N)\r").lower()
        while mybool != "n" and mybool != "y":
            print("Invalid selection\r")
            mybool = input("Generate closed state?  (Y/N)\r")
        if mybool == "y":
            stringnum = str(numclosed)
            mystring = "C" + stringnum
            states.append(mystring)
            numclosed = numclosed+1
        else:
            closedloop = 0
    # at this point, all open and closed states shoudl be generated in the list "states".  
    #Open states will have their conductances held in the dictionary "conductances".
    
    #Also, if anyone else is trying to maintain/fix this, I'm so sorry for what is next.
    #There is no reason I am doing this 3d array as a dictionary.  I'm so, so sorry.
    
    rates = {}
    x = 0
    y = 0
    strmax = len(states)
    print("\rYou have generated a model with the following states:\r")
    print (states)
    print("We will now configure the connections between all possible states\r")
    #print (strmax)
    for x in range (0, strmax):
        for y in range(0, strmax):
            print ("For states ", states[x], " and ", states[y], ":\r")
            mybool = input("Are these two states connected? (Y/N)\r").lower()
            while mybool != "n" and mybool != "y":
                print("Invalid selection\r")
                mybool = input("Are these two states connected?  (Y/N)\r")
            if mybool == "y":
                print ("What Type of connection exists between these two states:", states[x], ", and ", states[y], "?\r")
                print("1.  Constant")
                print("2.  boltzman")
                print("3.  exponential")
                print("4.  LigandGated")
                print("5.  None")
                selection = input("Type 1-5 to make selection, and hit 'Enter'.\r")
                while selection != "1" and selection != "2" and selection != "3" and selection != "4" and selection != "5":
                    print("Invalid selection\r")
                    selection = input("Type 1-5 to make selection, and hit 'Enter'.\r")
                if selection == "1":
                    print("What is the constant rate of connection between states", states[x], ", and ", states[y], "?\r")
                    var = input("Please Enter a number, greater than 0.\r")
                    varnotset = 1
                    while varnotset == 1:
                        work =0
                        try:
                            var = float(var)
                            work = 1
                        except:
                            print("Constant rate must be a number.  Please try again.\r")
                            var = input("Please Enter a number, greater than 0.\r")
                        if work ==1:
                            if var > 0:
                                key = createKey(x,y,1)
                                rates [key]=1
                                key = createKey(x,y,2)
                                rates[key]=var
                                varnotset = 0
                            else:
                                print ("Constant rate must be greater than zero.  Please try again.\r")
                                var = input("Please Enter a number, greater than 0.\r")
                elif selection == "2":
                    print("You have selected a boltzman  rate constant between states", states[x], ", and ", states[y], "\r")
                    print("Boltzman rates are voltage dependent rates that utalize the boltzman equation.\r")
                    print("The boltzman equation requires three parameters:  a, v_half, and k.")
                    
                    print("Pleae enter your desired value for 'a'\r")
                    var = input("Please Enter a number\r")
                    varnotset = 1
                    while varnotset == 1:
                        work =0
                        try:
                            var = float(var)
                            work = 1
                        except:
                            print("'a' must be a number.  Please try again.\r")
                            var = input("Please Enter a number\r")
                        if work ==1:
                            if var > 0:
                                key = createKey(x,y,1)
                                rates [key]=2
                                key = createKey(x,y,2)
                                rates[key]=var
                                varnotset = 0
                    
                    print("Pleae enter your desired value for 'v_half'\r")
                    var = input("Please Enter a number\r")
                    varnotset = 1
                    while varnotset == 1:
                        work =0
                        try:
                            var = float(var)
                            work = 1
                        except:
                            print("'v_half' must be a number.  Please try again.\r")
                            var = input("Please Enter a number\r")
                        if work ==1:
                            if var > 0:
                                key = createKey(x,y,3)
                                rates[key]=var
                                varnotset = 0
                                
                    print("Pleae enter your desired value for 'k'\r")
                    var = input("Please Enter a number\r")
                    varnotset = 1
                    while varnotset == 1:
                        work =0
                        try:
                            var = float(var)
                            work = 1
                        except:
                            print("'k' must be a number.  Please try again.\r")
                            var = input("Please Enter a number\r")
                        if work ==1:
                            if var > 0:
                                key = createKey(x,y,4)
                                rates[key]=var
                                varnotset = 0
                    
                elif selection == "3":
                    print("You have selected an exponential rate constant between states", states[x], ", and ", states[y], "\r")
                    print("Exponential rates are voltage dependent rates.\r")
                    print("Exponential rates require two parameters:  a and k.")
                    
                    print("Pleae enter your desired value for 'a'\r")
                    var = input("Please Enter a number\r")
                    varnotset = 1
                    while varnotset == 1:
                        work =0
                        try:
                            var = float(var)
                            work = 1
                        except:
                            print("'a' must be a number.  Please try again.\r")
                            var = input("Please Enter a number\r")
                        if work ==1:
                            if var > 0:
                                key = createKey(x,y,1)
                                rates [key]=3
                                key = createKey(x,y,2)
                                rates[key]=var
                                varnotset = 0
                    
                    print("Pleae enter your desired value for 'k'\r")
                    var = input("Please Enter a number\r")
                    varnotset = 1
                    while varnotset == 1:
                        work =0
                        try:
                            var = float(var)
                            work = 1
                        except:
                            print("'k' must be a number.  Please try again.\r")
                            var = input("Please Enter a number\r")
                        if work ==1:
                            if var > 0:
                                key = createKey(x,y,3)
                                rates[key]=var
                                varnotset = 0
                                
                elif selection == "4":
                    print("You have selected a ligand gated rate constant between states", states[x], ", and ", states[y], "\r")
                    print("Ligand gated rate constants depend on the presence of ligand.\r")
                    print("Ligand gated connections requires three parameters:  ligand, ligand_power, and k.")
                    
                    print("Pleae enter your desired ligand\r")
                    var = input("Please Enter a string\r")
                    varnotset = 1
                    while varnotset == 1:
                        if input =='':
                            print("You must enter a ligand")
                            var = input("Please Enter a string\r")
                        else:
                            key = createKey(x,y,1)
                            rates [key]=4
                            key = createKey(x,y,2)
                            rates[key]=var
                            varnotset = 0
                    
                    print("Pleae enter your desired value for 'ligand_power'\r")
                    var = input("Please Enter a number\r")
                    varnotset = 1
                    while varnotset == 1:
                        work =0
                        try:
                            var = float(var)
                            work = 1
                        except:
                            print("'ligand_power' must be a number.  Please try again.\r")
                            var = input("Please Enter a number\r")
                        if work ==1:
                            if var > 0:
                                key = createKey(x,y,3)
                                rates[key]=var
                                varnotset = 0
                                
                    print("Pleae enter your desired value for 'k'\r")
                    var = input("Please Enter a number\r")
                    varnotset = 1
                    while varnotset == 1:
                        work =0
                        try:
                            var = float(var)
                            work = 1
                        except:
                            print("'k' must be a number.  Please try again.\r")
                            var = input("Please Enter a number\r")
                        if work ==1:
                            if var > 0:
                                key = createKey(x,y,4)
                                rates[key]=var
                                varnotset = 0
                elif selection == "5":
                    key = createKey(x,y,1)
                    rates[key] = 0
                else:
                    print("We're sorry.  An error has occured.  Please restart program.  This should not happen.")
                    sys.exit()                
            else:
                key = createKey(x,y,1)
                rates[key]= 0
            y=y+1
        x = x+1
    print("Model is fully defined.  Model will now save to file\r")
    fileString = name + "_model.p"
    fileString = str(fileString)
    with open(fileString, 'wb') as f:
        pickle.dump(name, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(states, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(conductances, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(rates, f, pickle.HIGHEST_PROTOCOL)
    print("Module successfully configured.  Returning to main menu\r")
    
    
def createKey(a, b, c):
    a = str(a)
    b = str(b)
    c = str(c)
    newstring = a +"," + b + "," + c
    #print (newstring)
    return newstring

def Model_mod():
    print("Entering Model Modifier")
    
def Model_copy():
    print("Entering Model Copier")
    #PLEASE MAKE A WAY TO SHOW ALL OF THE MODELS IN THE WORKING FOLDER!!!
    print("Pleae enter the name of the model you wish to open\r")
    var = input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if input =='':
            print("You must enter a name")
            var = input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_model.p"
    with open(fileString, 'rb') as f:
        name = pickle.load(f)
        states = pickle.load(f)
        conductances = pickle.load(f)
        rates = pickle.load(f)
        
    print("Pleae enter the name you would like to save the new model as\r")
    var = input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if input =='':
            print("You must enter a name")
            var = input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_model.p"    
    with open(fileString, 'wb') as f:
        pickle.dump(name, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(states, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(conductances, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(rates, f, pickle.HIGHEST_PROTOCOL)
    print("Model successfully saved")
    
def Model_view():
    print("Entering Model Viewer")
    #PLEASE MAKE A WAY TO SHOW ALL OF THE MODELS IN THE WORKING FOLDER!!!
    print("Pleae enter the name of the model you wish to open\r")
    var = input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if input =='':
            print("You must enter a name")
            var = input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_model.p"
    with open(fileString, 'rb') as f:
        name = pickle.load(f)
        states = pickle.load(f)
        conductances = pickle.load(f)
        rates = pickle.load(f)
        print("You are now viewing the following modle:")
        print(name)
        print("\rname has the following states:\r")
        print(states)
        print("\rThe open states have the following conductances\r")
        print(conductances)
        print("\rThe rate table is as follows (appologies that it is still in its raw data form.  This will be fixed soon.)\r")
        print(rates)
        print("\rReturning to Main Menu\r")

def Parameters():
    print ("Entering Simulation parameter Configuration menu")
    
def Simulation():
    print ("entering Simulation mode")

while 1:
    menu()
