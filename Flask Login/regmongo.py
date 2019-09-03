from flask import Flask, render_template, jsonify, request, redirect,abort
import pymongo

x = pymongo.MongoClient('mongodb://localhost:27017')
db = x['signup']
col = db['login']


app=Flask(__name__)

@app.route('/')
def beranda():
    return render_template('regmong.html')

@app.route('/data', methods=['GET'])
def data():
    request.method == 'GET'
    data = list(col.find())
    listkey=[]
    for loop in range(len(data)):
        for key in data[loop].keys():
            if key == '_id':
                listkey.append(key)
                listkey.pop(-1)
            else:
                listkey.append(key)
    keys = sorted(list(set(listkey)))

    a = [tuple(item.values()) for item in data]
    vals = []
    for item in range(len(a)):
        vals.append(a[item][1:])

    dicts = [{key:val for key,val in zip(keys,vals[item])} for item in range(len(vals))]
    return jsonify(dicts)

@app.route('/signup', methods = ['POST'])
def signup():
    request.method == 'POST'
    # body = request.json
    body = request.form
    hasil = list(col.find({"email":body['email']}))
    if hasil == []:
        data = {"email":body['email'],"password":body['password']}
        col.insert_one(data)
        return redirect('/') 
    else:
        return render_template('lready.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        body = request.form
        hasil = list(col.find({"email":body['email']}))
        if hasil == []:
            return render_template('wgemail.html')
        else:
            hasil = list(col.find({"email":body['email'],"password":body['password']}))
            if hasil == [] :
                return render_template('wgpass.html')
            else :
                return render_template('lgnsuccess.html')

@app.route('/data/<string:_id>')
def dataid(_id):
    if _id.isdigit() and int(_id)>0 :
        data = list(col.find())
        listkey=[]
        for loop in range(len(data)):
            for key in data[loop].keys():
                if key == '_id':
                    listkey.append(key)
                    listkey.pop(-1)
                else:
                    listkey.append(key)
        keys = sorted(list(set(listkey)))

        a = [tuple(item.values()) for item in data]
        vals = []
        for item in range(len(a)):
            vals.append(a[item][1:])

        dicts = [{key:val for key,val in zip(keys,vals[item])} for item in range(len(vals))]
        if int(_id) <= len(dicts):
            dictsid = dicts[int(_id)-1]
            return jsonify(dictsid)
        else:
            return abort(404)
    else:
        return jsonify({'status' : 'harap masukkan angka!'})

if __name__ == '__main__':
    app.run(
        debug=True,
        host='localhost',
        port=1235
        )