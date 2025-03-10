from flask import Flask
from flask import request
import requests
import base64
import json

def read_stats_file(path):
    stats = []
    try:
        with open(path, 'r') as file:
            for line in file:
                number = int(line.strip())
                stats.append(number)
            stats_dict = dict([("num_books", stats[0]), ("size", stats[1])])
            return stats_dict
    except FileNotFoundError:
        print(f"Error: File stats.txt not found.")

app = Flask(__name__)
@app.route('/welcome')
def welcome():  # put application's code here
    message = """Welcome to the files server.
    You have successfully connected.
    On this server, you can store book files and retrieve them by author or genre."""
    return message

@app.route('/list', methods=['GET'])
def list_titles():
    response = requests.get("http://localhost:5526/list").content
    return response

@app.route('/add', methods=['GET', 'POST'])
def add_title():
    if request.method == 'POST':
        body_json = request.get_json()
        send_post = requests.post("http://localhost:5526/add", json=body_json)
        response = send_post.content
        return response

@app.route('/count', methods = ['GET', 'POST'])
def count_words():
    if request.method == 'POST':
        body_json = request.get_json()
        send_post = requests.post("http://localhost:5531/count", json=body_json)
        response = send_post.content
        return response
@app.route('/stats', methods = ['GET', 'POST'])
def get_stats():
    dictionary = read_stats_file("/home/lora/Microservices/stats.txt")
    # make_json = json.dumps(dictionary)
    # print(make_json)
    send_post = requests.post("http://localhost:5529/stats", json = dictionary)
    print(send_post.status_code)
    response = send_post.content
    return response


if __name__ == '__main__':
    app.run(debug =True, port = 5525)






