import paramiko
from cryptography.fernet import Fernet
import base64
import getpass

# Generate a key for encryption and decryption
# Store this key securely and don't share it
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_passphrase(passphrase):
    return cipher_suite.encrypt(passphrase.encode('utf-8'))

def decrypt_passphrase(encrypted_passphrase):
    return cipher_suite.decrypt(encrypted_passphrase).decode('utf-8')

def ssh_command(ip, port, user, private_key_file, passphrase, command):
    try:
        # Create the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Load the private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_file, password=passphrase)

        # Connect to the remote host
        client.connect(ip, port=port, username=user, pkey=private_key)

        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)

        # Read the output from stdout
        output = stdout.read().decode('utf-8')
        print("Command output:")
        print(output)

        # Read the error from stderr (if any)
        error = stderr.read().decode('utf-8')
        if error:
            print("Command error:")
            print(error)

        # Close the connection
        client.close()

    except Exception as e:
        print(f"Failed to execute command: {e}")

if __name__ == "__main__":
    # Connection details
    remote_ip = "10.103.32.128"
    remote_port = 22
    username = "bskiran"
    private_key_path = "/home/bskiran/Downloads/id_rsa"

    # Example command to run on the remote host
    remote_command = "curl ifconfig.me"

    # Get the passphrase securely
    passphrase = getpass.getpass("Enter your SSH key passphrase: ")

    # Encrypt the passphrase (for storage if needed)
    encrypted_passphrase = encrypt_passphrase(passphrase)
    
    # Decrypt the passphrase for use in the script
    decrypted_passphrase = decrypt_passphrase(encrypted_passphrase)

    # Run the SSH command
    ssh_command(remote_ip, remote_port, username, private_key_path, decrypted_passphrase, remote_command)

