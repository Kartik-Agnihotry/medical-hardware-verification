import subprocess
from pathlib import Path

CIRCUITS = Path(__file__).resolve().parent.parent / "circuits"


def run_simulation(filename):
    result = subprocess.run(
        ["ngspice", "-b", str(CIRCUITS / filename)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    for line in result.stdout.splitlines():
        data = line.split()

        if len(data) == 2 and data[0] == "out":
            return float(data[1])

    raise RuntimeError("Output voltage not found")


def detect_fault(voltage):
    if voltage < 3.1:
        return "LOW_VOLTAGE_FAULT"
    elif voltage > 3.5:
        return "HIGH_VOLTAGE_FAULT"
    else:
        return "NORMAL"


test_cases = [
    ("TC-001", "voltage_divider.cir", "NORMAL"),
    ("TC-002", "voltage_divider_short.cir", "LOW_VOLTAGE_FAULT"),
    ("TC-003", "voltage_divider_open.cir", "HIGH_VOLTAGE_FAULT")
]

passed = 0

for test_id, filename, expected in test_cases:

    print(f"\nTest ID: {test_id}")

    try:
        voltage = run_simulation(filename)
        actual = detect_fault(voltage)

        print(f"Voltage  : {voltage:.9f} V")
        print(f"Expected : {expected}")
        print(f"Actual   : {actual}")

        if actual == expected:
            print("Result   : PASS")
            passed += 1
        else:
            print("Result   : FAIL")

    except (RuntimeError, OSError, ValueError) as error:
        print(f"Result   : ERROR - {error}")

    print("-" * 40)

total = len(test_cases)

print("\nTEST SUMMARY")
print("=" * 40)
print(f"Total Tests : {total}")
print(f"Passed      : {passed}")
print(f"Not Passed  : {total - passed}")
print(f"Pass Rate   : {passed / total * 100:.2f}%")

raise SystemExit(0 if passed == total else 1)
