FILES = [
    './extract.py',
    '../wwwroot/init/iorama.json'
    '../wwwroot/config.json'
]


ACCESS_TOKEN = input("ION Access Token: ")

for path in FILES:
    file_contents = ""
    with open(path, "r+") as f:
        file_contents = f.read()
    # print(file_contents)
    with open(path, "w") as f:
        file_contents = file_contents.replace("<ION_ACCESS_TOKEN>", ACCESS_TOKEN)
        f.write(file_contents)