from flask import Flask, render_template, request

app = Flask(__name__)

todo_items = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new_item = request.form.get('todo_text')
        if new_item:
            todo_items.append(new_item)
    return render_template('home.html', todo_items=todo_items)


if __name__ == "__main__":
    app.run(debug=True)
