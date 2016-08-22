import sys
from decimal import *
import pickle
from modFossa import *

def menu():
    print ("What module would you like to run?")
    print ("1.  Markov Model Configuration")
    print ("2.  Simulation Parameter Configuration")
    print ("3.  Simulations")
    print ("4.  Exit")
    selection = raw_input("Type 1-4 to select module, and hit 'Enter'.\r")
    if selection =='1':
        Models()
    elif selection == '2':
        Parameters()
    elif selection == '3':
        Simulation()
    elif selection == '4':
        print("Are you sure you want to quit?")
        confirm = raw_input("Y/N\r").lower()
        while confirm != "y" and confirm != "n":
            confirm = raw_input("Y/N\r").lower()
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
    selection = raw_input("Type 1-5 to make selection, and hit 'Enter'.\r")
    while selection != '1' and selection != '2' and selection != '3' and selection != '4' and selection != '5':
        print("Invalid selection\r")
        selection = raw_input("Type 1-5 to make selection, and hit 'Enter'.\r")
    if selection == '1':
        Model_gen()
    elif selection == '2':
        Model_mod()
    elif selection == '3':
        Model_copy()
    elif selection == '4':
        print("Entering Model Viewer")
        Model_view()
    elif selection == '5':
        print ("Returning to main menu\r")
        menu()
    else:
        print("We're sorry.  An error has occured.  Please restart program.  This should not happen.")
        sys.exit()

