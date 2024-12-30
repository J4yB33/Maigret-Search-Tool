### Maigret Application Script

### `maigret_app.py`

```python
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
```

---

### README.md for GitHub

```markdown
# Maigret Web Application

A Flask-based web interface for performing OSINT username searches using [Maigret](https://github.com/soxoj/maigret).

This application allows users to search for online accounts associated with a username and view the results directly in their browser.

## Features

- **Simple Web Interface**: Input a username and receive results in real-time.
- **Real-Time Streaming**: See Maigret's output as it runs.
- **Proxy Support**: Configured to use a SOCKS5 proxy (`127.0.0.1:9050`).
- **Accessible**: Runs on all interfaces, making it accessible within the network.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/maigret-webapp.git
    cd maigret-webapp
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install flask
    pip install maigret
    ```

4. **Ensure Maigret is Installed**:
    - Install Maigret globally or within the virtual environment:
      ```bash
      pip install maigret
      ```

5. **Start the Flask App**:
    ```bash
    python maigret_app.py
    ```

6. **Access the Web Interface**:
    - Open your browser and navigate to `http://<server-ip>:5000`.

## Usage

1. Enter a username in the input box on the webpage.
2. Click "Search".
3. The results will be displayed in real-time in the results section.

## Example Output

Results will appear similar to the following:

```
Running Maigret for username: 0999ad
[+] Twitch: https://www.twitch.tv/0999ad
[+] TikTok: https://www.tiktok.com/@0999ad
...
```

## Notes

- This application uses a development server and should not be used in production as-is. Consider deploying it using a WSGI server like Gunicorn or uWSGI.
- Ensure your proxy (e.g., Tor) is running if you want to use SOCKS5.

## Contributing

Contributions are welcome! Please fork this repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```

---

### Key Files

1. **`maigret_app.py`**: The main Flask application script.
2. **`README.md`**: Documentation for the project to be added to GitHub.
3. **Webpage Interface**: This is embedded within the `index` route of the Flask app.
