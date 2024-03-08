
# Signal Sampler & Recovery Desktop Application

![Signal Sampler & Recovery Desktop Application](https://github.com/Muhannad159/Sampling_Theory_Studio/assets/110257687/75313b3b-16ae-4b5e-aa61-d30db458abf4)

## Introduction

Sampling an analog signal is a crucial step for any digital signal processing system. The Nyquist–Shannon sampling theorem guarantees a full recovery of the signal when sampling with a frequency larger than or equal to the bandwidth of the signal (or double the maximum frequency in case of real signals).

This desktop application demonstrates the process of sampling and recovering a signal, showcasing the importance and validation of the Nyquist rate.

## Features

### Sample & Recover

This feature allows users to load a mid-length signal, visualize it, sample it at different frequencies, and then recover the original signal using the Whittaker–Shannon interpolation formula. It provides a practical demonstration of the Nyquist–Shannon sampling theorem.

### Load & Compose

Users can load a signal from a file or compose one using a signal mixer. The signal mixer permits users to add multiple sinusoidal signals of different frequencies and magnitudes, enabling experimentation with various signal compositions.

### Additive Noise

This feature enables users to introduce noise to the loaded signal with a custom controllable Signal-to-Noise Ratio (SNR) level. Users can observe how noise affects the signal, and the application visually demonstrates the dependency of noise effects on signal frequency.

### Real-time

Sampling and recovery operations are performed in real-time, providing immediate feedback to users as they adjust parameters. This feature enhances the user experience by allowing for seamless interaction with the application.

### Resize

The application's user interface is designed to be easily resizable without disruption. Users can adjust the size of the application window to suit their preferences without compromising usability.

### Different Sampling Scenarios

The application includes at least three synthetic signals generated through the Composer, each addressing different testing scenarios. These scenarios provide users with opportunities to explore various signal characteristics and sampling conditions.

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

## Contributors <a name = "Contributors"></a>

<table>
  <tr>
    <td align="center">
    <a href="https://github.com/Muhannad159" target="_black">
    <img src="https://avatars.githubusercontent.com/u/104541242?v=4" width="150px;" alt="Muhannad Abdallah"/>
    <br />
    <sub><b>Muhannad Abdallah</b></sub></a>
    </td>
  <td align="center">
    <a href="https://github.com/AliBadran716" target="_black">
    <img src="https://avatars.githubusercontent.com/u/102072821?v=4" width="150px;" alt="Ali Badran"/>
    <br />
    <sub><b>Ali Badran</b></sub></a>
    </td>
     <td align="center">
    <a href="https://github.com/ahmedalii3" target="_black">
    <img src="https://avatars.githubusercontent.com/u/110257687?v=4" width="150px;" alt="Ahmed Ali"/>
    <br />
    <sub><b>Ahmed Ali</b></sub></a>
    </td>
<td align="center">
    <a href="https://github.com/hassanowis" target="_black">
    <img src="https://avatars.githubusercontent.com/u/102428122?v=4" width="150px;" alt="Hassan Hussein"/>
    <br />
    <sub><b>Hassan Hussein</b></sub></a>
    </td>
      </tr>
 </table>


