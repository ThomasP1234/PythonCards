import subprocess

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

if __name__ == '__main__':
    check_command = 'Get-NetFirewallRule -DisplayName "Python Cards Game"'
    check_info = run(check_command)
    if check_info.returncode != 0:
        print("Ports do not exist")
    else:
        print("Rule Exists")
    
    print("-------------------------")