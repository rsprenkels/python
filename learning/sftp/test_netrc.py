import netrc

# Define which host in the .netrc file to use
HOST = '77.64.250.147'

# Read from the .netrc file in your home directory
secrets = netrc.netrc()
username, account, password = secrets.authenticators( HOST )

print(username, password)