from urllib import request
import pyrebase
import fitz
from flask import *
import json

firebaseConfig = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": "",
  "measurementId": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)

storage = firebase.storage()

# storage.child("pdfs/test.pdf").put("hftest2.pdf")

# storage.child("pdfs/test.pdf").download("test.pdf")

def three_rules(filename, page):
    doc = fitz.open(filename)
    width = doc[page].rect.width
    height = doc[page].rect.height
    blocks = doc[page].get_text("blocks",sort=True)
    hyo = 50
    hy1 = 100
    index = []
    empty_header = 0
    empty_footer = 0
    rect = fitz.Rect(0, 0, width, 50)  
    header_text = doc[page].get_textbox(rect)  
    rect2 = fitz.Rect(0, height-50, width, height)
    footer_text = doc[page].get_textbox(rect2)

    for i in range(0, len(blocks)):
        if blocks[i][1] <= 40 and blocks[i][4][1:6] == "image":
            header_text = header_text + "image"
            hyo = blocks[i][3]
        if (blocks[i][3] >= height-50 and blocks[i][3] <= height) and blocks[i][4][1:6] == "image":
            footer_text = footer_text + "image"

    header_text = "".join(header_text.split())
    footer_text = "".join(footer_text.split())
    if(header_text == ""): 
        empty_header = 1
    if(footer_text == ""): 
        empty_footer = 1

    for i in range(0, len(blocks)):
        if blocks[i][1] <= hyo and blocks[i][3] <= hy1 and (not empty_header):
            index.append(i)
        if blocks[i][3] >= height - 40 and blocks[i][3] <= height and (not empty_footer):
            index.append(i)
    
    content = ""
    image_count = 0
    for i in range(len(blocks)):
        if i not in index:
            line = blocks[i][4]
            if(line[1:6] != "image"):
                content += line
            else:
                image_count += 1
    # print(image_count)
    content_list = content.split('\n')
    # print(content_list)
    min_line_count = 0
    blank_page = 0
    for x in content_list:
        l = x.split(" ")
        if len(l) > 1:
            min_line_count += 1
        if min_line_count >= 5:
            break
    blank_cnt = 0
    for x in content_list:
        if x == "":
            blank_cnt += 1
    if (blank_cnt == len(content_list)) and (image_count == 0) and (min_line_count == 0):
        blank_page = 1
    #blank_page-0 or 1, empty_header-0 or 1, empty_footer-0 or 1, min_line_count-max value 5
    return (empty_header, empty_footer, blank_page, min_line_count)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def basis():
  str1 = """outputformat = {
    "missing_font": {
        "page_i_invalid_fonts": ["list contains names of all the invalid fonts used in page i."]
    },
    "min_no_of_lines": {
        "page": ["list containing all the page numbers where there are less than 5 lines of text."]
    },
    "missing_header": {
        "page": ["list containing all the page numbers where the page header is missing"]
    },
    "missing_footer": {
        "page": ["list containing all the page numbers where the page footer is missing"]
    },
    "blank_pages": {
        "page": ["list containing the page numbers of all blank pages"]
    },
    "missing_entity":{
        "page": ["list containing the page numbers where a entity is missing"]
    }
  }"""
  if request.method == "POST":
    upload  = request.files['upload']
    storage.child("pdfs/test.pdf").put(upload)
    storage.child("pdfs/test.pdf").download("/","test.pdf")
    filename = "test.pdf"
    try:
      doc = fitz.open(filename)
      res = {}
      for page in range(doc.page_count):
          (header_status, footer_status, blank_page_status, min_line_count) = three_rules(filename, page)
          # print(header_status)
          # print(footer_status)
          # print(blank_page_status)
          # print(min_line_count)
          if header_status == 1:
              if "missing_header" not in res:
                  res["missing_header"] = {"page": [page+1]}
              else:
                  res["missing_header"]["page"].append(page+1)

          if footer_status == 1:
              if "missing_footer" not in res:
                  res["missing_footer"] = {"page": [page+1]}
              else:
                  res["missing_footer"]["page"].append(page+1)

          if blank_page_status == 1:
              if "blank_pages" not in res:
                  res["blank_pages"] = {"page": [page+1]}
              else:
                  res["blank_pages"]["page"].append(page+1)

          if (min_line_count != 5 and blank_page_status != 1) or (min_line_count == 0 and blank_page_status == 0):
              if "min_no_of_lines" not in res:
                  res["min_no_of_lines"] = {"page": [page+1]}
              else:
                  res["min_no_of_lines"]["page"].append(page+1)
        
      for i in range(len(doc)):
        fontlist = doc.get_page_fonts(i)
        for font in fontlist:
            if (font[3].lower().find("arial") == -1 and font[3].lower().find("symbol") == -1 and font[3].lower().find("times new roman") == -1
            and font[3].lower().find("frutigerltpro") == -1 and font[3].lower().find("frutigerltstd") == -1 and font[3].lower().find("classicalgaramond") == -1
            and font[3].lower().find("timesnewroman") == -1 and font[3].lower().find("times-roman") == -1):
                l = font[3].split("+")
                invalid_font = ""
                if len(l) == 2:
                    invalid_font = l[1]
                else:
                    invalid_font = l[0]
                if "missing_font" not in res:
                    key = "page_"+str(i+1)+"_invalid_fonts"
                    res["missing_font"] = {key:[invalid_font]}
                else:
                    key = "page_"+str(i+1)+"_invalid_fonts"
                    if key not in res["missing_font"]:
                        res["missing_font"][key] = [invalid_font]
                    else:
                          res["missing_font"][key].append(invalid_font)
      # print(res)
      for page in range(len(doc)):
        blocks = doc[page].get_text("dict",sort=True)["blocks"]
        for i in range(len(blocks)):
            if "lines" in blocks[i]:
                for i in blocks[i]["lines"]:
                    for j in i["spans"]:
                        text = str(j["text"])
                        l = [i for i in text]
                        # text = text.split("")
                        # print(j["font"] + " "+ str(l))
                        fontname = str(j["font"])
                        flag = 0
                        if fontname.lower().find("arial") != -1 and fontname.lower() != "arialmt":
                            flag = 1
                            font = fitz.Font("Arial")
                        elif fontname.lower().find("times new roman") != -1 or fontname.lower().find("timesnewroman") != -1 or fontname.lower().find("times-roman") != -1:
                            flag = 1
                            font = fitz.Font("times-roman")
                        elif fontname.lower().find("classicalgaramond") != -1:
                            flag = 1
                            font = fitz.Font(fontfile = "ClassicalGaramondBT.ttf")
                        elif fontname.lower().find("frutigerltpro") != -1:
                            flag = 1
                            font = fitz.Font(fontfile = "FrutigerLTPro.otf")
                        elif fontname.lower().find("frutigerltstd") != -1:
                            flag = 1
                            font = fitz.Font(fontfile = "FrutigerLTStd.otf")
                        elif fontname.lower().find("symbol") != -1:
                            flag = 1
                            font = fitz.Font("symb")
                        if flag == 1:
                            vuc = font.valid_codepoints()
                            ch = []
                            for k in vuc:
                                ch.append(chr(k))
                            for k in l:
                                if k not in ch:
                                    if "missing_entity" not in res:
                                        res["missing_entity"] = {"page": [page+1]}
                                    else:
                                        if page+1 not in res["missing_entity"]["page"]:
                                            res["missing_entity"]["page"].append(page+1)

      if res == {}:
        response = "The pdf is valid."
      else:
        response = json.dumps(res)
      return render_template('index.html', result=response, output_format=str1)
    except Exception as e:
      message = ""
      if str(e) == 'cannot open broken document':
        message = str(e) + ". Please select a pdf document. Other file extensions are considered invalid."
      elif str(e) == 'cannot open empty document':
        message = str(e) + ". Please select a pdf document"
      if message == "":
        message = str(e)
        return render_template('index.html', result=message, output_format=str1)
      else:
        return render_template('index.html', result=message, output_format=str1)
  return render_template('index.html', result="", output_format=str1)

if __name__ == "__main__":
  app.run(debug=True)