def Model_gen():
    print("Entering Model Generator")
    name = raw_input("Please name your model\r")
    states = []
    conductances = {}
    openloop = 1
    numopen = 0
    numclosed = 0
    while openloop == 1:
        mybool = raw_input("Generate open state? (Y/N)\r").lower()
        while mybool != "n" and mybool != "y":
            print("Invalid selection\r")
            mybool = raw_input("Generate open state?  (Y/N)\r")
        if mybool == "y":
            stringnum = str(numopen+1)
            mystring = "O" + stringnum
            states.append(mystring)
            numopen = numopen +1
            output_string = "Please input Conductance of " + mystring +", a number greater than 0, and up to 1\r"
            conductance = raw_input(output_string)
            cnotset = 0
            while cnotset ==0:
                work = 0
                try:
                    conductance = float(conductance)
                    work = 1
                except ValueError:
                    print ("input is not a number.  Please Try again\r")
                if work == 1:
                    #conductance = Decimal(conductance)
                    print ("conductance is ", conductance, "\r")
                    if conductance > 1:
                        print("input must be less than or equal to one.  Please try again\r")
                    elif conductance <= 0:
                        print("input must be greater than zero.  Please try again\r")
                    else:
                        conductances[mystring] = conductance
                        cnotset = 1
                if cnotset == 0:
                    conductance = raw_input(output_string)
        else:
            openloop = 0
    closedloop = 1
    print("conductances are ")
    print(conductances)
    while closedloop == 1:
        mybool = raw_input("Generate closed state? (Y/N)\r").lower()
        while mybool != "n" and mybool != "y":
            print("Invalid selection\r")
            mybool = raw_input("Generate closed state?  (Y/N)\r")
        if mybool == "y":
            stringnum = str(numclosed+1)
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
    print("\rYour states have the following conductances:\r")
    print (conductances)
    print("We will now configure the connections between all possible states\r")
    #print (strmax)
    for x in range (0, strmax):
        for y in range(0, strmax):
            if y!=x:
                print ("For states ", states[x], " and ", states[y], ":\r")
                mybool = raw_input("Are these two states connected? (Y/N)\r").lower()
                while mybool != "n" and mybool != "y":
                    print("Invalid selection\r")
                    mybool = raw_input("Are these two states connected?  (Y/N)\r")
                if mybool == "y":
                    print ("What Type of connection exists between these two states:", states[x], ", and ", states[y], "?\r")
                    print("1.  Constant")
                    print("2.  boltzman")
                    print("3.  exponential")
                    print("4.  LigandGated")
                    print("5.  None")
                    selection = raw_input("Type 1-5 to make selection, and hit 'Enter'.\r")
                    while selection != '1' and selection != '2' and selection != '3' and selection != '4' and selection != '5':
                        print("Invalid selection\r")
                        selection = raw_input("Type 1-5 to make selection, and hit 'Enter'.\r")
                    if selection == '1':
                        print("What is the constant rate of connection between states", states[x], ", and ", states[y], "?\r")
                        var = raw_input("Please Enter a number, greater than 0.\r")
                        varnotset = 1
                        while varnotset == 1:
                            work =0
                            try:
                                var = float(var)
                                work = 1
                            except:
                                print("Constant rate must be a number.  Please try again.\r")
                                var = raw_input("Please Enter a number, greater than 0.\r")
                            if work ==1:
                                if var > 0:
                                    key = createKey(states[x],states[y],1)
                                    rates [key]=1
                                    key = createKey(states[x],states[y],2)
                                    rates[key]=var
                                    varnotset = 0
                                else:
                                    print ("Constant rate must be greater than zero.  Please try again.\r")
                                    var = raw_input("Please Enter a number, greater than 0.\r")
                    elif selection == '2':
                        print("You have selected a boltzman  rate constant between states", states[x], ", and ", states[y], "\r")
                        print("Boltzman rates are voltage dependent rates that utalize the boltzman equation.\r")
                        print("The boltzman equation requires three parameters:  a, v_half, and k.")
                        
                        print("Pleae enter your desired value for 'a'\r")
                        var = raw_input("Please Enter a number\r")
                        varnotset = 1
                        while varnotset == 1:
                            work =0
                            try:
                                var = float(var)
                                work = 1
                            except:
                                print("'a' must be a number.  Please try again.\r")
                                var = raw_input("Please Enter a number\r")
                            if work ==1:
                                if var > 0:
                                    key = createKey(states[x],states[y],1)
                                    rates [key]=2
                                    key = createKey(states[x],states[y],2)
                                    rates[key]=var
                                    varnotset = 0
                        
                        print("Pleae enter your desired value for 'v_half'\r")
                        var = raw_input("Please Enter a number\r")
                        varnotset = 1
                        while varnotset == 1:
                            work =0
                            try:
                                var = float(var)
                                work = 1
                            except:
                                print("'v_half' must be a number.  Please try again.\r")
                                var = raw_input("Please Enter a number\r")
                            if work ==1:
                                key = createKey(states[x],states[y],3)
                                rates[key]=var
                                varnotset = 0
                                    
                        print("Pleae enter your desired value for 'k'\r")
                        var = raw_input("Please Enter a number\r")
                        varnotset = 1
                        while varnotset == 1:
                            work =0
                            try:
                                var = float(var)
                                work = 1
                            except:
                                print("'k' must be a number.  Please try again.\r")
                                var = raw_input("Please Enter a number\r")
                            if work ==1:
                                if var > 0:
                                    key = createKey(states[x],states[y],4)
                                    rates[key]=var
                                    varnotset = 0
                        
                    elif selection == '3':
                        print("You have selected an exponential rate constant between states", states[x], ", and ", states[y], "\r")
                        print("Exponential rates are voltage dependent rates.\r")
                        print("Exponential rates require two parameters:  a and k.")
                        
                        print("Pleae enter your desired value for 'a'\r")
                        var = raw_input("Please Enter a number\r")
                        varnotset = 1
                        while varnotset == 1:
                            work =0
                            try:
                                var = float(var)
                                work = 1
                            except:
                                print("'a' must be a number.  Please try again.\r")
                                var = raw_input("Please Enter a number\r")
                            if work ==1:
                                if var > 0:
                                    key = createKey(states[x],states[y],1)
                                    rates [key]=3
                                    key = createKey(states[x],states[y],2)
                                    rates[key]=var
                                    varnotset = 0
                        
                        print("Pleae enter your desired value for 'k'\r")
                        var = raw_input("Please Enter a number\r")
                        varnotset = 1
                        while varnotset == 1:
                            work =0
                            try:
                                var = float(var)
                                work = 1
                            except:
                                print("'k' must be a number.  Please try again.\r")
                                var = raw_input("Please Enter a number\r")
                            if work ==1:
                                if var > 0:
                                    key = createKey(states[x],states[y],3)
                                    rates[key]=var
                                    varnotset = 0
                                    
                    elif selection == '4':
                        print("You have selected a ligand gated rate constant between states", states[x], ", and ", states[y], "\r")
                        print("Ligand gated rate constants depend on the presence of ligand.\r")
                        print("Ligand gated connections requires three parameters:  ligand, ligand_power, and k.")
                        
                        print("Pleae enter your desired ligand\r")
                        var = raw_input("Please Enter a string\r")
                        varnotset = 1
                        while varnotset == 1:
                            if raw_input =='':
                                print("You must enter a ligand")
                                var = raw_input("Please Enter a string\r")
                            else:
                                key = createKey(states[x],states[y],1)
                                rates [key]=4
                                key = createKey(states[x],states[y],2)
                                rates[key]=var
                                varnotset = 0
                        
                        print("Pleae enter your desired value for 'ligand_power'\r")
                        var = raw_input("Please Enter a number\r")
                        varnotset = 1
                        while varnotset == 1:
                            work =0
                            try:
                                var = float(var)
                                work = 1
                            except:
                                print("'ligand_power' must be a number.  Please try again.\r")
                                var = raw_input("Please Enter a number\r")
                            if work ==1:
                                if var > 0:
                                    key = createKey(states[x],states[y],3)
                                    rates[key]=var
                                    varnotset = 0
                                    
                        print("Pleae enter your desired value for 'k'\r")
                        var = raw_input("Please Enter a number\r")
                        varnotset = 1
                        while varnotset == 1:
                            work =0
                            try:
                                var = float(var)
                                work = 1
                            except:
                                print("'k' must be a number.  Please try again.\r")
                                var = raw_input("Please Enter a number\r")
                            if work ==1:
                                if var > 0:
                                    key = createKey(states[x],states[y],4)
                                    rates[key]=var
                                    varnotset = 0
                    elif selection == '5':
                        key = createKey(states[x],states[y],1)
                        rates[key] = 0
                    else:
                        print("We're sorry.  An error has occured.  Please restart program.  This should not happen.")
                        sys.exit()                
                else:
                    key = createKey(states[x],states[y],1)
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
    print("To modify a model, first you must select a model to modify")
    Model_view()
    print("How would you to modify the model?")
    print("1.  Add or remove states")
    print("2.  Change Connections between states")
    print("3.  Return to Main Menu")
    selection = raw_input("Type 1-3 to make selection, and hit 'Enter'.\r")
    while selection != '1' and selection != '2' and selection != '3' and selection != '4' and selection != '5':
        print("Invalid selection\r")
        selection = raw_input("Type 1-3 to make selection, and hit 'Enter'.\r")
    if selection == '1':
        #Fix this later.  I probably won't have time to, but Hopefully I will.
        print("This Section is not yet implemented.  Our appologies.  For fundamental changes to Model, including number of states, please Generate a new Model")
    elif selection == '2':
        x = 0
        y = 0
        strmax = len(states)
        print("\rYou are currently modifying a model with the following states:\r")
        print (states)
        for x in range (0, strmax):
            print(x, ", ", state[x], "\r")
            
        #Save modified model
        print("Model is fully defined.  Model will now save to file\r")
        fileString = name + "_model.p"
        fileString = str(fileString)
        with open(fileString, 'wb') as f:
            pickle.dump(name, f, pickle.HIGHEST_PROTOCOL)
            pickle.dump(states, f, pickle.HIGHEST_PROTOCOL)
            pickle.dump(conductances, f, pickle.HIGHEST_PROTOCOL)
            pickle.dump(rates, f, pickle.HIGHEST_PROTOCOL)
        print("Module successfully configured.  Returning to main menu\r")
    elif selection == '3':
        print ("Returning to main menu\r")
        menu()
    else:
        print("We're sorry.  An error has occured.  Please restart program.  This should not happen.")
        sys.exit()    
    
