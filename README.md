# **Maigret Web Scanner**

This repository contains a web-based interface for the **Maigret** tool, a powerful open-source username enumeration and reconnaissance tool. With this web app, users can input a username and generate detailed **HTML** and **PDF** reports showing results from Maigret’s scan of thousands of platforms.

![Screenshot 2024-12-31 at 10 03 18](https://github.com/user-attachments/assets/7290d76e-e71f-4688-93f8-ee59a786b264)


## **Features**
- **Web-based interface**: Users can scan usernames directly via a web page.
- **Real-time feedback**: Displays scan progress with a loading spinner.
- **Downloadable reports**: HTML and PDF reports are automatically generated for each scan.
- **Error handling**: Displays error messages if scans fail or unexpected issues occur.
- **Secure workflow**: Prevents simultaneous scans to avoid conflicts.

---

## **Technologies Used**
- **Python**: Flask framework for backend server.
- **Maigret**: The core username scanning tool.
- **HTML/CSS/JavaScript**: For the user interface with responsive design.
- **jQuery**: Simplifies AJAX requests and dynamic page updates.
- **Bootstrap**: Ensures clean, responsive design.

---

## **Getting Started**
### **1. Prerequisites**
- Python 3.8 or later
- Virtual environment (`venv`) for Python package management
- Maigret tool installed
- A modern web browser (for accessing the UI)

### **2. Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name/maigret-web-scanner.git
   cd maigret-web-scanner
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install Maigret:
   ```bash
   pip install maigret
   ```

### **3. Configuration**
- Ensure the `static/` directory contains `lcnr.jpg` (or replace the logo path in `index.html`).

### **4. Running the App**
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```
   or replace `127.0.0.1` with your server’s IP for external access.

---

## **How to Use**
1. Enter the username in the input box on the webpage.
2. Click the "Run Scan" button.
3. Wait for the scan to complete (loading spinner indicates progress).
4. View or download the generated HTML and PDF reports via the provided links.

---

## **Project Structure**
```plaintext
maigret-web-scanner/
├── app.py                # Main Flask application
├── templates/
│   └── index.html        # Frontend HTML template
├── static/
│   ├── lcnr.jpg          # Logo file
│   └── style.css         # Additional CSS (optional, not used in the example)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## **Example Reports**
Generated reports include:
- **HTML Report**: An interactive, browser-friendly summary.
- **PDF Report**: A downloadable version for offline use or sharing.

---

## **Advanced Options**
To customize the Maigret command further, modify the `app.py` file:
```python
command = f"maigret {username} -a -HP --folderoutput output/{username}"
```
You can add options like `--tags`, `--site`, or `--top-sites` to refine the scan.

---

## **Troubleshooting**
- **Port already in use**: Kill the process running on port 5000:
  ```bash
  lsof -i :5000
  kill -9 <process_id>
  ```
- **Errors in scan**: Check that Maigret is properly installed and accessible in the system PATH.

---

## **Future Enhancements**
- Add authentication for secure access.
- Support scheduling scans or saving scan history.
- Integrate database for managing results.
- Dockerize for simplified deployment.

---

## **License**
This project is open-source and licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contributing**
We welcome contributions! Feel free to submit issues, feature requests, or pull requests to improve this project.

---

## **Acknowledgments**
- **Maigret**: For the powerful username enumeration engine.
- **Flask**: For providing the web framework.
- **Bootstrap**: For clean and responsive design.

**Happy Scanning!**
