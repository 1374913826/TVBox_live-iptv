import os
from flask import Flask, render_template

base_dir = os.getcwd()
TEMPLATES_DIR = os.path.join(base_dir, "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)

@app.route('/')
def index():
    content = ""
    if os.path.exists("live.txt"):
        with open("live.txt", 'r', encoding='utf-8') as file:
            content += file.read() + "\n\n"
    if os.path.exists("local.txt"):
        with open("local.txt", 'r', encoding='utf-8') as file:
            content += file.read() + "\n"
            
    print(content)
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4545)
```—
