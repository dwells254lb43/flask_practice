from flask import Flask, Markup, render_template, request, jsonify
import sqlite3

conn = sqlite3.connect(":memory:", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE benfords_law
             (data_set_name text, one number, two number, three number, four number, five number, six number, seven number, eight number, nine number, UNIQUE(data_set_name))''')

# c.execute('INSERT INTO benfords_law VALUES (?,?,?,?,?,?,?,?,?,?)', ("test", 1, 1, 1, 1, 1, 1, 1, 1, 1))
conn.commit()
app = Flask(__name__)

@app.route('/')
def bar():
    return render_template('chart.html', title='Benford\'s Law')

@app.route('/charts', methods=(['GET', 'POST']))
def dbInsert():
    if request.method == 'POST':
        c = conn.cursor()
        req_data = request.get_json()
        name = req_data['name']
        values = tuple(req_data['values'])
        data = (name, *values[0:])
        try:
            c.execute('INSERT INTO benfords_law VALUES (?,?,?,?,?,?,?,?,?,?)', data)
        except:
            print('IGNORED, DUPLICATE FILE NAME');
        conn.commit()
        return jsonify(('success'))
    
    elif request.method == 'GET':
        c = conn.cursor()
        returnData = []
        for row in c.execute('SELECT * FROM benfords_law'):
            returnData.append(row)
        return jsonify(data=returnData)


 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0')