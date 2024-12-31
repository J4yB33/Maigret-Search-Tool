import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__)

# Set up logging
logging.basicConfig(
    filename="maigret_app.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger().addHandler(logging.StreamHandler())

# Directory for output files
BASE_DIR = "/home/student/maigret_env"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# State to track if a scan is running
scan_in_progress = False

@app.route("/")
def index():
    logging.info("Index page accessed.")
    return render_template("index.html")

@app.route("/run_maigret", methods=["GET"])
def run_maigret():
    global scan_in_progress
    username = request.args.get("username")
    
    if not username:
        logging.warning("No username provided.")
        return jsonify({"error": "No username provided"}), 400

    if scan_in_progress:
        logging.warning("Scan already in progress.")
        return jsonify({"error": "A scan is already in progress. Please wait."}), 400

    logging.info(f"Starting scan for username: {username}")
    scan_in_progress = True
    try:
        output_dir = os.path.join(OUTPUT_DIR, username)
        os.makedirs(output_dir, exist_ok=True)

        command = [
            "maigret", username, "-a", "-HP",
            "--folderoutput", output_dir
        ]

        process = subprocess.run(command, text=True, capture_output=True)

        if process.returncode != 0:
            logging.error(f"Maigret failed: {process.stderr}")
            scan_in_progress = False
            return jsonify({"error": f"Error running Maigret: {process.stderr}"}), 500

        logging.info(f"Scan completed successfully for username: {username}")
        html_report = f"/output/{username}/report_{username}_plain.html"
        pdf_report = f"/output/{username}/report_{username}.pdf"
        
        return jsonify({
            "message": f"Scan completed for {username}",
            "html_report": html_report,
            "pdf_report": pdf_report
        })

    except Exception as e:
        logging.exception("Unexpected error during scan.")
        scan_in_progress = False
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        scan_in_progress = False

@app.route("/output/<username>/<path:filename>")
def serve_report(username, filename):
    logging.info(f"Serving file: {filename} for username: {username}")
    user_output_dir = os.path.join(OUTPUT_DIR, username)
    return send_from_directory(user_output_dir, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
