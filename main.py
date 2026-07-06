import socket

# Replace with your robot's actual IP address
ROBOT_IP = 
PORT =  # Primary/Real-Time interface port for UR robots


try:
    # Create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROBOT_IP, PORT))
    
    # Receive data from the robot
    data = s.recv(1024)
    print(f"Received robot data: {data}")

except Exception as e:
    print(f"Connection failed: {e}")

finally:
    s.close()
