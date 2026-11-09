# Network Analyzer & Circuit Simulator

A beginner-friendly Streamlit project combining basic network diagnostics, circuit calculations, and AI explanations using Google's Gemini API.

## Features

### Network Analyzer
- Local device and network interface information
- Internet download/upload speed test
- Ping latency measurements
- Packet loss and latency variation estimates

### Circuit Simulator
- Simple DC voltage source and resistor
- Ohm's law current calculation
- Electrical power calculation
- AI explanation of circuit results

### AI Assistant
- Gemini-powered explanations for network and electronics questions

## Project structure

```text
network-analyzer-circuit-simulator/
├── app.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer (a compatible Python version supported by the installed packages)
- Internet connection for speed testing and Gemini API requests
- Google AI Studio API key for AI features

## Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/network-analyzer-circuit-simulator.git
   cd network-analyzer-circuit-simulator
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your Gemini API key.

   Get a key from [Google AI Studio](https://aistudio.google.com/app/apikey).

   Windows PowerShell:

   ```powershell
   $env:GEMINI_API_KEY="YOUR_API_KEY"
   ```

   macOS/Linux:

   ```bash
   export GEMINI_API_KEY="YOUR_API_KEY"
   ```

   Do not commit your API key to GitHub.

5. Run the app:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL Streamlit prints in your terminal (usually `http://localhost:8501`).

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with GitHub and create a new app.
4. Select your repository, branch, and `app.py`.
5. In the app settings, open **Secrets** and add:

   ```toml
   GEMINI_API_KEY = "YOUR_API_KEY"
   ```

6. Deploy the app.

## Important limitations

- Network tests run on the machine hosting the Python process. On a cloud deployment, this means the cloud server—not each visitor's personal device.
- Speed tests transfer data and can consume bandwidth.
- Ping may fail if the target or local network blocks ICMP.
- Speed test services may occasionally be unavailable.
- The circuit simulator currently models an ideal DC source and one resistor. It is an educational calculation, not a professional electrical design tool.
- Gemini API availability, model access, and usage limits depend on your Google AI Studio account.

## Formulas

Ohm's law:

`I = V / R`

Electrical power:

`P = V × I`

Where:
- `V` is voltage in volts
- `R` is resistance in ohms
- `I` is current in amperes
- `P` is power in watts

## License

Choose a license before publishing or distributing this project.
