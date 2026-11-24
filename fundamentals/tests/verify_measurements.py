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
def verify(parameter, measured, expected, tolerance):

    error = abs(measured - expected) / abs(expected) * 100

    if error <= tolerance:
        status = "PASS"
    else:
        status = "FAIL"

    print(f"Parameter : {parameter}")
    print(f"Expected  : {expected:.6f}")
    print(f"Measured  : {measured:.6f}")
    print(f"Error     : {error:.6f}%")
    print(f"Tolerance : {tolerance}%")
    print(f"Result    : {status}")
    print("-" * 35)

    return status == "PASS"


print("\nHardware Verification Report")
print("=" * 35)

test1 = verify("Input Voltage (V)", vin, 5, 1)

test2 = verify("Output Voltage (V)", vout, 10/3, 1)

test3 = verify("Current (mA)", current * 1000, 1/6, 1)

if test1 and test2 and test3:
    print("OVERALL RESULT: PASS")
else:
    print("OVERALL RESULT: FAIL")
    exit(1)
