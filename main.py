import socket
import pandas as pd
print(pd.__version__)
import time

ROBOT_IP = " "
PORT =  
FREQUENCY_HZ = 25
INTERVAL = 1.0 / FREQUENCY_HZ


data_list = []

try: 
    # create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROBOT_IP, PORT))
    print("Successfully connected. Starting data collection...")

    for i in range(5):
       
        #ask for coordinates
        request_cmd = "get actual tcp pose\n"
        s.sendall(request_cmd.encode('utf-8'))    
       
        response = s.recv(1024).decode('utf-8').strip()
        
        #Removing brackets like p[...] if your robot adds them
        cleaned_response = response.replace('p[', '').replace(']', '')
        
        try:
            coords = [float(val) for val in cleaned_response.split(',')]
            if len(coords) < 6:
                raise ValueError("Incomplete pose data received")
            x, y, z, rx, ry, rz = coords
        
        except ValueError as val_err:
            print(f"Skipping sample {i+1}: Could not parse response '{response}'. Error: {val_err}")
            continue
            
        # current time
        timestamp = pd.Timestamp.now()
            
        # collect robot data
        robot_reading = {
            "X": x, "Y": y, "Z": z,
            "RX": rx, "RY": ry, "RZ": rz
        }
            
        # combine timestamp and real data into one record
        record = {"Timestamp": timestamp, **robot_reading}
        data_list.append(record)
            
        print(f"Captured sample {i+1}/5 -> X: {x:.3f}, Y: {y:.3f}, Z: {z:.3f}")
        time.sleep(0.5)

except Exception as e:
    print(f"Network error: {e}")
    
finally:
    try:
        s.close() 
        print("Socket connection closed.")
    except NameError:
        pass

if data_list:
    df = pd.DataFrame(data_list)
    df.set_index("Timestamp", inplace=True)
    print("\n--- Final Time-Series DataFrame ---")
    print(df)
else:
    print("No data collected due to connection failure.")
