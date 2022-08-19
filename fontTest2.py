import fitz                       # PyMuPDF

def font_validator(filename):
    doc = fitz.open(filename)
    res = {}
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
    print(res)

filename = "paytm.pdf"
font_validator(filename)
