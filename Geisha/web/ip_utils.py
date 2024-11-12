# web/ip_utils.py
import requests
import socket
import logging

def is_aws_environment():
    try:
        socket.create_connection(("169.254.169.254", 80), timeout=1)
        return True
    except OSError:
        return False

def get_public_ip():
    if is_aws_environment():
        try:
            token_response = requests.put(
                "http://169.254.169.254/latest/api/token",
                headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
                timeout=1
            )
            token = token_response.text
            ip_response = requests.get(
                "http://169.254.169.254/latest/meta-data/public-ipv4",
                headers={"X-aws-ec2-metadata-token": token},
                timeout=1
            )
            ip_response.raise_for_status()
            return ip_response.text
        except requests.RequestException as e:
            logging.error("Failed to retrieve public IP from AWS metadata service", exc_info=e)
    
    try:
        fallback_response = requests.get("https://api.ipify.org?format=json", timeout=1)
        fallback_response.raise_for_status()
        return fallback_response.json()["ip"]
    except requests.RequestException as e:
        logging.error("Failed to retrieve public IP from fallback service", exc_info=e)
        return "IP retrieval failed"
