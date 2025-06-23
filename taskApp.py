from flask import Flask,render_template,redirect,request
import sqlite3

connection = sqlite3.connect("task.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    done BOOLEAN           
)""")
connection.commit()

connection.close()

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])

def getAllTask(): 
    if request.method == "POST":
        task = request.form["task"]
        with sqlite3.connect("task.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task,done) VALUES(?,?)",(task,0))
        return redirect("/")
    
    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        print(tasks)
    return render_template("index.html",tasks = tasks)
    
@app.route("/delete/<int:id>")
def deleteTask(id):
    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?",(id,))
    return redirect("/")

@app.route("/done/<int:id>",methods=["POST"])
def done(id):
    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT done FROM tasks WHERE id = ?",(id,))
        current_done = cursor.fetchone()
     
        if(current_done[0] == 0):
            d = 1
        else:
            d=0
        cursor.execute(f"UPDATE tasks SET done = {d} WHERE id = ?",(id,))

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0",port=5000)

# py taskApp.py