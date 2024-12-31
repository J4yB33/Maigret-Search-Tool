from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import threading

app = Flask(__name__)

# Track scan status
scan_in_progress = False
scan_lock = threading.Lock()

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/run_maigret', methods=['GET'])
def run_maigret():
    """Run Maigret scan for a given username."""
    global scan_in_progress

    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required."}), 400

    # Prevent concurrent scans
    with scan_lock:
        if scan_in_progress:
            return jsonify({"error": "A scan is already in progress. Please wait."}), 400
        scan_in_progress = True

    output_dir = f"output/{username}"
    os.makedirs(output_dir, exist_ok=True)
    command = ["maigret", username, "-a", "-HP", "--folderoutput", output_dir]

    try:
        # Run the Maigret command
        subprocess.run(command, capture_output=True, text=True, check=True)

        html_report = f"{output_dir}/report_{username}_plain.html"
        pdf_report = f"{output_dir}/report_{username}.pdf"

        # Reset the scan flag after completion
        with scan_lock:
            scan_in_progress = False

        return jsonify({
            "message": f"Scan for {username} completed successfully.",
            "html_report": html_report,
            "pdf_report": pdf_report
        })
    except subprocess.CalledProcessError as e:
        # Reset the scan flag in case of errors
        with scan_lock:
            scan_in_progress = False
        return jsonify({"error": f"Error running Maigret: {e.stderr}"}), 500

@app.route('/view_report/<path:filename>', methods=['GET'])
def view_report(filename):
    """Serve the HTML or PDF report for viewing."""
    try:
        return send_file(filename, as_attachment=False)
    except FileNotFoundError:
        return jsonify({"error": "Report not found."}), 404

@app.route('/download_report/<path:filename>', methods=['GET'])
def download_report(filename):
    """Serve the HTML or PDF report for download."""
    try:
        return send_file(filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Report not found."}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
