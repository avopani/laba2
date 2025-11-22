from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def hello():
    student_name = os.getenv('STUDENT_NAME', 'Девопсов Олег')
    return render_template('index.html', student_name=student_name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
