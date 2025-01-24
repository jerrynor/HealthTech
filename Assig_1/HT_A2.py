import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 1. Load signal data based on student ID
name = "Jerry Nordman"
id = 2422307

# Select the file based on the student ID
n = id % 5  # Modulo 5 of the student ID
num_list = [3, 4, 6, 8, 9]  # List of file numbers
filename = f'./data/bidmc_{num_list[n]:02d}_Signals.csv'
print(f'Filename: {filename}')

# Load the data
try:
    data = pd.read_csv(filename)
except FileNotFoundError:
    print(f"File {filename} not found.")

# 2. Select the PPG signal and define time
ppg = data[' PLETH']  # Select the PLETH signal
sampling_frequency = 125  # Sampling frequency in Hz
ts = 1 / sampling_frequency  # Sampling interval in seconds
t = np.arange(len(ppg)) * ts  # Time vector

# 3. Plot the signal (first 180 seconds)
plt.figure(figsize=(10, 3))
plt.plot(t, ppg, label='PPG Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title(f'File: {filename}')
plt.xlim(0, 180)
plt.grid()
plt.legend()
plt.show()

# 4. Detect peaks in the signal
peaks, _ = find_peaks(ppg, distance=sampling_frequency*0.6)  # Minimum 0.6 seconds between peaks

# Plot the signal with detected peaks
plt.figure(figsize=(12, 6))
plt.plot(t, ppg, label='PPG Signal')
plt.plot(t[peaks], ppg[peaks], "rx", label='Peaks')
plt.title("PPG Signal and Detected Peaks")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

# 5. Calculate HRV parameters
peak_intervals = np.diff(peaks) / sampling_frequency * 1000  # Convert to milliseconds
average_hr = 60 / (np.mean(peak_intervals) / 1000)  # Average heart rate
std_ppi = np.std(peak_intervals)  # Standard deviation of PPI
rmssd = np.sqrt(np.mean(np.diff(peak_intervals)**2))  # RMS of successive differences

# Print the parameters
print("Average Heart Rate (HR):", average_hr)
print("Average PPI (ms):", np.mean(peak_intervals))
print("PPI Standard Deviation (SD):", std_ppi)
print("RMSSD:", rmssd)

