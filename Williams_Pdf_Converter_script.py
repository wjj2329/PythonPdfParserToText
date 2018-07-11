from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import string
import re

# Open a PDF file.
fp = open('ldc_user_manual.pdf', 'rb')

# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)

# Create a PDF document object that stores the document structure.
# Password for initialization as 2nd parameter
document = PDFDocument(parser)

# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()

# Create a PDF device object.
device = PDFDevice(rsrcmgr)

# BEGIN LAYOUT ANALYSIS
# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)

def parse_obj(lt_objs, pagenumber, myfile,buffer, begin_loc=None):
    # loop over the object list
    for obj in lt_objs:
        if hasattr(obj, "get_text") and isinstance(obj, pdfminer.layout.LTAnno) or isinstance(obj, pdfminer.layout.LTChar):
            #print obj
            if obj.get_text()==" " or obj.get_text()==":" or obj.get_text()=="!" or obj.get_text()==".":
                if begin_loc==None:
                    continue
                location_end = obj.bbox,
                result= buffer+" "+str(pagenumber)+" "+str(begin_loc[0][0])+ " "+str(begin_loc[0][1])+ " "+str(location_end[0][2])+ " "+str(location_end[0][3])+ " "
                result=result.encode('utf-8')               
                myfile.write(result)
                begin_loc=None
                buffer=""
            elif obj.get_text().isupper() and len(buffer)>0 and not buffer[-1].isupper():
                if begin_loc==None:
                    #print "my buffer is  "+buffer
                    continue
                location_end = obj.bbox,
                result= buffer+" "+str(pagenumber)+" "+str(begin_loc[0][0])+ " "+str(begin_loc[0][1])+ " "+str(location_end[0][2])+ " "+str(location_end[0][3])+ " "
                result=result.encode('utf-8')
                myfile.write(result)
                begin_loc=None
                buffer=""
                buffer+=obj.get_text()
            elif obj.get_text().isdigit()and len(buffer)>0 and buffer[-1].isalpha():
                if begin_loc==None:
                    #print "my buffer is  "+buffer
                    continue
                location_end = obj.bbox,
                result= buffer+" "+str(pagenumber)+" "+str(begin_loc[0][0])+ " "+str(begin_loc[0][1])+ " "+str(location_end[0][2])+ " "+str(location_end[0][3])+ " "
                result=result.encode('utf-8')                
                myfile.write(result)
                begin_loc=None                
                buffer=""
                buffer+=obj.get_text()
            else:
                buffer+=obj.get_text()
                if begin_loc==None and not isinstance(obj, pdfminer.layout.LTAnno):
                    begin_loc=obj.bbox,

        '''    
        if isinstance(obj, pdfminer.layout.LTTextBox) or isinstance(obj, pdfminer.layout.LTTextLineHorizontal):
            location = obj.bbox,
            print obj.get_text()
            string_arr= obj.get_text().split(" ")
            for s in string_arr:
               #print s
               s = re.sub(r'[^\w\s]','',s, re.UNICODE) 
               if s is " " or string is "":
                   continue
               #print "I push as string "+string    
               result= s+" "+str(pagenumber)+" "+str(location[0][0])+ " "+str(location[0][1])+ " "+str(location[0][2])+ " "+str(location[0][3])+ " "
               result=result.encode('utf-8')
               myfile.write(result)
               myfile.flush()
'''
        # if it's a container, recurse
        if hasattr(obj, "_objs"):
            parse_obj(obj._objs, pagenumber, myfile, buffer)

# loop over all pages in the document
pagenumber=1
filename="ldc_user_manual.txt"
myfile=open(filename, "w")
for page in PDFPage.create_pages(document):
    # read the page into a layout object
    interpreter.process_page(page)
    layout = device.get_result()
   # print layout._objs
    # extract text from this object
    parse_obj(layout._objs, pagenumber, myfile, "")
    pagenumber+=1