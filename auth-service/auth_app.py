from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

USERS = {
    'user1': 'password1',
    'user2': 'password2'
}

login_form_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
</head>
<body>
    <form method="post" action="/validate">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route('/validate', methods=['POST', 'GET'])
def validate_credentials():
    if request.method == 'GET':
        # If the request is GET, render the login form template
        return render_template_string(login_form_template)

    # For POST requests, proceed with credential validation
    username = request.form.get('username')
    password = request.form.get('password')

    if username in USERS and USERS[username] == password:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'Invalid credentials'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
