import re
import csv


def matchurl(text):
    url_regex = r'(?:https?://|www\.)(?:[-\w./?&])+(?=[.\s,\n\r\t)])'
    url_pattern = re.compile(url_regex)
    matches = url_pattern.findall(text)
    return matches

def matchTrigger(text):
    keywords = [r'step', r'step', r'demo', r'reproduce', r'usage', r'compile with', r'trigger']
    flag = 0

    # Create a regular expression that matches any of the keywords in the list
    keyword_pattern = '|'.join(keywords)
    if re.search(keyword_pattern, text, re.IGNORECASE):
        flag = 1
        return flag

    # Create regular expressions to match numeric and alphabetic lists
    number_pattern = r'(\(\d+\)|\d+\)|\d+\.)'
    letter_pattern = r'(\([a-zA-Z]\)|[a-zA-Z]\)|[a-zA-Z]\.)'

    # Split the text into lines and check each line
    lines = text.split('\n')
    for index, line in enumerate(lines):
        if re.search(number_pattern, line):
            flag = check_sequential(lines[index:], number_pattern)
        elif re.search(letter_pattern, line):
            flag = check_sequential(lines[index:], letter_pattern)

        if flag:
            break

    return flag

def check_sequential(lines, pattern):
    current = 0
    for line in lines:
        match = re.search(pattern, line)
        if match:
            if pattern == r'(\(\d+\)|\d+\)|\d+\.)':
                number = int(re.findall(r'\d+', match.group())[0])
                if number == current + 1:
                    current += 1
                elif number > current + 1:
                    return 0
            elif pattern == r'(\([a-zA-Z]\)|[a-zA-Z]\)|[a-zA-Z]\.)':
                letter = re.findall(r'[a-zA-Z]', match.group())[0].lower()
                if ord(letter) == ord('a') + current:
                    current += 1
                elif ord(letter) > ord('a') + current:
                    return 0
    return 1 if current > 0 else 0

def matchRecord(text):
    flag = 0
    # Updated pattern1, now checks if '$' and './' are on the same line
    pattern1 = r'@.*\./|:\.*>|\$.*\./'
    pattern2 = r'\[\+\]|\[\-\]|\[\*\]'  # Checks if '[+]', '[-]', or '[*]' exist in the text

    # Check if the entire text contains '[+]', '[-]', or '[*]'
    if re.search(pattern2, text):
        # Check each line to see if '@' and './', ':\' and '>', or '$' and './' are on the same line
        for line in text.split('\n'):
            if re.search(pattern1, line):
                flag = 1
                break

    return flag

def extract(filepath_list):
    #print(filepath_list)
    for filepath in filepath_list:
        #print(filepath)
        with open(filepath, 'r', encoding='utf-8') as file:
            file_content = file.read()
        matchlist = matchurl(file_content)
        Triggerflag = matchTrigger(file_content)
        Recordflag = matchRecord(file_content)

        with open('All.csv','a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([filepath,Triggerflag,Recordflag,matchlist])


