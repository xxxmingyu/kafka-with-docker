import json
from flask import Flask, request
from kafka import KafkaProducer
import datetime

app = Flask(__name__)

broker1 = '172.31.1.220:9092'
broker2 = '172.31.0.80:9092'
broker3 = '172.31.10.183:9092'
kafka_bootstrap_servers = [broker1, broker2, broker3]

now = datetime.datetime.now

def kafka_producer(topic, user_input):
    producer = KafkaProducer(
            bootstrap_servers = kafka_bootstrap_servers, 
            acks = 0, 
            retries = 3)

    producer.send(topic = topic, value = json.dumps({"datetime": now(),
                                                   "message": user_input}, default = str).encode('utf-8'))
    producer.flush()

@app.route('/')
def hello_page():
    return 'Hello, world!'

@app.route('/send', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        topic = request.form['topic']
        user_input = request.form['user_input']
        kafka_producer(topic, user_input)  
    return ''' 
        <form method="post" action="/send">
            <label for="Select-topic">Select topic :</label>
            <select name="topic" id="topic">
                <option value="postgrestopic">postgres (store)</option>
                <option value="sparktopic">spark (make dataframe)</option>
            </select>
            <label for="user_input">Message :</label>
            <input type="text" id="user_input" name="user_input">
            <input type="submit" value="Submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
