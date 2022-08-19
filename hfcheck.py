import fitz

def hf(filename):
    page = 4
    doc = fitz.open(filename)
    width = doc[page].rect.width
    height = doc[page].rect.height
    rect = fitz.Rect(0, 0, width, 50)  # define your rectangle here
    header_text = doc[page].get_textbox(rect)  # get text from rectangle
    
    rect2 = fitz.Rect(0, height-50, width, height)
    footer_text = doc[page].get_textbox(rect2)  # get text from rectangle
    
    blocks = doc[page].get_text("blocks",sort=True)
    for i in range(0, len(blocks)):
        if blocks[i][1] <= 50 and blocks[i][4][1:6] == "image":
            print(3)
            header_text = header_text + "image"

    header_text = "".join(header_text.split())
    print(header_text)
    if(header_text == "" or header_text == " "): 
        print(True)

    footer_text = "".join(footer_text.split())
    print(footer_text)
    if(footer_text == ""): 
        print(True)
    print(blocks)
    # clean_text = ' '.join(text.split())
    # print(clean_text)
    # print('break')
    # print(doc[0].get_text('dict'))
    #print(doc[0].get_text('text'))

filename = 'test1_1.pdf'
hf(filename)