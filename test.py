from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
data_list = []  

@app.route('/')
def home():
    return '<p>Welcome! Go to <a href="/data">/data</a> to submit a number.</p>'

form_html = """
<!DOCTYPE html>
<html>
<head><title>Submit Number</title></head>
<body>
    <h2>Enter a Number</h2>
    <form method="POST" action="/data">
        <input type="number" name="number" required>
        <input type="submit" value="Submit">
    </form>
    <p><a href="/data/json">View submitted data (JSON)</a></p>
</body>
</html>
"""

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        try:
            number = int(request.form['number'])
            data_list.append(number)
            return f"<p>Number {number} added!</p><a href='/data'>Go back</a>"
        except ValueError:
            return "Invalid input. Please enter a valid number."
    return render_template_string(form_html)

@app.route('/data/json', methods=['GET'])
def get_json():
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)
