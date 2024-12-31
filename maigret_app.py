from flask import Flask, request, jsonify, send_from_directory, render_template
from pathlib import Path
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_maigret', methods=['GET'])
def run_maigret():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "No username provided"}), 400

    try:
        output_dir = Path(f'output/{username}')
        output_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            'maigret', username, '-a', '-HP',
            '--output', str(output_dir),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({
                "error": "Error running Maigret",
                "stderr": result.stderr,
                "stdout": result.stdout
            }), 500

        html_report = output_dir / f'report_{username}_plain.html'
        pdf_report = output_dir / f'report_{username}.pdf'

        if not html_report.exists() or not pdf_report.exists():
            return jsonify({
                "error": "Reports not generated",
                "html_report_exists": html_report.exists(),
                "pdf_report_exists": pdf_report.exists()
            }), 500

        return jsonify({
            "message": "Maigret execution successful",
            "html_report": f"/output/{username}/report_{username}_plain.html",
            "pdf_report": f"/output/{username}/report_{username}.pdf",
            "stdout": result.stdout
        })
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/output/<path:filename>')
def download_file(filename):
    return send_from_directory('output', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
