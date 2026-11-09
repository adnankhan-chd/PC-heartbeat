import os
import socket
import time
import platform
import statistics
import streamlit as st
import psutil
import speedtest
from ping3 import ping
from google import genai

st.set_page_config(
    page_title="Network Analyzer & Circuit Simulator",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Network Analyzer & Circuit Simulator")
st.caption("Monitor your connection, explore circuit calculations, and ask AI for explanations.")

# ---------- Helpers ----------
def get_gemini_client():
    """Load API key from Streamlit secrets or environment variable."""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""
    api_key = api_key or os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def ai_explain(prompt):
    client = get_gemini_client()
    if client is None:
        return "Gemini API key is missing. Add GEMINI_API_KEY to Streamlit secrets or your environment."
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return response.text or "The model returned an empty response."
    except Exception as exc:
        return f"AI request failed: {exc}"

def get_local_ip():
    """Find the local IP address without sending application data."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This does not send a packet; it selects the outgoing interface.
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "Unavailable"
    finally:
        sock.close()

# ---------- Navigation ----------
network_tab, circuit_tab, ai_tab = st.tabs(
    ["🌐 Network Analyzer", "⚡ Circuit Simulator", "🤖 AI Assistant"]
)

# ---------- Network Analyzer ----------
with network_tab:
    st.header("Network connection details")

    col1, col2, col3 = st.columns(3)
    col1.metric("Device", platform.node() or "Unknown")
    col2.metric("Operating system", platform.system())
    col3.metric("Local IP", get_local_ip())

    st.subheader("Network interfaces")
    interfaces = psutil.net_if_addrs()
    rows = []
    for interface, addresses in interfaces.items():
        for address in addresses:
            if address.family == socket.AF_INET:
                rows.append({
                    "Interface": interface,
                    "IPv4 address": address.address,
                    "Netmask": address.netmask or "N/A"
                })
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No IPv4 interface information found.")

    st.subheader("Internet speed test")
    st.warning("A speed test transfers data and may use significant bandwidth.")
    if st.button("Run internet speed test", key="speed_test"):
        with st.spinner("Testing download and upload speed..."):
            try:
                tester = speedtest.Speedtest()
                tester.get_best_server()
                download_mbps = tester.download() / 1_000_000
                upload_mbps = tester.upload() / 1_000_000
                latency_ms = tester.results.ping

                a, b, c = st.columns(3)
                a.metric("Download", f"{download_mbps:.2f} Mbps")
                b.metric("Upload", f"{upload_mbps:.2f} Mbps")
                c.metric("Test server latency", f"{latency_ms:.1f} ms")
            except Exception as exc:
                st.error(f"Speed test failed: {exc}")
                st.caption("The test provider may be unavailable or blocked by your network.")

    st.subheader("Latency and connection stability")
    host = st.text_input("Host to test", value="8.8.8.8")
    count = st.slider("Number of ping samples", min_value=3, max_value=10, value=5)

    if st.button("Measure latency", key="latency_test"):
        results = []
        progress = st.progress(0)
        status = st.empty()

        for i in range(count):
            status.write(f"Ping sample {i + 1} of {count}...")
            try:
                result = ping(host, timeout=2, unit="ms")
                results.append(result if result is not None else None)
            except Exception:
                results.append(None)
            progress.progress((i + 1) / count)
            time.sleep(0.2)

        successful = [r for r in results if r is not None]
        lost = len(results) - len(successful)
        loss_pct = lost / count * 100

        x, y, z = st.columns(3)
        x.metric("Packet loss", f"{loss_pct:.0f}%")
        y.metric("Successful samples", f"{len(successful)}/{count}")
        z.metric("Average latency", f"{statistics.mean(successful):.1f} ms" if successful else "N/A")

        if successful:
            st.write(f"Minimum: {min(successful):.1f} ms")
            st.write(f"Maximum: {max(successful):.1f} ms")
            if len(successful) > 1:
                st.write(f"Latency variation (standard deviation): {statistics.pstdev(successful):.1f} ms")
        st.caption("Ping results depend on the host, firewall, and network conditions.")

# ---------- Circuit Simulator ----------
with circuit_tab:
    st.header("Basic DC circuit simulator")
    st.write("Simulate a simple resistor connected to a DC voltage source.")

    left, right = st.columns(2)
    with left:
        voltage = st.number_input("Voltage (V)", min_value=0.0, value=12.0, step=1.0)
        resistance = st.number_input("Resistance (Ω)", min_value=0.01, value=100.0, step=10.0)
    with right:
        st.markdown("### Circuit")
        st.code(
            "  + ─── [ DC Voltage Source ] ─── [ Resistor ] ─── -\n"
            f"  V = {voltage:.2f} V                 R = {resistance:.2f} Ω"
        )

    current = voltage / resistance
    power = voltage * current

    m1, m2, m3 = st.columns(3)
    m1.metric("Current", f"{current:.4f} A")
    m2.metric("Power", f"{power:.4f} W")
    m3.metric("Resistance", f"{resistance:.2f} Ω")

    st.latex(r"I = \frac{V}{R}")
    st.latex(r"P = V \times I")

    if st.button("Explain my circuit with AI"):
        prompt = (
            "Explain this simple DC resistor circuit in beginner-friendly terms. "
            f"Voltage={voltage} V, resistance={resistance} ohms, "
            f"calculated current={current:.4f} A, power={power:.4f} W. "
            "Explain Ohm's law and show the calculation."
        )
        with st.spinner("Generating circuit explanation..."):
            st.markdown(ai_explain(prompt))

# ---------- AI Assistant ----------
with ai_tab:
    st.header("AI network and circuit assistant")
    st.write("Ask for help interpreting network measurements or understanding circuit concepts.")
    question = st.text_area(
        "Your question",
        placeholder="Example: What does 80 ms latency mean for video calls?"
    )
    if st.button("Ask AI", key="ask_ai"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("AI is thinking..."):
                st.markdown(ai_explain(
                    "You are a helpful beginner-friendly network and electronics tutor. "
                    "Explain concepts clearly and safely. User question: " + question
                ))

st.divider()
st.caption("Educational project. Network measurements are estimates and may vary by device, server, and connection.")
