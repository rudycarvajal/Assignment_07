#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Rcarvajal,  2020-Aug-20, Added functions and code to get script functioning  
# Rcarvajal,  2020-Aug-22, Added documentation to functions
# Rcarvajal,  2020-Aug-26, Fixed bug in get_cd function
# Rcarvajal,  2020-Aug-28, Adding structured error handling and saving as binary file
#------------------------------------------#

import pickle #pickle module to work with binary data

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # binary storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    
    
    @staticmethod
    def add_cd(cdNum, cdTitle, cdArtist, table):
        """Adds the information of a CD to a 2D table (list of dicts)
        
        Takes cd id, title and artist and formats the data as a dictionary 
        then appends it to a table
        
        Args:
            cdNum (int): ID for data entry. Must be integer value.
            cdTitle (string): string input argument for title name.
            cdArtist (string): string input argument for artist name.
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime 
        
        Returns:
            None.
            
        """
        # to check if ID already in use. If not, CD is added to inventory
        counter = 0
        for row in table:
            if row['ID'] == cdNum:
                counter += 1
        if counter > 0:
            print('\n------- ID already in use -------\n')
        else:
            dicRow = {'ID': cdNum, 'Title': cdTitle, 'Artist': cdArtist}
            table.append(dicRow)
        
    @staticmethod
    def delete_cd(table, cd):
        """Deletes an inputted CD from Inventory
        
        Takes a CD id the user inputted and searches a table to find it. If found, 
        it deletes it. If the CD is not in inventory, it lets the user know. 
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            cd (int): an integer that identifies a row of data in the indentified 2D data structure 
        
        Returns:
            None.
        """
        
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == cd:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
 

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(table, file_name):
        """Function to manage data ingestion from a binary file to a list of dictionaries

        Checks to make sure file exists and file contains data. Then reads the data from 
        a binary file identified by file_name into a 2D table (list of dicts). Will only 
        load a file and merge lists if found. 

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            file_name (string): name of file used to read the data from
            
        Returns:
            None.
        """
        
        table.clear()
        try:
            with open(file_name, 'rb') as objFile:
                data = pickle.load(objFile)
                
                if data != "":
                    table.extend(data)
                    
        except FileNotFoundError: 
            print("\n======= File not found! =======\n")
        except EOFError:
            print("\n======= File was empty. Nothing was loaded! =======\n")

    @staticmethod
    def write_file(table, file_name):
        """Function to save data (a list of dictionaries) to file
        
        Writes the data, which is a 2D data structure (list of dicts) identified 
        by the table name, to a file indentified by file_name
        
        Args:
            file_name (string): name of file to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None.
        """
        
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)
        
        
# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    def get_cd():
        """Gets user input to add a CD 
        
        Asks user for CD id, Title and Artist. Makes sure user inputted an integer
        for a CD id.
        
        Args: 
            None.
        
        Returns:
            cdID (int): ID for data entry. Must be integer value.
            cdTitle (string): string input argument for title name.
            cdArtist (string): string input argument for artist name.
        """ 
        # while statement checks to make sure user entered integer for ID
        while True:    
           try: 
               cdID = int(input('Enter an ID: ').strip())
               break;
           except ValueError:
               print("This is not a number. Please enter a valid number")        
        cdTitle = input('Enter the CD\'s Title: ').strip()
        cdArtist = input('Enter the Artist\'s Name: ').strip()
        return cdID, cdTitle, cdArtist
    

# 1. When program starts, read in the currently saved Inventory
    FileProcessor.read_file(lstTbl, strFileName)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(lstTbl, strFileName)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist and 
        intID, strTitle, strArtist = IO.get_cd()
        # 3.3.2 Add item to the table
        DataProcessor.add_cd(intID, strTitle, strArtist,lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try: 
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break;
            except ValueError:
               print("This is not a number. Please enter a valid number")
        # 3.5.1.3 Trapping for not entering an integer
        # 3.5.2 search thru table and delete CD
        DataProcessor.delete_cd(lstTbl, intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data to file
            FileProcessor.write_file(lstTbl, strFileName)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




