# Ultimate Lo-Fi: Browser-Native Real-Time Generative Music Engine

A decentralized, edge-computing generative audio system that creates non-repeating Lo-Fi ambient music directly inside the browser. Built as an undergraduate graduation project at **National Chi Nan University (NCNU)**.

By combining **WebAssembly (PyScript/Pyodide)** for algorithmic composition and the native **Web Audio API** for digital signal processing (DSP), this system operates entirely client-side without any server overhead or local software installations.

## 🚀 Live Demo
Experience the real-time generative engine directly on GitHub Pages:
👉 **[👉 這裡貼上你的 GitHub Pages 網址，例如: https://你的帳號.github.io/ultimate_lo_fi/]**

---

## ✨ Key Features
- **Deterministic Markov Chain Composition:** Governs chord progressions via a discrete-time Markov chain, incorporating a strict diagonal constraint ($P_{ii} = 0$) to eliminate mechanical loops.
- **High-Performance Wasm Kernel:** Leverages PyScript to execute vectorized audio matrix generation using NumPy at near-native speeds inside the browser.
- **Zero-Copy FFI Memory Bridge:** Utilizes Pyodide's memory mapping to transfer raw waveform arrays directly to the browser C++ rendering thread, achieving sub-10ms latency.
- **Analog Tape Physical Modeling:** Real-time retro tape emulation via a dynamic Biquad low-pass filter (-12 dB/oct roll-off) and customized Wow & Flutter temporal micro-modulations.
- **Glassmorphism UI Dashboard:** A responsive, modern interface stylized with Tailwind CSS designed for low cognitive load.

---

## 🛠️ Tech Stack
- **Frontend Layer:** HTML5, Tailwind CSS (Glassmorphic Design)
- **Execution Kernel:** PyScript / Pyodide (Python compiled to WebAssembly)
- **Mathematical Processing:** NumPy Vectorized Matrix Operations
- **Audio Rendering Engine:** Web Audio API (Native Browser C++ Context)