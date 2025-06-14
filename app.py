from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    def summarize():
     summary = ''
    if request.method == 'POST':
        input_text = request.form['input_text']
        summary = summarize_text(input_text)
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
