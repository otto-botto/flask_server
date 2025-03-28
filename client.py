import base64
from http.client import responses
import os
import requests
import json

def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path)
        return file_size
    except FileNotFoundError:
        return None
def get_file_path():
    path = input("Enter absolute path: ")
    if (os.path.isfile(path) == False):
        path = input("Path does not exist or not a file. Enter absolute path: ")
    return path

def collect_info():
    last = input("Enter author's last name: ").lower()
    first = input("Enter author's first name: ").lower()
    title = input("Enter title, spaces are _: ").lower()

    # accept only digits from 1 to 5
    while True:
        try:
            genreNum = int(input("Select genre (enter digit): [1] FICTION [2] NONFICTION [3] MYSTERY [4] SCIFI [5] CHILDREN: "))
            if 1<= genreNum <= 5:
                break
            else:
                print("Invalid input. Please select a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please select a number.")

    path = input("Enter absolute path: ")
    if(os.path.isfile(path) == False):
        path = input("Path does not exist or not a file. Enter absolute path: ")

    size = get_file_size(path)
    # accept only digits from 1 to 3
    while True:
        try:
            formatNum = int(input("Select file type (enter digit): [1] txt [2] pdf [3] epub: "))
            if 1<= formatNum <= 3:
                break
            else:
                print("Invalid input. Please select a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please select a number.")
    # comment out response for testing
    response = send_post_request(path, last, first, title, genreNum, size, formatNum)
    # return for testing
    # return [path, first, last, title, genreNum, formatNum]

    return response
def send_post_request(path, last, first, title, genreNum, size, formatNum):
    format = ""
    genre = ""

    # set genre
    match genreNum:
        case 1:
            genre = "FICTION"
        case 2:
            genre = "NONFICTION"
        case 3:
            genre = "MYSTERY"
        case 4:
            genre = "SCIFI"
        case 5:
            genre = "CHILDREN"

    # set file format
    match formatNum:
        case 1:
            format = "txt"
        case 2:
            format = "pdf"
        case 3:
            format = "epub"

    with open(path, "rb") as f:
        bytes = f.read()
    encoded = base64.b64encode(bytes).decode('utf-8')


    return requests.post("http://localhost:5525/add", json={
        "last": last,
        "first": first,
        "title": title,
        "genre": genre,
        "format": format,
        "size": size,
        "file": encoded
    })

def list_files():
    request = requests.get("http://localhost:5525/list")
    return request

def main():
    request = requests.get("http://localhost:5525/welcome")
    if request.status_code == 200:
        print("""Welcome to the files server. You have successfully connected.
              On this server, you can store book files and retrieve them by author or genre.""")
    print("Type a command \n"
          "[add] to add a file\n"
          "[list] to list all files\n"
          "[logout] to exit server:\n"
          "[search] to search titles:\n"
          "[stats] to see server statistics:\n"
          "[count] to see word count and read time:\n"
          ">>> ")


    while(True):
        command = input("Enter command: ")

        if command == "logout":
            answer = input("Are you sure you want to exit completely out of the server? [y] for yes [n] for no: ")
            if answer == "y":
                print("You have successfully logged out. Goodbye.")
                break
            else:
                continue
        try:
            if command == "add":
                print("Adding a title takes about a minute for files within a few GB.")
                response = collect_info()
                if response.status_code == 200:
                    print(response.content.decode('ascii'))
                    continue
            elif command == "list":
                response = requests.get("http://localhost:5525/list")
                if response.status_code == 200:
                    print("Listing all files: \n")
                    list = response.content
                    print(list.decode('ascii'))
                    continue
            elif command == "count":
                print("To find word count and reading time, provide the file's path:")
                path = get_file_path()
                response = requests.post("http://localhost:5525/count", json={"path": path})
                if response.status_code == 200:
                    stats = response.content.decode('ascii')
                    print(stats)
                    continue

            elif command == "stats":
                print("The server will show you the number of books saved and the size of the server:")
                response = requests.get("http://localhost:5525/stats")
                if response.status_code == 200:
                    stats = response.content.decode('ascii')
                    print(stats)
                    continue

            elif command == "search":
                print("You can search titles by author's last name:")
                name = input("Enter last name: ").lower()
                response = requests.post("http://localhost:5525/search", json={"item": name})
                if response.status_code == 200:
                    titles = json.loads(response.content)
                    print(f"All titles by {name} are: {titles}")
                    continue

            elif command == "sort":
                print("You can sort titles alphabetically: ")

                response = requests.post("http://localhost:5525/sort", json={"type": "ALPHA"})
                if response.status_code == 200:
                    titles = json.loads(response.content)
                    print(titles)
                    continue


        except ValueError:
            print("Command not recognized.\n")



if __name__ == '__main__':
    main()