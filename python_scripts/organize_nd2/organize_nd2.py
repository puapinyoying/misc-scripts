#! /bin/python3

import itertools
import argparse
import textwrap
import shutil
import sys
import os 
import re


#################
### Constants ###
#################


REGEXP = r'(\w+)_Well(\w+)_Channel(\d+) nm,(\d+) nm,(\d+) nm,(\d+) nm_(\w+).(nd2)'

DRUG_DICT = {
'drug1': {
'dose1': ['A01','A03','A05', 'A07'],    'dose2': ['C01','C03','C05', 'C07'], 
'dose3': ['E01','E03','E05', 'E07'],    'dose4': ['G01','G03','G05', 'G07'],
'dose5': ['I01','I03','I05', 'I07'],    'dose6': ['K01','K03','K05', 'K07'],
'dose7': ['M01','M03','M05', 'M07'],    'dose8': ['O01','O03','O05', 'O07']},
            
'drug2': {
'dose1': ['A02','A04','A06', 'A08'],    'dose2': ['C02','C04','C06', 'C08'], 
'dose3': ['E02','E04','E06', 'E08'],    'dose4': ['G02','G04','G06', 'G08'],
'dose5': ['I02','I04','I06', 'I08'],    'dose6': ['K02','K04','K06', 'K08'],
'dose7': ['M02','M04','M06', 'M08'],    'dose8': ['O02','O04','O06', 'O08']},
            
'drug3': {
'dose1': ['A09','A11','A13', 'A15'],    'dose2': ['C09','C11','C13', 'C15'],
'dose3': ['E09','E11','E13', 'E15'],    'dose4': ['G09','G11','G13', 'G15'],
'dose5': ['I09','I11','I13', 'I15'],    'dose6': ['K09','K11','K13', 'K15'],
'dose7': ['M09','M11','M13', 'M15'],    'dose8': ['O09','O11','O13', 'O15']},
            
'drug4': {
'dose1': ['A10','A12','A14', 'A16'],    'dose2': ['C10','C12','C14', 'C16'],
'dose3': ['E10','E12','E14', 'E16'],    'dose4': ['G10','G12','G14', 'G16'],
'dose5': ['I10','I12','I14', 'I16'],    'dose6': ['K10','K12','K14', 'K16'],
'dose7': ['M10','M12','M14', 'M16'],    'dose8': ['O10','O12','O14', 'O16']},
            
'drug5': {
'dose1': ['A17','A19','A21', 'A23'],    'dose2': ['C17','C19','C21', 'C23'],
'dose3': ['E17','E19','E21', 'E23'],    'dose4': ['G17','G19','G21', 'G23'],
'dose5': ['I17','I19','I21', 'I23'],    'dose6': ['K17','K19','K21', 'K23'],
'dose7': ['M17','M19','M21', 'M23'],    'dose8': ['O17','O19','O21', 'O23']},

'drug6': {
'dose1': ['A18','A20','A22', 'A24'],    'dose2': ['C18','C20','C22', 'C24'],
'dose3': ['E18','E20','E22', 'E24'],    'dose4': ['G18','G20','G22', 'G24'],
'dose5': ['I18','I20','I22', 'I24'],    'dose6': ['K18','K20','K22', 'K24'],
'dose7': ['M18','M20','M22', 'M24'],    'dose8': ['O18','O20','O22', 'O24']},

'drug7': {
'dose1': ['B01','B03','B05', 'B07'],    'dose2': ['D01','D03','D05', 'D07'],
'dose3': ['F01','F03','F05', 'F07'],    'dose4': ['H01','H03','H05', 'H07'],
'dose5': ['J01','J03','J05', 'J07'],    'dose6': ['L01','L03','L05', 'L07'],
'dose7': ['N01','N03','N05', 'N07'],    'dose8': ['P01','P03','P05', 'P07']},
            
'drug8': {
'dose1': ['B02','B04','B06', 'B08'],    'dose2': ['D02','D04','D06', 'D08'],
'dose3': ['F02','F04','F06', 'F08'],    'dose4': ['H02','H04','H06', 'H08'],
'dose5': ['J02','J04','J06', 'J08'],    'dose6': ['L02','L04','L06', 'L08'],
'dose7': ['N02','N04','N06', 'N08'],    'dose8': ['P02','P04','P06', 'P08']},

'drug9': {
'dose1': ['B09','B11','B13', 'B15'],    'dose2': ['D09','D11','D13', 'D15'],
'dose3': ['F09','F11','F13', 'F15'],    'dose4': ['H09','H11','H13', 'H15'],
'dose5': ['J09','J11','J13', 'J15'],    'dose6': ['L09','L11','L13', 'L15'],
'dose7': ['N09','N11','N13', 'N15'],    'dose8': ['P09','P11','P13', 'P15']},
            
'drug10':{
'dose1': ['B10','B12','B14', 'B16'],    'dose2': ['D10','D12','D14', 'D16'],
'dose3': ['F10','F12','F14', 'F16'],    'dose4': ['H10','H12','H14', 'H16'],
'dose5': ['J10','J12','J14', 'J16'],    'dose6': ['L10','L12','L14', 'L16'],
'dose7': ['N10','N12','N14', 'N16'],    'dose8': ['P10','P12','P14', 'P16']},
            
'drug11':{
'dose1': ['B17','B19','B21', 'B23'],    'dose2': ['D17','D19','D21', 'D23'],
'dose3': ['F17','F19','F21', 'F23'],    'dose4': ['H17','H19','H21', 'H23'],
'dose5': ['J17','J19','J21', 'J23'],    'dose6': ['L17','L19','L21', 'L23'],
'dose7': ['N17','N19','N21', 'N23'],    'dose8': ['P17','P19','P21', 'P23']},
 
 'drug12':{
'dose1': ['B18','B20','B22', 'B24'],    'dose2': ['D18','D20','D22', 'D24'],
'dose3': ['F18','F20','F22', 'F24'],    'dose4': ['H18','H20','H22', 'H24'],
'dose5': ['J18','J20','J22', 'J24'],    'dose6': ['L18','L20','L22', 'L24'],
'dose7': ['N18','N20','N22', 'N24'],    'dose8': ['P18','P20','P22', 'P24']}
}

