## Utility Functions.
## Convenience functions to be reused.
import cv2
import matplotlib.pyplot as plt 
import numpy as np
import os
import pandas as pd
from pathlib import Path

def cleanFolder(folder, recurse=False):
    """
        Given an folder, remove all its contents. The folder itself is not
        deleted
        @param folder Folder name
        @param recurse Recursive delete Yes or No
    """
    if not os.path.exists(folder):
        return
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                if recurse is True:
                    cleanFolder(file_path)
                    os.rmdir(file_path)
                continue
        except Exception as e:
            print(e)

def checkPathExists(path):
    """
    Given an full path to a directory, confirm if the it exists.
    @param path Directory path
    """
    if not os.path.exists(path):
        print(f"Cannot access path: {path}")
    else:
        print (f"Path {path} accessible")

def buildCropDiseaseCountTuple(instanceFolder):
    """
    Given a class folder, find the number of samples of that class and return
    a tuple of the form ('Crop Name', 'Class Name', 'Count')
    Note: Name of Crop and Disease is the folder name so split it .
          Need to change the logic here based on the data source . Much Pain!!
    @param instanceFolder Folder containing images of a particular class
    @return Tuple ('Crop Name', 'Class Name', 'Count')
    """
    instanceFolder = Path(instanceFolder)
    
    str_name = str(instanceFolder.name)
    str_name = str_name.replace(" leaf", "").rstrip()
    #print(str_name)
    values = str_name.split(" ", 2)
    f = instanceFolder.rglob('*')
    counts = np.unique([x.parent for x in f], return_counts=True)[1]
    if len(values) == 1:
        values = ['Coffee', values[0]]
        #values.append('healthy')
    return (values[0], values[1], counts[0].tolist())

def getClassCounts(dataFolder, classNames=None):
    '''
    Given the root data folder, return number of samples for each class (label). 
    Note the assumption here is that the images are already seperated into their respective class subfolders
    Example -
        <rootFolder>
            |_<classFolder_1>
                |_<image_1> ... <image_n>
            |_<classFolder_2>
                |_<image_1> ... <image_n>
            ...
    @param dataFolder Root Folder with labeled data
    @param classNames list of class names to find count of.
    @return Class counts as a pandas dataframe 
    '''
    dataFolder = Path(dataFolder)
    dataList = []
    # Get all the folders within the path - The list of folders are the classes.
    if classNames != None:
        instancePathList = [f for f in dataFolder.iterdir() if f.is_dir() and f.name in classNames]
    else:
        instancePathList = [f for f in dataFolder.iterdir() if f.is_dir()]
    for classPath in instancePathList:
        dataList.append(buildCropDiseaseCountTuple(classPath))

    ## Make a DataFrame
    samplesDataFrame = pd.DataFrame(dataList, columns=['Crop', 'Disease', 'numberImages'])
    return samplesDataFrame

def displayDataAsPiePlot(df, title="Categories", ax=None, verbose=False):
    """
    Generate a pie plot showing the proportion of the different classes
    of the target variable.
    @param df Pandas data frame
    @param title Title of the plot
    @param ax Axes object from matplotlib
    @param verbose If true, print the proportions for each class
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("First parameter in not a Pandas dataframe")
    proportions = []
    sz = len(df.Disease.unique())
    total = np.sum(df.numberImages)
    for c in range(sz):
        prop = df.numberImages[c]
        if verbose:
            print(f"Proportion of data in class {df.Disease[c]} is {prop} : {prop/total*100:0.2f} %")
        proportions.append(prop)

    #colors = ['#003f5c', '#58508d' , '#bc5090', '#ff6361', '#ffa600']
    colors = ['gray', '#f8af3a', '#544ED5', '#71a2a5', '#bc5090']

    if ax is None:
        fig, ax = plt.subplots()
    ax.pie(proportions, labels=df.Disease, autopct='%1.1f%%', colors=colors, textprops={'color':"black"})
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title(title, color='black')

def generateAndSaveMetaDataAsCSV(dataDir, outputDir, outputfilename, classNames=None):
    """
    Build a CSV file for the dataset
    @param dataDir Directory where the data is located
    @param outputDir Output location for the CSV file
    @param classNames list of classnames to save into csv.
    @param outputfilename Name of the CSV file
    """
    dataDir = Path(dataDir)
    outputDir = Path(outputDir)
    if not dataDir.exists():
        raise FileNotFoundError('Data Folder (1st parameter) does not exist')
    if not outputDir.exists():
        raise FileNotFoundError('Output Folder (2nd parameter) does not exist')
    metadata_tuplelist = []
    if classNames != None:
        class_list = [x for x in dataDir.iterdir() if x.name in classNames]
    else:
        class_list = [x for x in dataDir.iterdir()]
    for c, class_ in enumerate(class_list):
        print(f"Tracking {class_}")
        for f, file in enumerate(class_.glob(f"*")):
            im = cv2.imread(str(file))
            h, w, ch = im.shape
            metadata_tuplelist.append((f"{file}", class_.name, h, w, ch))
    #print(len(metadata_tuplelist))
    metadata_df = pd.DataFrame(metadata_tuplelist, columns=['FileName', 'ClassName', 'FrameHeight', 'FrameWidth', 'Channels'])
    #print(metadata_df.shape)
    metadata_df.to_csv(outputDir.joinpath(outputfilename))
    print(f'File saved to {outputDir} with {metadata_df.shape} entries')

def loadData(inputDir):
    """
    Given the dataset folder, load the CSV file, and return a tuple of
    the form (<Image_paths> <Image_class> <Image_id>)
    @param inputDir dataset directory
    @return Tuple of (images, classes, imageID)
    """
    all_images = []
    all_classes = []
    all_ids = []
    for _, p in enumerate(inputDir.glob(f"*.csv")):
        df = pd.read_csv(p)
        sz = df.shape[0]
        for i in range(sz):
            file = df.iloc[i]['FileName']
            all_classes.append(df.iloc[i]['ClassName'])
            all_images.append(file)
            all_ids.append(file.split('.')[0])
    print(len(all_images))
    all_images = np.asarray(all_images)
    all_classes = np.asarray(all_classes)
    all_ids = np.asarray(all_ids)
    return all_images, all_classes, all_ids
