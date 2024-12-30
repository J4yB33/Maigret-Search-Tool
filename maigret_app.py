from flask import Flask, request, render_template, Response
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Maigret Search</title>
        </head>
        <body>
            <h1>Maigret Username Search</h1>
            <form action="/run_maigret" method="post">
                <label for="username">Enter Username:</label>
                <input type="text" id="username" name="username" required>
                <button type="submit">Search</button>
            </form>
            <h2>Results:</h2>
            <div id="results">
                <iframe id="output" style="width:100%;height:400px;"></iframe>
            </div>
        </body>
        <script>
            const form = document.querySelector('form');
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                const username = document.querySelector('#username').value;
                const iframe = document.querySelector('#output');
                iframe.src = `/run_maigret?username=${username}`;
            });
        </script>
        </html>
    '''

@app.route('/run_maigret', methods=['GET'])
def run_maigret():
    username = request.args.get('username')
    if not username:
        return "Error: No username provided.", 400

    def generate():
        yield f"Running Maigret for username: {username}<br>"
        try:
            process = subprocess.Popen(
                [
                    'maigret', username,
                    '--timeout', '30',
                    '--retries', '3',
                    '--verbose',
                    '--proxy', 'socks5://127.0.0.1:9050'
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in iter(process.stdout.readline, ''):
                yield line.replace("\n", "<br>")
            for err_line in iter(process.stderr.readline, ''):
                yield f"<span style='color: red;'>{err_line}</span><br>"
        except Exception as e:
            yield f"Error running Maigret: {e}<br>"

    return Response(generate(), mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
