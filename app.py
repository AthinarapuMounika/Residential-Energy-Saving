import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import random


# 🔧 Enhanced device control function with persistent state
def device_control(device, room):
    st.markdown("### 🎛️ Device Control")

    if "device_states" not in st.session_state:
        st.session_state.device_states = {}

    key = f"{room}_{device}"
    current_state = st.session_state.device_states.get(key, "OFF")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Turn ON"):
            st.session_state.device_states[key] = "ON"
            st.success(f"{device} turned ON in {room}")
    with col2:
        if st.button("Turn OFF"):
            st.session_state.device_states[key] = "OFF"
            st.warning(f"{device} turned OFF in {room}")

    st.markdown(f"**Current State:** {st.session_state.device_states.get(key, 'OFF')}")

# 🔐 Authentication setup
hashed_passwords = stauth.Hasher(['admin123']).generate()

config = {
    'credentials': {
        'usernames': {
            'admin': {
                'name': 'Administrator',
                'password': hashed_passwords[0]
            }
        }
    },
    'cookie': {
        'name': 'simple_login',
        'key': 'random_key',
        'expiry_days': 1
    },
    'preauthorized': {
        'emails': []
    }
}

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("main")

# 🔓 Main app logic
if authentication_status:
    st.sidebar.title(f"Welcome, {name}")
    authenticator.logout("Logout", "sidebar")

    st.title("🏠 Residential Energy Dashboard")

    # 📦 Sample data
    blocks = {
        "Block A": ["Room 101", "Room 102", "Room 103"],
        "Block B": ["Room 201", "Room 202", "Room 203"],
        "Block C": ["Room 301", "Room 302", "Room 303"]
    }

    occupied_rooms = ["Room 101", "Room 202", "Room 301", "Room 103"]
    all_rooms = [room for rooms in blocks.values() for room in rooms]
    unoccupied_rooms = list(set(all_rooms) - set(occupied_rooms))

    # 🏠 Room and device selection
    block = st.selectbox("Select Block", list(blocks.keys()))
    room = st.selectbox("Select Room", blocks[block])
    device = st.selectbox("Select Device", ["Light", "Fan", "AC", "Heater"])

    # ⚡ Simulated usage data
    usage_28_days = random.randint(50, 500)  # kWh
    usage_365_days = random.randint(1000, 5000)  # kWh
    current_status = random.choice(["ON", "OFF"])
    power_usage = random.randint(50, 200)  # Watts

    st.markdown(f"### 🔍 Status for {device} in {room}, {block}")
    st.info(f"Power usage: {power_usage}W\nStatus: {current_status}")

    # ✅ Device control
    device_control(device, room)

    # 📊 Electricity Usage & 💰 Estimated Cost (Interactive)
    st.markdown("### 📊 Electricity Usage & 💰 Estimated Cost")

    period = st.selectbox("Select Time Period", ["28 Days", "365 Days"])
    rate_per_kwh = 7.5  # ₹ per kWh

    if period == "28 Days":
        st.metric("Usage", f"{usage_28_days} kWh")
        st.metric("Estimated Cost", f"₹{usage_28_days * rate_per_kwh:.2f}")
    else:
        st.metric("Usage", f"{usage_365_days} kWh")
        st.metric("Estimated Cost", f"₹{usage_365_days * rate_per_kwh:.2f}")

    # 📈 Historical Usage Chart
    st.markdown("### 📈 Usage Trend (Last 30 Days)")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    usage = np.random.randint(5, 20, size=30)
    st.line_chart(pd.DataFrame({"Usage (kWh)": usage}, index=dates))

    # 🛏️ Unoccupied Rooms
    st.markdown("### 🛏️ Unoccupied Rooms")
    st.write(unoccupied_rooms)

    # ⚡ Idle Rooms
    st.markdown("### ⚡ Idle Rooms (Low Usage)")
    idle_rooms = [r for r in all_rooms if r not in occupied_rooms or random.random() < 0.3]
    st.write(idle_rooms)

    # 💡 Energy Saving Tips
    st.markdown("### 💡 Energy Saving Tips")
    st.info("Use LED lights, unplug idle devices, and schedule appliance usage during off-peak hours.")

elif authentication_status is False:
    st.error("Incorrect username or password.")
elif authentication_status is None:
    st.warning("Please enter your username and password.")