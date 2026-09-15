from flask import Flask, render_template_string, request
from werkzeug.middleware.proxy_fix import ProxyFix
import boto3

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Initialize DynamoDB resource pointing directly to the Interface Endpoint
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    endpoint_url='https://vpce-0d5107b23891af2b9-sow3v4uq.dynamodb.us-east-1.vpce.amazonaws.com'
)
table = dynamodb.Table('pgsn')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Login Page</title></head>
<body style="font-family: Arial; margin: 50px;">
    <h2>Login Portal</h2>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
    <form method="POST">
        <label>Username (Cluster):</label><br>
        <input type="text" name="username" required><br><br>
        <label>Password:</label><br>
        <input type="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            response = table.get_item(Key={'cluster': username})
            user = response.get('Item')

            if user and user.get('password') == password:
                return f"<h2>Welcome, {username}! Login successful.</h2>"
            else:
                error = "Invalid username or password."
        except Exception as e:
            error = f"Database error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
