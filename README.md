
# Signal Sampler & Recovery Desktop Application
![image](https://github.com/Muhannad159/Sampling_Theory_Studio/assets/110257687/75313b3b-16ae-4b5e-aa61-d30db458abf4)
## Introduction
Sampling an analog signal is a crucial step for any digital signal processing system. The Nyquist–Shannon sampling theorem guarantees a full recovery of the signal when sampling with a frequency larger than or equal to the bandwidth of the signal (or double the maximum frequency in case of real signals).

This desktop application demonstrates the process of sampling and recovering a signal, showcasing the importance and validation of the Nyquist rate.

## Features
- **Sample & Recover**: Load a mid-length signal, visualize and sample it via different frequencies, then use the sampled points to recover the original signal using the Whittaker–Shannon interpolation formula.
- **Load & Compose**: Load a signal from a file or compose one using a signal mixer. The mixer allows users to add multiple sinusoidal signals of different frequencies and magnitudes.
- **Additive Noise**: Users can add noise to the loaded signal with a custom controllable Signal-to-Noise Ratio (SNR) level. The program shows the dependency of the noise effect on the signal frequency.
- **Real-time**: Sampling and recovery are performed in real-time upon user changes.
- **Resize**: The application can be resized easily without disrupting the user interface.
- **Different Sampling Scenarios**: The application includes at least 3 testing synthetic signals generated through the Composer, each addressing different testing scenarios.

## How to Use
1. **Clone this repository** to your local machine.
2. **Install the required dependencies** (`numpy`, `matplotlib`, `scipy`).
3. **Run the `main.py` file**.
4. **Use the application interface** to load a signal, adjust sampling frequency, add noise, and visualize the sampled and recovered signals.
5. **Experiment with different scenarios** and observe the effects on signal recovery.

## Dependencies
- Python 
- NumPy
- Matplotlib
- SciPy

## Contributors
- [Ahmed Mohamed Ali]
- [Muhannad abdallah]
- [Ali Badran]
- [Hassan Ewees]


