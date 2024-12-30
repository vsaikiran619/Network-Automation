import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"{e.stderr}")


if __name__ == "__main__":
   # ip_addresses = ["8.8.8.8", "1.1.1.1", "123.123.123.123"]
    for ip in range(1,256):
        ip='10.181.44.{0}'.format(ip)
        host = str ('host ' + ip)
        print(host)
        run_command(host)
        #subprocess.run(host)
