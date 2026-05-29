# 🎵 Browser-Native Generative Lo-Fi Music System

[![Live Demo](https://img.shields.io/badge/Play_Now-Live_Demo-success?style=for-the-badge&logo=play)](https://roge8787.github.io/projectForLofi/)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![WebAssembly](https://img.shields.io/badge/WebAssembly-Powered-orange.svg)
![PyScript](https://img.shields.io/badge/PyScript-Framework-black.svg)
![NumPy](https://img.shields.io/badge/NumPy-Vectorized-013243.svg)
![Web_Audio_API](https://img.shields.io/badge/Web_Audio-API-brightgreen.svg)

A real-time, zero-installation generative Lo-Fi music system operating entirely within the browser. This project leverages **WebAssembly (Wasm)** via **PyScript** to bring desktop-grade Digital Signal Processing (DSP) and algorithmic composition to the edge, completely bypassing server-side rendering and local binary dependencies.

**👉 Experience the system instantly:** [https://roge8787.github.io/projectForLofi/](https://roge8787.github.io/projectForLofi/)

## ✨ Core Features

* **Edge-Computed Generative Engine:** Utilizes a music-theory-constrained, first-order Markov Chain (with strict zero-diagonal transition matrices) to generate infinite, non-repetitive harmonic progressions.
* **Master-Bus Physical Modeling (DSP):** * **Wow & Flutter:** Implements Sample Index Modulation to simulate organic analog tape pitch instability.
  * **Dynamic Breathing Filter:** Real-time Biquad Low-Pass Filtering with LFO micro-sweeps to prevent auditory fatigue.
* **High-Performance Memory Architecture:** Replaces Python scalar loops with **NumPy Vectorization** and utilizes a **Zero-Copy FFI Bridge** (`pyodide.ffi.to_js`) to stream floating-point arrays directly to the C++ Web Audio API thread.
* **Asynchronous Pre-rendering:** Synthesizes an extensive 8-bar block (~22.58 seconds) in the background, ensuring UI operations (like scenario switching) remain glitch-free.
* **Low-Cognitive-Load UI:** A responsive, glassmorphism-styled dashboard tailored for focus and stress reduction.

## 🎛️ Ambient Scenarios

The system synthesizes specialized psychoacoustic soundstages. You can switch between these modes seamlessly without interrupting the rhythmic pulse:

| Mode | DSP Cutoff | Tape Noise Gain | Aesthetic Target |
| :--- | :--- | :--- | :--- |
| 🌙 **Midnight** | 350 Hz | 0.001 | Deep, warm, low-tension isolation |
| 🌧️ **Rainy** | 800 Hz | 0.08 | High-gain acoustic masking via white noise |
| ☕ **Cafe** | 6000 Hz | 0.008 | Bright, vintage, mid-gain ambient hiss |
| 🎚️ **Passthrough** | - | - | *Demo Mode:* Direct A/B comparison with unprocessed audio |

## 🚀 Quick Start (Installation & Usage)

Because this system is entirely **Browser-Native**, you can run it directly via the Live Demo without installing Python, pip, or any local dependencies. 

If you wish to run it locally for development:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Roge8787/projectForLofi.git](https://github.com/Roge8787/projectForLofi.git)
   cd projectForLofi
