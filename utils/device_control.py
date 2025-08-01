def should_turn_off(device_status, user_present):
    return device_status == "On" and user_present == "No"