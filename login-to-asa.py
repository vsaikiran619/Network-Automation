# function to login to ASA;
import pexpect
import re




def login_to_asa(user,passwd,ip,prompt='#'):
    with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(passwd)
        enable_status = ssh.expect([">", "#"])
        if enable_status == 0:
            ssh.sendline("enable")
            ssh.expect("[Pp]assword")
            ssh.sendline(passwd)
            ssh.expect(prompt)
        ssh.sendline('sh int ip br')
        output = ''
        while True:
            '''Now after sending the command, expect method waits for another option --More-- - sign, that there will be one more page further. Since it’s not known in advance how many pages will be in the output, reading is performed in a loop while True. Loop is interrupted if prompt is met # or no prompt appears within 10 seconds or --More--.

If --More-- is met, pages are not over yet and you have to scroll through the next one. In Cisco, you need to press space bar to do this (without new line). Therefore, send method is used here, not sendline - sendline automatically adds a new line character. '''

            match = ssh.expect([prompt, "--More--", pexpect.TIMEOUT])
            page = ssh.before.replace("\r\n", "\n")

            '''This string page = re.sub(" +\x08+ +\x08+", "\n", page) removes backspace symbols which are around --More-- so they don’t end up in the final output.
            '''
            page = re.sub(" +\x08+ +\x08+", "\n", page)
            output += page
            if match == 0:
                break
            elif match == 1:
                ssh.send(" ")
            else:
                print("Error: timeout")
                break
        output = re.sub("\n +\n", "\n", output)
        return output

asa_mgmt_ip = "10.103.16.200"
user="scripty"
passwd = input("Enter Scripty Password: ")


result=login_to_asa(user,passwd,asa_mgmt_ip)
print(result)
