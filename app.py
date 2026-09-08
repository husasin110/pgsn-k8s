from flask import Flask, request, render_template_string
import boto3
from boto3.dynamodb.conditions import key

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')

HTML_TEMPLATE = '''
<!doctype html>
<title>Login Application</title>
<div style="font-family: Arial; margin: 50px auto; width: 300px;">
  <h2>Login</h2>
  {% if message %}
    <p style="color: red;">{{ message }}</p>
  {% endif %}
  <form method="post">
    <label>Username:</label><br>
    <input type="text" name="username" required style="width: 100%; margin-bottom: 10px;"><br>
    <label>Password:</label><br>
    <input type="password" name="password" required style="width: 100%; margin-bottom: 10px;"><br>
    <button type="submit" style="width: 100%; padding: 8px;">Login</button>
  </form>
</div>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        response = table.get_item(Key={'username': username})
        user = response.get('Item')
        
        if user and user.get('password') == password:
            return f"<h2>Welcome, {username}! Login successful.</h2>"
        else:
            message = "Invalid username or password."
            
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
