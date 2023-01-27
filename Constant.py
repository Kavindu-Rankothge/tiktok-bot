# gets list of all lines in file
with open('constants.txt', 'r') as file:
    lines = file.read().splitlines()

# gets the constant next to the id text
def find_constant(lines, id):
    index = -1
    for line in lines:
        index = line.find(id)
        if index != -1:
            constant = line[index+len(id)+1:]
            return constant
    raise Exception('Constant not found')

# constants declared
CLIENT = find_constant(lines, 'client')
SECRET = find_constant(lines, 'secret')
USER = find_constant(lines, 'user')
PASSWORD = find_constant(lines, 'password')
SUBREDDIT = find_constant(lines, 'subreddit')
BACKGROUND = find_constant(lines, 'background')
COMMENT_NUM = int(find_constant(lines, 'comment'))
TIKTOK_RATIO = float(find_constant(lines, 'tiktokRatio'))