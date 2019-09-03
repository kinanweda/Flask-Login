from flask import Flask, render_template, jsonify, request, redirect
import mysql.connector
from mysql.connector.errors import Error
from mysql.connector import errorcode

db = mysql.connector.connect(
    host = 'localhost',
    user = 'kinanweda',
    passwd = 'Jimbamamba22',
    database = 'signup'
)

app=Flask(__name__)

@app.route('/')
def beranda():
    return render_template('reg.html')

@app.route('/data', methods=['GET'])
def data():
    request.method == 'GET'
    used = db.cursor()
    used.execute('describe login')
    hasil = used.fetchall()
    namakolom = []
    # nama kolom
    for i in hasil:
        namakolom.append(i[0])
    # print(namakolom)
    used.execute('select * from login')
    hasil = used.fetchall()
    data = []
    for i in hasil:
        x = {
            namakolom[0]:i[0],
            namakolom[1]:i[1],
            namakolom[2]:i[2]
        }
        data.append(x)
    return jsonify(data)

@app.route('/signup', methods = ['POST'])
def signup():
    try:
        request.method == 'POST'
        # body = request.json
        body = request.form
        used = db.cursor()
        qry = 'insert into login (email, password) values(%s,%s)'
        val = (body['email'],body['password'])
        used.execute(qry, val)
        db.commit()
        return redirect('/')    
    except mysql.connector.Error:
        return render_template('already.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        body = request.form
        used = db.cursor()
        qry = 'select * from login where email = %s'
        val = (body['email'],)
        used.execute(qry,val)
        hasil = used.fetchall()
        if hasil == []:
            return render_template('wrongemail.html')
        else:
            qry = 'select * from login where email = %s and password = %s'
            val = (body['email'],body['password'])
            used.execute(qry,val)
            hasil = used.fetchall()
            if hasil == [] :
                return render_template('wrongpass.html')
            else :
                return render_template('loginsuccess.html')

@app.route('/data/<string:_id>')
def dataid(_id):
    if _id.isdigit() and int(_id)>0 :
        used = db.cursor()
        used.execute('describe login')
        hasil = used.fetchall()
        namakolom = []
        # nama kolom
        for i in hasil:
            namakolom.append(i[0])
        qry = 'select * from login where _id = %s'
        _id = (_id,)
        used.execute(qry,_id)
        hasil = used.fetchall()
        data = []
        for i in hasil:
            x = {
                namakolom[0]:i[0],
                namakolom[1]:i[1],
                namakolom[2]:i[2]
            }
            data.append(x)
        return jsonify(data)
    else:
        return jsonify({'status' : 'harap masukkan angka!'})

if __name__ == '__main__':
    app.run(
        debug=True,
        host='localhost',
        port=1234
        )