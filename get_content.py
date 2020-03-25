import os

def get_content(path):
    '''
    get the title, author and text content of the novel
    '''
    content = ''
    with open(path, "r", encoding = "utf8") as input_data:
        for line in input_data:
            if 'Title:' in line.strip():
                title = line.split(':')[1]
#                 print(line.split(':')[1])
            elif 'Author:' in line.strip():
                author = line.split(':')[1]
#                 print(line.split(':')[1])
                break

        # Skips text before the beginning of the novel:
        # *** START OF THE PROJECT GUTENBERG EBOOK, TITLE_OF_NOVEL ***
        for line in input_data:
            if 'START OF THE PROJECT GUTENBERG EBOOK' in line.strip():
                break
        # Reads text until the end of the novel:
        # *** END OF THE PROJECT GUTENBERG EBOOK, TITLE_OF_NOVEL ***
        for line in input_data:
            if 'END OF THE PROJECT GUTENBERG EBOOK' in line.strip():
                break
            content += line

    return title, author, content