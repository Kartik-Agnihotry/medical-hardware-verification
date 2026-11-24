import subprocess

result = subprocess.run(
    ["ngspice", "-b", "../circuits/voltage_divider.cir"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("Simulation failed!")
    print(result.stderr)
    exit(1)

vin = None
vout = None
current = None

for line in result.stdout.splitlines():

    data = line.split()

    if len(data) == 2:

        if data[0] == "in":
            vin = float(data[1])

        elif data[0] == "out":
            vout = float(data[1])

        elif data[0] == "v1#branch":
            current = abs(float(data[1]))

if None in (vin, vout, current):
    print("Required measurements not found!")
    exit(1)

print("Hardware Measurement Report")
print("---------------------------")
print(f"Input Voltage  : {vin:.6f} V")
print(f"Output Voltage : {vout:.6f} V")
print(f"Circuit Current: {current * 1000:.6f} mA")
