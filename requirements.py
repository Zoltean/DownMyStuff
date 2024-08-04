import subprocess
import sys

# Список залежностей
dependencies = [
    "PyQt5",
    "pandas",
    "openpyxl",
    "matplotlib"
]

# Функція для встановлення залежностей
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Встановлення всіх залежностей
for package in dependencies:
    install(package)

print("All dependencies installed successfully.")
