import logging
import requests
import time
import yaml

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def check_endpoint(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')

    try:
        response = requests.request(method, url, headers=headers, data=body)
        response.raise_for_status()  
        latency = response.elapsed.total_seconds() * 1000  
        if latency < 500 :
            return True, latency
        else:
            return False, latency
    except requests.exceptions.HTTPError as e:
        logging.error(e)
        return False, 0
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return False, 0

def calculate_availability_percentage(successful_requests, total_requests):
    if total_requests == 0:
        return 0
    return int((successful_requests / total_requests) * 100)

def log_availability_percentages(availabilities):
    for domain, (successful_requests, total_requests) in availabilities.items():
        percentage = calculate_availability_percentage(successful_requests, total_requests)
        logging.info(f"{domain} has {percentage}% availability percentage")

def main():
    file_path = input("Enter the path of the YAML configuration file: ")

    with open(file_path, 'r') as file:
        endpoints = yaml.safe_load(file)

    availabilities = {}

    try:
        while True:
            for endpoint in endpoints:
                result, latency = check_endpoint(endpoint)

                domain = endpoint['url'].split('/')[2]
                if domain not in availabilities:
                    availabilities[domain] = [0, 0]  

                availabilities[domain][1] += 1  

                if result:
                    availabilities[domain][0] += 1  

                logging.info(
                    f"Endpoint with name {endpoint['name']} "
                    f"has HTTP response code {200 if result else 'error'} "
                    f"and response latency {latency:.2f} ms => {'UP' if latency<500 and result else 'DOWN'}"
                )

            log_availability_percentages(availabilities)
            time.sleep(15)

    except KeyboardInterrupt:
        logging.info("Program terminated by user.")

if __name__ == "__main__":
    main()
