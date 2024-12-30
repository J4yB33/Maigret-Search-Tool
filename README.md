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

