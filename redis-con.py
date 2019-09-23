#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from flask import Flask, jsonify, request
# redis自定义的一些操作链接，，strictredisy严格意义链接
# r = redis.Redis(host='localhost', port=6379, db=0, password='pass')
# r.set('key', 'value')

app = Flask(__name__)

@app.route("/call")
def call():
    dic = {'test': {'age': 23, 'name': 'test'}, 'test2': {'age': 12, 'name': 'test2'}}
    if request.method == 'GET':
        age = request.args['age']
        name = request.args['name']
        return jsonify(dic.get(name))
    elif request.method == 'POST':
        # get。就是redis操作
        age = request.form.get('age', '')
        name = request.form.get('name', '')
        return jsonify(dic.get(name))



if __name__ == '__main__':
    app.run(debug=True)