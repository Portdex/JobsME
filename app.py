from flask import Flask,jsonify
from flask_mysqldb import MySQL
from functions import connection_db
host,user,password,database = connection_db()

app = Flask(__name__)
app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = database
mysql = MySQL(app)


@app.route('/',methods=['GET'])
def home():
    return "Api V1"

@app.route('/api/v1/jobs/',methods=['GET'])
def jobs():
    mysql = MySQL(app)
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM jobs')
    all_data = all_data.fetchall()
    all_jobs = [list(row) for row in all_data]
    cursor.close()    
    return jsonify(all_jobs)

if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0')

