import urllib

def read_text():
    f = open('movie_quotes.txt')
    contents = f.read()
    print contents
    f.close()
    check_profanity(contents)

def check_profanity(text):
    conn = urllib.urlopen("http://www.wdyl.com/profanity?q="+text)
    output = conn.read()
    print output
    conn.close()

read_text()
