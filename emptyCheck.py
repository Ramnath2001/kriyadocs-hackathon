import fitz

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


filename = 'rules.pdf'
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

print(res)