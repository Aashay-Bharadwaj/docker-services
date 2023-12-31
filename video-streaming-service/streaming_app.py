from flask import Flask, render_template,render_template_string, request, redirect, stream_with_context, Response, session, url_for
import mysql.connector
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        credentials = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }

        auth_response = requests.post('http://35.224.55.194:5002/validate', data=credentials)
        if auth_response.status_code == 200:
            session['authenticated'] = True
            return redirect(url_for('list_videos'))
        else:
            return "Invalid credentials", 403

    if request.method == 'GET':
        return render_template_string('''
            <form method="post" enctype=multipart/form-data>
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Upload">
            </form>
        ''')
    credentials = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }

    auth_response = requests.post('http://35.224.55.194:5002/validate', data=credentials)
    if auth_response.status_code == 200:
        session['authenticated'] = True
        return redirect(url_for('list_videos'))
    else:
        return "Invalid credentials", 403

@app.route('/videos', methods=['GET'])
def list_videos():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    connection = mysql.connector.connect(user='root', password='password', host='mysql', database='videos')
    cursor = connection.cursor()
    cursor.execute('SELECT name, path FROM videos')
    videos = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('video_list.html', videos=videos)

@app.route('/stream/<filename>', methods=['GET'])
def stream_video(filename):
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    video_url = f"http://34.134.55.164:5003/get/{filename}"
    r = requests.get(video_url, stream=True)

    def generate():
        for chunk in r.iter_content(chunk_size=8192):
            yield chunk

    return Response(stream_with_context(generate()), content_type='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
