# Nessus Scanning Automation

This project provides a Python script to automate conditional Nessus scans based on device availability and specific scan profiles. The script reads configurations from two YAML files and checks if network devices are online before initiating Nessus scans. This setup is especially useful for environments where equipment may go offline for extended periods, allowing for efficient and targeted vulnerability scanning.

## Description

The Nessus Conditional Scanning Automation script enables network security teams to:
- Define a configuration file (`config.yml`) for the Nessus server URL, scan templates, and API keys stored securely as environment variables.
- Maintain an inventory file (`inventory.yml`) where network devices are categorized by type (e.g., workstations, servers, routers) and associated with specific scan templates.
- Only initiate scans on devices that are currently online, saving resources and reducing unnecessary scan attempts.

The script leverages the Nessus API to create and launch scans based on a device’s type, with DISA STIG profiles for different device types, ensuring each device is scanned appropriately.

## Getting Started

### Dependencies

* **Python 3.x** is required.
* Python libraries:
  - `requests` for making HTTP requests to the Nessus API.
  - `yaml` for loading configuration and inventory files.
* **Nessus API Access**: You need access to a Nessus server and API keys.
* **Environment Variables**:
  - `NESSUS_ACCESS_KEY` and `NESSUS_SECRET_KEY` must be set to store sensitive API credentials securely.

### Installing

1. **Clone the repository**:
   ```
   git clone https://github.com/VanHelwig/nessus-automation.git
   ```
2. **Install required Python packages**:
   ```
   pip install requests pyyaml
   ```
3. **Set up environment variables for API keys**:
   - On Linux/macOS:
     ```bash
     export NESSUS_ACCESS_KEY='access-key'
     export NESSUS_SECRET_KEY='secret-key'
     ```
   - On Windows:
     ```powershell
     $env:NESSUS_ACCESS_KEY='access-key'
     $env:NESSUS_SECRET_KEY='secret-key'
     ```

### Executing program

1. **Configure the YAML files**:
   - `config.yml`: Define the Nessus URL and scan templates.
   - `inventory.yml`: Specify the device inventory, organized by device type, and associate each with a scan profile.

   Example `config.yml`:
   ```yaml
   nessus:
     url: 'https://<nessus-server-ip>:8834'

   scan_templates:
     windows_stig: '<windows-stig-template-uuid>'
     esxi_stig: '<esxi-stig-template-uuid>'
     network_stig: '<network-stig-template-uuid>'
   ```

   Example `inventory.yml`:
   ```yaml
   equipment:
     workstations:
       scan_type: windows_stig_profile
       hosts:
         - workstation1.domain.local
         - workstation2.domain.local
     servers:
       scan_type: esxi_stig_profile
       hosts:
         - server1.domain.local
         - server2.domain.local
     network_equipment:
       scan_type: network_stig_profile
       hosts:
         - router1.domain.local
         - switch1.domain.local
   ```

2. **Run the program**:
   ```bash
   python nessus-scanner.py
   ```

   This will check each device in `inventory.yml` to see if it’s online. If a device is online, it will launch a Nessus scan using the associated scan profile.

## Help

If you encounter common issues, such as connection errors or missing environment variables, consider the following:

* Ensure your **Nessus server URL** is correctly configured in `config.yml`.
* Verify that **API keys** are set correctly in environment variables.
* Confirm the **Nessus scan template UUIDs** are correct for each scan type in `config.yml`.

To view help details:
```
python nessus_scanner.py --help
```

## Authors

Contributors:
- **Keenan Helwig**  
 

## Version History

* 0.1
    * Initial Release with basic functionality for conditional scanning

## License

This project is licensed under the [MIT License](LICENSE.md).

## Acknowledgments

This project was inspired and developed with the help of the following resources:
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [Tenable Nessus API Documentation](https://docs.tenable.com/nessus/)
