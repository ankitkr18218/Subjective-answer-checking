import os, cv2, io
from google.cloud import vision
import pandas as pd
import matplotlib.pyplot as plt
import pandasql as ps
import glob
from os.path import split
from os.path import basename
import ntpath
import time

start_time = time.time()
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'D:\Image_Ext\qwiklabs-gcp-04-2520d417c0a1-3e1ea6f55a1c.json'
def find_lines(img):
    img=cv2.imread(img)
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    rect=cv2.getStructuringElement(cv2.MORPH_RECT, (100,1))
    lineLocations = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, rect, iterations=1)

    return lineLocations

def fnamebypath(fpath):
    first, last = ntpath.split(fpath)
    return last or ntpath.basename(first)


seg=[]
dict={}
dir_path = 'D:\Image_Ext\ezyzip (1)\**\*'
i=0
for filepath in glob.glob(dir_path, recursive=True):
    lineLocations = find_lines(filepath)
    filename = fnamebypath(filepath)
    i+=1
    df_lineLocations = pd.DataFrame(lineLocations.sum(axis=1)).reset_index()

    df_lineLocations.columns = ['rowLoc', 'LineLength']
    #add coulumn line with intail value 0
    df_lineLocations['line'] = 0
    #assigning 1 to linelength if length>100
    df_lineLocations.loc[df_lineLocations['LineLength'] > 300, 'line'] = 1
    #cumsum is done to detect the height of page till line appears.
    df_lineLocations['cumSum'] = df_lineLocations['line'].cumsum()

    query = '''
    select row_number() over (order by cumSum) as SegmentOrder
    , min(rowLoc) as SegmentStart
    , max(rowLoc) - min(rowLoc) as Height
    from df_lineLocations
    where line = 0
    --and CumSum !=0
    group by cumSum
    '''
    df_SegmentLocations  = ps.sqldf(query, locals())
    segments = []
    y = df_SegmentLocations['SegmentStart'][2]
    h = df_SegmentLocations['Height'][2]
    img = cv2.imread(filepath)
    cropped = img[y:y+h]
    seg.append([cropped])


    client = vision.ImageAnnotatorClient()
    _, encoded_image = cv2.imencode('.png', cropped)
    content = encoded_image.tobytes()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    doc_text=response.full_text_annotation.text
    #print(doc_text)
    print("--- %s seconds ---" % (time.time() - start_time))
    dict[filename]=doc_text
    if (i == 1):
        #plt.figure(figsize=(8,8))
        #plt.imshow(cropped)
        #plt.show()
        break


print("--- %s seconds ---" % (time.time() - start_time))
print(dict)
