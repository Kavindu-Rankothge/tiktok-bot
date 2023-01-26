with open('constants.txt', 'r') as file:
    lines = file.read().splitlines()

def find_constant(lines, id):
    index = -1
    for line in lines:
        index = line.find(id)
        if index != -1:
            constant = line[index+len(id)+1:]
            return constant
    raise Exception("Constant not found")


CLIENT = find_constant(lines, 'client')
SECRET = find_constant(lines, 'secret')
USER = find_constant(lines, 'user')
PASSWORD = find_constant(lines, 'password')
SUBREDDIT = find_constant(lines, 'subreddit')
BACKGROUND = find_constant(lines, 'background')
