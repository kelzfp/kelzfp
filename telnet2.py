# Import required modules/packages/library
import pexpect

# Define Variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
config_file = 'router_config.txt'  # File to save the configuration

# Function to save the configuration to a local file
def save_configuration(session, filename):
    session.sendline('show running-config')
    session.expect('#')
    config_output = session.before
    with open(filename, 'w') as f:
        f.write(config_output)

# Create telnet session
session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8', timeout=20)

result = session.expect(['Username:', pexpect.TIMEOUT])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

# Session is expecting a username, enter the details
session.sendline(username)
result = session.expect(['Password:', pexpect.TIMEOUT])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('--- FAILURE! entering username:', username)
    exit()

# Session is expecting a password, enter the details
session.sendline(password)
result = session.expect(['#', pexpect.TIMEOUT])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('--- FAILURE! entering password:', password)
    exit()

# Add the hostname 'Router2'
session.sendline('conf t')
session.sendline('hostname Router2')
session.expect(['\(config\)#', pexpect.TIMEOUT])

# Save the configuration to a local file
save_configuration(session, config_file)

# Display a success message if it works
print('-------------------------------------------------')
print('')
print('--- Success! connecting to:', ip_address)
print('---               Username:', username)
print('---               Password:', password)
print('--- Configuration saved to:', config_file)
print('')
print('---------------------------------')

# Terminate telnet to the device and close the session
session.sendline('quit')
session.close()