def Model_copy():
    print("Entering Model Copier")
    #PLEASE MAKE A WAY TO SHOW ALL OF THE MODELS IN THE WORKING FOLDER!!!
    print("Pleae enter the name of the model you wish to open\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a name")
            var = raw_input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_model.p"
    with open(fileString, 'rb') as f:
        name = pickle.load(f)
        states = pickle.load(f)
        conductances = pickle.load(f)
        rates = pickle.load(f)
        
    print("Pleae enter the name you would like to save the new model as\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a name")
            var = raw_input("Please Enter a string\r")
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
    #PLEASE MAKE A WAY TO SHOW ALL OF THE MODELS IN THE WORKING FOLDER!!!
    print("Pleae enter the name of the model you wish to open\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a name")
            var = raw_input("Please Enter a string\r")
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

def Parameters():  #Done
    print ("Entering Simulation parameter Configuration menu")
    print("1.  Generate Experimental Procedure")
    print("2.  Modify Existing Experimental Procedure")
    print("3.  Copy Existing Experimental Procedure")
    print("4.  View Existing Experimental Procedure")
    print("5.  Return to Main Menu")
    selection = raw_input("Type 1-5 to make selection, and hit 'Enter'.\r")
    while selection != '1' and selection != '2' and selection != '3' and selection != '4' and selection != '5':
        print("Invalid selection\r")
        selection = raw_input("Type 1-5 to make selection, and hit 'Enter'.\r")
    if selection == '1':
        Param_gen()
    elif selection == '2':
        Param_mod()
    elif selection == '3':
        Param_copy()
    elif selection == '4':
        print("Entering Model Viewer")
        Param_view()
    elif selection == '5':
        print ("Returning to main menu\r")
        menu()
    else:
        print("We're sorry.  An error has occured.  Please restart program.  This should not happen.")
        sys.exit()
        
