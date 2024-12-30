from flask import Flask, render_template, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_maigret', methods=['GET'])
def run_maigret():
    username = request.args.get('username')
    if not username:
        return "Error: No username provided.", 400

    output_dir = f"output/{username}"
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Run Maigret with -a -HP options
        command = [
            "maigret", username,
            "--timeout", "30",
            "--retries", "3",
            "-a", "-HP",
            "--folderoutput", output_dir  # Correct argument for specifying output folder
        ]
        subprocess.run(command, check=True)

        # Paths to the generated files
        html_report = os.path.join(output_dir, f"{username}.html")
        pdf_report = os.path.join(output_dir, f"{username}.pdf")

        # Ensure files exist
        if not os.path.exists(html_report) or not os.path.exists(pdf_report):
            return f"Error: Reports for {username} not found.", 500

        return {
            "html_report": f"/download?file={html_report}",
            "pdf_report": f"/download?file={pdf_report}",
            "message": f"Reports for {username} generated successfully."
        }
    except subprocess.CalledProcessError as e:
        return f"Error running Maigret: {e}", 500

@app.route('/download')
def download():
    file_path = request.args.get('file')
    if not file_path or not os.path.exists(file_path):
        return "Error: File not found.", 404
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
