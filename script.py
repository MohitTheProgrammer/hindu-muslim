import io
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm


namesSet = set()


allowedBooths = {
  40, 41, 42, 43, 44, 45, 46, 50, 52, 53, 54, 55, 56, 57, 58, 59,
  68, 69, 70, 82, 85, 86, 87, 88, 89, 93, 99, 102, 103, 104, 105,
  106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
  119, 120, 121, 122, 123, 124, 130, 131, 132, 133, 134, 135, 136,
  137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149,
  150, 151, 152, 153, 154, 156, 157, 158, 159, 160, 161, 162, 163,
  164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176,
  177, 178
}

with open('names.txt') as names_file:
    for line in names_file:
        namesSet.add(line.strip().lower())




def pdfToImages(path):
    pages = convert_from_path(path, 250)
    images = []
    for count, page in enumerate(pages):
        if count > 1:
            images.append(page)
    return images

def imageToText(image):
    
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(thresh)
    return text

def getNamesFromImageText(text):
    names = ""
    for line in io.StringIO(text):
        if(line.startswith('Name : ')):
            name = line[7:];
            names += name
    return names;

def getFileNames():
    import glob
    return(glob.glob("./files/*"))

def generateTextData():
    fileNames = getFileNames()
    for fileName in fileNames:
        realName = fileName[8:-4]
        boothNo = realName.split('-')[-2]
        if int(boothNo) not in allowedBooths:
            continue
        
        inputFilePath = 'files/' + realName + '.pdf'
        
        images = pdfToImages(inputFilePath)
        print('PDF fetched with', len(images), 'pages.')
        
        with open('output/' + realName + '.txt', 'a') as file:
            for image in tqdm(images, desc=f'Writing {realName}', unit='page'):
                text = imageToText(image)
                names = getNamesFromImageText(text)
                file.write(names)
        
        printCounts(realName, boothNo)

    
def printCounts(realName, boothNo):
    
    muslimCount = 0;
    hinduCount = 0;
    muslims = ""
    with open(f'output/{realName}.txt') as topo_file:
        for line in topo_file:
            name = line.strip().split(' ')[0]
            # for name in names:
            if name.lower() in namesSet:
                muslims += name + '\n'
                muslimCount+= 1
            else:
                hinduCount += 1
                
    statement = f'Booth No: {boothNo} Total Muslim: {muslimCount}'
    
    with open('report.txt', 'a') as file:
        file.write(statement + '\n')

    print(statement)


generateTextData()
# printCounts()