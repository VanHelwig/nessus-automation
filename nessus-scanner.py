#!/bin/python3

import os               # Standard library to interact with the OS, used for pinging hosts
import requests         # Requests library to interact with the Nessus API
import yaml             # YAML library to load configuration and inventory files

# Load YAML configuration
def load_config(file_path='config.yml'):
    """Load configuration from the specified YAML file."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

# Load YAML inventory
def load_inventory(file_path='inventory.yml'):
    """Load inventory of devices from the specified YAML file."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

# Check if a host is online
def is_online(hostname):
    """
    Pings the hostname to check if it's online.
    Returns True if the host responds, False otherwise.
    """
    response = os.system(f'ping -c 1 {hostname} > /dev/null 2>&1')
    return response == 0  # 0 indicates success (host is online)

# Launch Nessus scan for an online host with specific scan type
def launch_nessus_scan(hostname, scan_type, nessus_url, headers, scan_templates):
    """
    Launches a Nessus scan for a specific hostname using the specified scan type.
    
    Args:
        hostname (str): The device's hostname.
        scan_type (str): Type of scan as defined in the inventory.
        nessus_url (str): Nessus API base URL.
        headers (dict): API headers with authentication.
        scan_templates (dict): Mapping of scan types to Nessus UUIDs.
    
    Returns:
        str: The scan ID if launched successfully, None otherwise.
    """
    # Get the UUID for the scan type
    template_uuid = scan_templates.get(scan_type)
    if not template_uuid:
        print(f'Scan type {scan_type} not found in template mapping.')
        return None

    # Define the payload with scan configuration
    scan_payload = {
        'uuid': template_uuid,
        'settings': {
            'name': f'Scan for {hostname} - {scan_type}',
            'text_targets': hostname,
            'enabled': True
        }
    }
    
    # Send the scan creation request to the Nessus API
    response = requests.post(f'nessus_url}/scans', headers=headers, json=scan_payload)
    if response.status_code == 200:
        scan_id = response.json()['scan']['id']
        print(f'Scan created and launched for {hostname} with ID: {scan_id}')
        return scan_id
    else:
        print(f'Failed to create scan for {hostname}.')
        return None

# Main function to process the inventory and configuration
def main():
    # Load configuration and inventory data from YAML files
    config = load_config()                 # Load Nessus URL, API keys, scan templates
    inventory = load_inventory()           # Load inventory of equipment to scan

    # Set Nessus URL and headers for API requests
    nessus_url = config['nessus']['url']
    headers = {
        'X-ApiKeys': f"accessKey={config['nessus']['access_key']}; secretKey={config['nessus']['secret_key']}",
        'Content-Type': 'application/json'
    }
    scan_templates = config['scan_templates']  # Load scan templates

    scan_ids = []  # To store launched scan IDs for tracking

    # Loop through each equipment type in the inventory
    for equipment_type, details in inventory['equipment'].items():
        scan_type = details['scan_type']  # Get scan type for the equipment category
        print(f"Checking {equipment_type} with scan type {scan_type}...")

        # Loop through each hostname under the current equipment type
        for hostname in details['hosts']:
            if is_online(hostname):  # Check if the host is online
                print(f'{hostname} is online. Launching {scan_type} scan...')
                scan_id = launch_nessus_scan(hostname, scan_type, nessus_url, headers, scan_templates)
                if scan_id:
                    scan_ids.append(scan_id)  # Append successful scan IDs
            else:
                print(f'{hostname} is offline. Skipping scan.')

    # Output the list of successfully launched scans
    print(f'Scans launched for the following hosts: {scan_ids}')

# Entry point for the script
if __name__ == "__main__":
    main()