DRUG_DIRS = ['drug1','drug2','drug3','drug4','drug5','drug6',
                'drug7','drug8','drug9','drug10','drug11', 'drug12']

DOSE_DIRS = ['dose1','dose2','dose3','dose4','dose5','dose6','dose7','dose8']



#################
### Functions ###
#################

def check_folder_exist(filesDir):
    """Make sure the file exists"""
    if not os.path.exists(filesDir):
        file_name = os.path.basename(filesDir)
        print(f"*Error: This path doesn't seem to exist...(type -h for help)\n\t'{filesDir}'")
        sys.exit(1)

def get_nd2_fileList(filesDir):
    fileList = []
    allFiles = os.listdir(filesDir)
    for file in allFiles:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.nd2':
            fileList.append(file)
    
    return fileList

def check_fileList(fileList, filesDir):
    """Make sure the directory has ND2 files exists"""
    if not fileList: # if its empty
        if filesDir == '.':
            filesDir = os.getcwd()
        print(f"*Error: Looks like this directory doesn't have any '.nd2' files... double check your path(type -h for help)\n\t'{filesDir}'")
        sys.exit(1) # Quit


def gen_dir_paths(filesDir):
    fullDrugDirPaths = [] # make an empty list to put the generated directory paths into
    # For each drug directory in the list, join the paths and add it to the empty list
    for drugDir in DRUG_DIRS: # I made DRUG_DIRS into a constant now, so no need to supply to function
        for doseDir in DOSE_DIRS:
            currDir = os.path.join(filesDir, drugDir, doseDir)
            fullDrugDirPaths.append(currDir)
            
    return fullDrugDirPaths


def make_dirs(fullDrugDirPaths):
    for path in fullDrugDirPaths:
        try:
            # chng to 'exist_ok=False' if you don't want to allow overwriting
            os.makedirs(path, exist_ok=True) 
            #print(f'Created directory: {path}')
        except FileExistsError: # won't ever get an exception if 'exist_ok=True'
            print(f'*Error: This directory already exists. Have you already run this script before? (type -h for help)\n---> "{path}"')


