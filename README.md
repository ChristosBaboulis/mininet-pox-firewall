# Software-defined Firewall using Mininet and POX

This repository contains a simple SDN-based firewall implemented using the POX controller and tested in a Mininet virtual network topology.

## Technologies Used

- Mininet – for emulating the virtual network
- POX Controller – to apply OpenFlow rules dynamically
- Open vSwitch – as the data plane element
- iperf / ping – for basic network testing

## Functionality

- Allows only **UDP traffic** between hosts.
- Drops all **ICMP (e.g., ping)** and **TCP** traffic.
- **Floods ARP packets** to enable basic connectivity.
- Dynamically installs flow rules on the switch for UDP traffic based on destination IP.

## Files

| File                | Description                                                        |
| ------------------- | ------------------------------------------------------------------ |
| `POX_Controller.py` | The reactive POX firewall controller implementation                |
| `topology.py`       | The Mininet script that creates a topology of 1 switch and 5 hosts |

## Environment Setup

This project was developed and tested on a virtual machine specifically prepared for the course "Internet Technologies and Services" (MSc, AUEB).

### Recommended Environment

- **Virtual Machine**: Lubuntu 24.04 LTS 64-bit
- **Hypervisor**: Oracle VirtualBox (latest version recommended)
- **Allocated Resources**:
- Disk Space: 10 GB
- RAM: 2 GB
- Video Memory: 128 MB (3D acceleration enabled)
- CPUs: 1 or 2 (adjustable from VM settings for better performance)
- **Guest Additions**: Installed (for file sharing and system acceleration)
- **User Credentials**:
- Username: `csuser`
- Password: `csuser`
- **Python Versions**:
- Python 3 (for Mininet)
- Python 2.7 (required for POX controller)
- **Software Included**:
- Mininet (with Open vSwitch)
- POX Controller
- Wireshark (for packet analysis)
- iperf, ping utilities

### Important Notes

- All commands must be run with **superuser privileges** (use `sudo`).
- Use `sudo mn -c` to clean any previous Mininet sessions.
- Make sure no other controller is using **port 6653**.
- To monitor network traffic, launch **Wireshark** and listen to the `s1-ethX` interfaces.

### Getting Started

A pre-configured virtual disk (`.vdi`) is provided through the course eClass platform. After downloading:

1. Extract it using [7-Zip](https://www.7-zip.org/).
2. Create a new Virtual Machine in VirtualBox:
   - Type: **Linux**
   - Version: **Ubuntu (64-bit)**
3. Attach the extracted `.vdi` file as an existing virtual hard disk.
4. Adjust system settings (RAM, CPUs, Video Memory) from VM settings if needed.
5. Enable **Virtualization Extensions** (VT-x or AMD-V) from your BIOS if the VM fails to start.

For detailed instructions and the virtual disk, refer to the course material at:  
**https://eclass.aueb.gr/modules/ebook/show.php/INF121/11/**

## How to Run

### Step 1 – Launch the POX controller

```bash
cd ~/pox
sudo ./pox.py log.level --DEBUG POX_Controller
```

### Step 2 – Launch the Mininet topology

```bash
sudo python3 topology.py
```

## Sample Results

- `pingall` fails: ICMP is blocked
- `iperfudp` succeeds: UDP is allowed
- `dpctl dump-flows` shows installed OpenFlow rules

## Disclaimer

For educational purposes only.

## Author

**Christos Bampoulis**  
GitHub: [@ChristosBaboulis](https://github.com/ChristosBaboulis)  
Email: chrisb2603@gmail.com

## Acknowledgments

This project was developed as part of an MSc academic assignment in the course "Internet Technologies and Services", focusing on SDN controller-based firewalls using POX and Mininet.

## License

This project is licensed under the MIT License.