def Param_gen():
    print("Entered Simulation Param Generation\r")
    nameset = 0
    while nameset == 0:
        pname = raw_input("Please name your Parameter set\r")
        if pname != "" and pname != "\r":
            name = pname
            nameset = 1
        else:
            print("Invalid name.  Please enter a name\r")
    oParam = []  #Should contain initial state, membraneCapacitance, maxchannelConductance, and reversalPotential.  You still need to raw_input these
    oParam.append(name)
    print("Parameter file successfully named ")
    print(oParam[0])
    print("we will now configure the overall simulation parameters\r")
    oSet = 0
    while oSet == 0:
        iState = raw_input("Please input your initial state\r")
        if iState != "" and iState != "\r":
            oParam.append(iState)
            oSet = 1
        else:
            print("Invalid input.  Please input a string")
    oSet = 0
    while oSet == 0:
        iState = raw_input("Please input membrane capacitance\r")
        try:
            iState = float(iState)
            oParam.append(iState)
            oSet = 1
        except ValueError:
            print("Invalid input.  Please input a number")
    oSet = 0
    while oSet == 0:
        iState = raw_input("Please input maximum channel conductance\r")
        try:
            iState = float(iState)
            oParam.append(iState)
            oSet = 1
        except ValueError:
            print("Invalid input.  Please input a number")
    oSet = 0
    while oSet == 0:
        iState = raw_input("Please input reversal potential\r")
        try:
            iState = float(iState)
            oParam.append(iState)
            oSet = 1
        except ValueError:
            print("Invalid input.  Please input a number")
    
    print ('Current contents of Parameter')
    print (oParam[0])
    print("Initial state: ")
    print(oParam[1])
    print("membrane Capacitance: ")
    print(oParam[2])
    print("Max Channel Conductance: ")
    print(oParam[3])
    print("reversal Potential: ")
    print(oParam[4])
    vParam = {}
    cParam = []
    openloop = 1
    x = 1
    lparam = 0
    while openloop == 1:
        mybool = raw_input("Add a voltage stage? (Y/N)\r").lower()
        while mybool != "n" and mybool != "y":
            print("Invalid selection\r")
            mybool = raw_input("Add a voltage stage?  (Y/N)\r")
        if mybool == "y":
            lparam = lparam+1
            print("Is this stage a hold, or a step (hold/step\r)")
            loop2 = 1
            while loop2 == 1:
                mybool2 = raw_input("Hold or step?\r").lower()
                if mybool2 != 'hold' and mybool2 != 'step':
                    print("Invalid input.  Please choose hold or step")
                else:
                    loop2 = 0
            if mybool2 == 'hold':
                print ("Please input the voltage to hold at.\r")
                vnotset = 1
                while vnotset == 1:
                    var = raw_input("Please input a number\r")
                    try:
                        var = float(var)
                        vnotset = 0
                    except ValueError:
                        print ("input is not a number.  Please try again\r")
                        var = raw_input("Please input a number\r")
                voltage = var
                dnotset = 1
                while dnotset == 1:
                    var = raw_input("Please input duration")
                    try:
                        var = float(var)
                        dnotset = 0
                    except ValueError:
                        print("input is not a number, please try again\r")
                        var = raw_input("Please input a number\r")
                duration = var
                key = createKey('concentrations', x, 0)
                vParam[key] = 1
                key = createKey('concentrations', x, 1)
                vParam[key] = voltage
                key = createKey('concentrations', x, 2)
                vParam[key] = duration
            elif mybool2 == 'step':
                print ("Please input the starting voltage\r")
                startnotset = 1
                while startnotset == 1:
                    var = raw_input("Please input a number\r")
                    try:
                        var = float(var)
                        startnotset = 0
                    except ValueError:
                        print ("input is not a number.  Please try again\r")
                        var = raw_input("Please input a number\r")
                start = var
                stopnotset = 1
                while stopnotset == 1:
                    var = raw_input("Please input a number for stop\r")
                    try:
                        var = float(var)
                        stopnotset = 0
                    except ValueError:
                        print("input is not a number, please try again\r")
                        var = raw_input("Please input a number\r")
                stop = var
                stepnotset = 1
                while stepnotset == 1:
                    var = raw_input("Please input a number for step\r")
                    try:
                        var = float(var)
                        stepnotset = 0
                    except ValueError:
                        print("input is not a number, please try again\r")
                        var = raw_input("Please input a number\r")
                step = var
                durationnotset = 1
                while durationnotset == 1:
                    var = raw_input("Please input a number for duration\r")
                    try:
                        var = float(var)
                        durationnotset = 0
                    except ValueError:
                        print("input is not a number, please try again\r")
                        var = raw_input("Please input a number\r")
                duration = var
                key = createKey('concentrations', x, 0)
                vParam[key] = 2
                key = createKey('concentrations', x, 1)
                vParam[key] = start
                key = createKey('concentrations', x, 2)
                vParam[key] = stop
                key = createKey('concentrations', x, 3)
                vParam[key] = step
                key = createKey('concentrations', x, 4)
                vParam[key] = duration
            else:  
                print ("this should not happen.  Our appologies")
            x = x+1
        else:
            print("Voltage proticol completed")
            vParam[0] = lparam
            print(vParam)
            openloop = 0
    openloop = 1
    print("Please enter your desired ligand\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    x = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a ligand")
            var = raw_input("Please Enter a string\r")
        else:
            cParam.append(var)
            varnotset = 0  
    while openloop == 1:
        print ("Please input first concentration\r")
        print ("You will input the concentration of ligand as two parts, a magnitude and a multiplier\r")
        varnotset = 1
        while varnotset == 1:  #I think I'm accepting all numbers, but I should just accept ints.  Maybe fix this later.
            var = raw_input ("Please enter magnitude.  The magnitude will be entered as 10^X\r")
            try:
                var = float(var)
                varnotset=0
            except:
                print("Ligand magnatude must be a number")
                var = raw_input ("Please enter magnitude.\r")
        varnotset = 1
        var = 10**var
        while varnotset == 1:
            var2 = raw_input ("Please enter scalar\r")
            work = 0
            try:
                var2 = float(var2)
                work = 1
            except:
                print("Ligand scalar must be a number")
                va2r = raw_input ("Please enter scalar.\r")
            if work == 1:
                if var2 <=0:
                    print("Ligand scalar must be greater than zero\r")
                    var = raw_input("Please enter scalar.\r")
                else:
                    varnotset = 0
        var = var * var2
        cParam.append(var)
        x = x+1
        print("Do you want to input an additional concentration?\r")
        confirm = raw_input ("Y/N\r").lower()
        while confirm != "y" and confirm != "n":
            confirm = raw_input ("Y/N\r")
        if confirm == 'n':
            openloop = 0
    print("Pleae enter the name you would like to save the new parameters as\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a name")
            var = raw_input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_Params.p"    
    with open(fileString, 'wb') as f:
        pickle.dump(name, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(oParam, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(vParam, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(cParam, f, pickle.HIGHEST_PROTOCOL)
    print("Parameters successfully saved")    

def Param_mod():
    print("Entering Simulation Parameter Modification\r")
    print("This section is not yet implemented.  Our oppologies")
    
def Param_copy():  #Completed with the small exception of showing options
    print("Entering Simulation Parameter Copy mode\r")
    #PLEASE MAKE A WAY TO SHOW ALL OF THE MODELS IN THE WORKING FOLDER!!!
    print("Pleae enter the name of the model you wish to open\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a name")
            var = raw_input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_Params.p"
    with open(fileString, 'rb') as f:
        name = pickle.load(f)
        oParam = pickle.load(f)
        vParam = pickle.load(f)
        cParam = pickle.load(f)
        
    print("Pleae enter the name you would like to save the new parameters as\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a name")
            var = raw_input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_Params.p"    
    with open(fileString, 'wb') as f:
        pickle.dump(name, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(oParam, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(vParam, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(cParam, f, pickle.HIGHEST_PROTOCOL)
    print("Parameters successfully saved")
    
def Param_view():  #Completed, but Please make it more user friendly, perhaps by going through the variables one at a time.  
    print("Entering Simulation Parameter Viewer\r")
    #PLEASE MAKE A WAY TO SHOW ALL OF THE MODELS IN THE WORKING FOLDER!!!
    print("Pleae enter the name of the Parameter file you wish to open\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a name")
            var = raw_input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_Params.p"
    with open(fileString, 'rb') as f:
        name = pickle.load(f)
        oParams = pickle.load(f)
        vParams = pickle.load(f)
        cParam = pickle.load(f)
        print("You are now viewing the following Parameter file:")
        print(name)
        print("\rname has the following overall Parameters:\r")
        print(oParams)
        print("\rThe following Voltage Proticols\r")
        print(vParams)
        print("\rThe following Concentration proticols)\r")
        print(cParam)

def Simulation():
    print ("entering Simulation mode")
    print("Pleae enter the name of the model you wish to open\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a name")
            var = raw_input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_model.p"
    with open(fileString, 'rb') as f:
        name = pickle.load(f)
        states = pickle.load(f)
        conductances = pickle.load(f)
        rates = pickle.load(f)

    #Define the states
    print("defining states")
    for x in states:
	print(x)
        if x[0] == 'O':
            print conductances
            dvar = conductances[x]
            print dvar
            state(x, conducting = True, gating = conductances[x])
        else:
            state(x)
    #Define the Connections and rates
    print rates
    for x in states:
        for y in states:
            if x!=y:
                key = createKey(x, y, 1)
                #if rates[key] == 0:
                    #Yeah this doesn't do anything maybe do something here?
                if rates[key] == 1: #constant
                    connection = x + y
                    #print(connection)
                    connect(fromState=x, toState=y, rate =connection)
                    key = createKey(x, y, 2)
                    rate(connection, type ='constant', k = rates[key])
                if rates[key] == 2: #Boltzman
                    connection = x + y
                    connect(fromState=x, toState = y, rate = connection)
                    key1 = createKey(x, y, 2)
                    key2 = createKey(x, y, 3)
                    key3 = createKey(x, y, 4)
                    rate(connection, type = 'sigmoidal', a = rates[key1], v_half = rates[key2], k = rates[key3])#This might have to be boltzman instead.  Documentation is unclear
                if rates[key] ==3: #Exponential
                    connection = x + y
                    connect(fromState=x, toState = y, rate = connection)
                    key1 = createKey(x, y, 2)
                    key2 = createKey(x, y, 3)
                    rate(connection, type = 'exponential', a = rates[key1], k = rates[key2])
                if rates[key] == 4:  #ligandGated
                    connection = x + y
                    connect(fromState=x, toState = y, rate = connection)
                    key1 = createKey(x, y, 2)
                    key2 = createKey(x, y, 3)
                    key3 = createKey(x, y, 4)
                    rate(connection, type = 'ligandGated', ligand = rates[key1], power = rates[key2], k = rates[key3])
    
    print("Pleae enter the name of the Parameter file you wish to open\r")
    var = raw_input("Please Enter a string\r")
    varnotset = 1
    while varnotset == 1:
        if raw_input =='':
            print("You must enter a name")
            var = raw_input("Please Enter a string\r")
        else:
            varnotset = 0
    fileString = var + "_Params.p"
    with open(fileString, 'rb') as f:
        name2 = pickle.load(f)
        oParam = pickle.load(f)
        vParam = pickle.load(f)
        cParam = pickle.load(f)                

    initialState(oParam[1])
    membraneCapacitance(oParam[2])
    maxChannelConductance(oParam[3])
    reversalPotential(oParam[4])
    
    voltageProtocol('vp')
    x = 1
    print vParam
    z=0
    lparam = vParam[0]
    while x < lparam:
        print("x is ")
        print(x)
        print("lparam is")
        print(lparam)
        key1 = createKey('concentrations', x, 0)
        key2 = createKey('concentrations', x, 1)
        key3 = createKey('concentrations', x, 2)
        key4 = createKey('concentrations', x, 3)
        key5 = createKey('concentrations', x, 4)
        if vParam[key1] == 1:
            #Hold
            vpname = 'hold' + str(z)
            arg1 = int(vParam[key2])
            arg2 = int(vParam[key3])
            voltageProtocolAddStage('vp', vpname, voltage = arg1, duration = arg2)
        elif vParam[key1] == 2:
            #Step
            vpname = 'step' + str(z)
            arg1 = int(vParam[key2])
            arg2 = int(vParam[key3])
            arg3 = int(vParam[key4])
            arg4 = int(vParam[key5])
            voltageProtocolAddStage('vp', vpname, start = arg1, stop = arg2, step = arg3, duration = arg4)            
        else:
            print("This Should not happen")
        x=x+1
    x = 1
    concentrationProtocol('concentrations')
    print("cparam is ")
    print(cParam)
    print("cParam 0 is ", cParam[0])
    while x < len(cParam):
        print("Cparam ", x, "is ", cParam[x], "\r")
        addConcentration('concentrations', Ca=cParam[x])
        x=x+1
    
    experiment(name, 'vp', 'concentrations')
    validate()
    run()
    
    #Plotting
    
    currents = plotMultipleCurrents(name)
    gVsV = plotGvsV(name, time_ms =1099) #Maybe figure this part out
    gVsCa = plotGvsConcentration(name, time_ms = 1099)
    
    iv_late = plotMultipleIV(name, time_ms = 1099, ymin = -10, ymax = 50, labelHeight = 40)
    iv_tail = plotMultipleIV(name, time_ms = 1099, ymin = -30, ymax = 30, labelHeight = 20)
    
        
        
    
                
                
                
while 1:
    menu()
