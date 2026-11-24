import subprocess

result = subprocess.run(
    ["ngspice", "-b", "../circuits/voltage_divider.cir"],
    capture_output=True,
    text=True
)

print(result.stdout)
print("Return code:", result.returncode)
