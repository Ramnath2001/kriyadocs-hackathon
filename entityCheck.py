import fitz
filename = 'test1.pdf'
doc = fitz.open(filename)
page = 2
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
                            print(k) 

