HTTP Endpoint Health Checker
Overview
This script monitors the health of HTTP endpoints as specified in a YAML configuration file. It checks each endpoint's status and logs their availability over time.
Requirements
Python 3.x
requests
pyyaml
Setup
Install the required Python libraries:
pip install requests pyyaml
Configuration
Create a YAML file with the list of endpoints to monitor. Example format:
yaml
	•	name: Example Endpoint url: https://example.com/api method: GET - name: Another Endpoint url: https://example.com/health method: POST headers: Content-Type: application/json body: '{"key": "value"}'
Usage
Run the script and enter the path to your configuration YAML file:
bash
python health_checker.py
Output
The script logs the status and availability percentage of each domain every 15 seconds.
Termination
To stop the script, use CTRL+C.
