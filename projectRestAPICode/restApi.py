from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def fetchResult():
    #mpValue = request.args.get('mpvalue')
    mpValue = request.form['mpvalue']
    conn = sqlite3.connect("C:/Users/nitaj/MS_work/sqlitedbFiles/TISProject.db")
    cursor = conn.cursor()
    print("opened db")
    print("mpvalue=",mpValue)
    #rows = cursor.execute("SELECT l.label FROM search_results s, label_mapping l where s.mp_id='MP1' and s.document_id=l.document_id ORDER by s.score desc").fetchall()
    rows = cursor.execute("SELECT l.label FROM search_results s, label_mapping l where s.mp_id=? and s.document_id=l.document_id ORDER by s.score desc",(mpValue,))
    #print("rows=",rows)
    value=""
    for i in rows:
        value+=i[0]
        value+="\n"
    print("value=",value)
    conn.close()
    
    return value
      
    

if __name__ == "__main__":
    app.run(debug=False)