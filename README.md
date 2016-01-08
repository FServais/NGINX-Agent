# NGINX-Agent

## Required
### Ubuntu/Debian
(`sudo apt-get install`)
- build-essential
- libssl-dev
- libffi-dev
- python-dev
- python-pip

### Fedora/RHEL-derivatives
(`sudo yum install`)
- gcc
- libffi-devel
- python-devel
- openssl-devel
- python-pip

## Python packages required
To install all at once:
```
pip install -r requirements.txt
```

## Run the Agent
You can run the agent using this command:
`sudo python agent.py --ip <ip_of_the_agent>`

That command will run a web server on the port 5000 of the device, providing an API at the address `<ip_of_the_agent>:5000`.

**Coming soon...**