def get_new_filenames(fileList):
    # file names in a list of tuples (old name, new name)
    oldNewFilenameList = []
    for oldFilename in fileList:
        try: # Some sanity checks
            r = re.search(REGEXP,oldFilename)
            newFilename = f'{r.group(1)}_Well{r.group(2)}_Channel_{r.group(3)}nm_{r.group(4)}nm_{r.group(5)}nm_{r.group(6)}nm_{r.group(7)}.{r.group(8)}'
            oldNewFilenameList.append((oldFilename, newFilename))
        except AttributeError:
            print(f'Looks like this .nd2 file as a weird naming scheme. Please fix or remove and try again (type -h for help). \n\t"{oldFilename}"')
            sys.exit(1) # QUIT

    return oldNewFilenameList


def gen_fileDestList(filesDir, fileList):
    fileDestList = []

    for file in fileList: # original file names in a list
        try: # Some sanity checks
            r = re.search(REGEXP,file)
        except AttributeError:
            print(f'Looks like this .nd2 file as a weird naming scheme. Please fix or remove and try again.(type -h for help)\n\t"{oldFilename}"')
            sys.exit(1) # QUIT

        for drug, doseDict in DRUG_DICT.items():
            for dose, wells in doseDict.items():
                if r.group(2) in wells:
                    destPath = os.path.join(filesDir, drug, dose) # destination path

                    # I am going to pair the file and destination path into a tuple using the extra parentheses ()
                    fileDestList.append((file, destPath))
    
    return fileDestList


def gen_moveList(fileDestList, oldNewFilenameList):
    moveList = [] # a list of tuples with (originalFullFilePath, renamedNewFilePath)

    for (file, destPath) in fileDestList:
        for (oldFile, newFile) in oldNewFilenameList:
            if file == oldFile:
                oldFilePath = os.path.join(filesDir, oldFile)
                newFilePath = os.path.join(destPath, newFile)

                moveList.append((oldFilePath, newFilePath))

    return moveList


def move_files(moveList):
    for (source, destination) in moveList:
        shutil.move(source, destination)
        print(f'Moved: "{source}"\n---> "{destination}"')


def parse_input():
    """Use argparse to handle user input for program"""
    # Create a parser object
    parser = argparse.ArgumentParser(
        prog='organize_nd2.py',
        
        formatter_class=argparse.RawDescriptionHelpFormatter,
        
        description="""Script to organize high throughput images into folders
        according to drugs and doses. It will also rename files with spaces and
        commas in the process. File names must have this specific naming scheme 
        for it to work.

        For example:
            'grn_d6_24hr_posttx_WellA01_Channel405 nm,488 nm,561 nm,640 nm_Seq0024.nd2'
            'grn_d6_24hr_posttx_WellG01_Channel405 nm,488 nm,561 nm,640 nm_Seq0144.nd2'
            'grn_d6_24hr_posttx_WellM03_Channel405 nm,488 nm,561 nm,640 nm_Seq0290.nd2'
        """)

    parser.add_argument('filesDir', help="Full path to files directory", nargs='?', default='.')

    parser.add_argument("-v", "--version", action="version",
                        version=textwrap.dedent("""\
        %(prog)s
        -----------------------   
        Version:    0.1 
        Updated:    12/20/2018
        By:         Prech Brian Uapinyoying   
        Website:    https://github.com/puapinyoying"""))

    args = parser.parse_args()
    
    return args


#############
#### Run ####
#############

if __name__ == "__main__":
    
    ### Step 1. Parse the user input directory and check if it exists
    args = parse_input()
    filesDir = args.filesDir
    check_folder_exist(filesDir) # if invalid path, quit


    ### Step 2. Get a list of only the '.nd2' files from the directory
    fileList = get_nd2_fileList(filesDir)
    check_fileList(fileList, filesDir) # if no '.nd2' files, quit

    ### Step 3. Make the directories
    fullDrugDirPaths = gen_dir_paths(filesDir)
    make_dirs(fullDrugDirPaths)

    ### Step 4. Generate the move list (source, destination)
    oldNewFilenameList = get_new_filenames(fileList)
    fileDestList = gen_fileDestList(filesDir, fileList)
    moveList = gen_moveList(fileDestList, oldNewFilenameList) 
    
    ### Step 5. Finally move the files
    move_files(moveList)