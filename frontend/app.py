import streamlit as st
import requests

st.set_page_config(page_title="BTC Predictor", page_icon="💹")
st.title("📈 BTC Price Predictor")
st.write("Wybierz horyzont (opcjonalnie) i kliknij Predict. Backend pobierze ostatnie dostępne dane i zwróci predykcję.")

horizon = st.selectbox("Wybierz horyzont predykcji:", ["auto", "30m", "1h", "4h", "24h", "7d"])
# st.write("Możesz też ręcznie wprowadzić cechy (opcjonalne) — pozostaw puste, by użyć ostatniego wiersza danych.")

# timestamp = st.text_input("Timestamp (opcjonalnie)")
# open_v = st.text_input("Open (opcjonalnie)")
# high_v = st.text_input("High (opcjonalnie)")
# low_v = st.text_input("Low (opcjonalnie)")
# volume_v = st.text_input("Volume (opcjonalnie)")

if st.button("Predict"):
    payload = {"horizon": None if horizon == "auto" else horizon}
    def maybe_float(x):
        try:
            return float(x)
        except Exception:
            return None

    # if timestamp:
    #     payload["Timestamp"] = maybe_float(timestamp)
    # if open_v:
    #     payload["Open"] = maybe_float(open_v)
    # if high_v:
    #     payload["High"] = maybe_float(high_v)
    # if low_v:
    #     payload["Low"] = maybe_float(low_v)
    # if volume_v:
    #     payload["Volume"] = maybe_float(volume_v)

    try:
        resp = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=20)
        if resp.status_code == 200:
            j = resp.json()
            st.success(f"Predykcja ceny: ${j['prediction']:.2f}")
            st.json(j)
        else:
            st.error(f"API returned status {resp.status_code}: {resp.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Błąd połączenia z API: {e}")
