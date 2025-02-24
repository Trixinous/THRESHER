import obsws_python as obs
import time
import winreg
import json
from datetime import datetime

class OBSController:
    def __init__(self):
        # Default connection parameters for OBS WebSocket
        self.host = "localhost"
        self.port = 4455
        def load_config_from_registry():
            try:
                key_path = r"Software\Trixinous\THRESHER"  # Modified registry path
                key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                config = {}
                i = 0
                while True:
                    try:
                        name, value, type = winreg.EnumValue(key, i)
                        if type == winreg.REG_SZ:
                            try:
                                config[name] = json.loads(value)  # Try to parse JSON (for lists/dicts)
                            except json.JSONDecodeError:
                                if value.lower() == "true":
                                    config[name] = True
                                elif value.lower() == "false":
                                    config[name] = False
                                else:
                                    config[name] = value  # If not JSON, keep as string
                        i += 1
                    except OSError:  # Reached end of values
                        break
                winreg.CloseKey(key)
                print("OBS_INTEG: Config loaded from registry.")
                return config
            except FileNotFoundError:
                print("OBS_INTEG: Config not found in registry.")
                return None
            except Exception as e:
                print(f"OBS_INTEG: Error loading config from registry: {e}")
                return None
            
        config = load_config_from_registry()
        try:
            self.password = config["obs_token"]  # Set this to your OBS WebSocket password if you have one
        except Exception as e:
            print(f"OBS_INTEG: Error loading password from registry: {e}")
        self.client = None
        
    def connect(self):
        """Establish connection to OBS WebSocket"""
        try:
            self.client = obs.ReqClient(
                host=self.host,
                port=self.port,
                password=self.password
            )
            return True
        except Exception as e:
            print(f"Failed to connect to OBS: {e}")
            return False

    def create_clip(self):
        """Create a clip using the Replay Buffer"""
        try:
            if not self.client:
                if not self.connect():
                    return False
            
            # Check if Replay Buffer is active
            status = self.client.get_replay_buffer_status()
            
            if not status.output_active:
                # Start Replay Buffer if it's not active
                self.client.start_replay_buffer()
                time.sleep(1)  # Give it a moment to start
            
            # Save the replay buffer
            self.client.save_replay_buffer()
            print("Clip saved from Replay Buffer!")
            return True
                
        except Exception as e:
            print(f"Error creating clip: {e}")
            print("Make sure Replay Buffer is enabled in OBS Settings -> Output -> Replay Buffer")
            return False

    def start_recording(self):
        """Start OBS recording"""
        try:
            if not self.client:
                if not self.connect():
                    return False
                
            self.client.start_record()
            print("Recording started")
            return True
            
        except Exception as e:
            print(f"Error starting recording: {e}")
            return False

    def stop_recording(self):
        """Stop OBS recording"""
        try:
            if not self.client:
                if not self.connect():
                    return False
                
            self.client.stop_record()
            print("Recording stopped")
            return True
            
        except Exception as e:
            print(f"Error stopping recording: {e}")
            return False

# Create global OBS controller instance
obs_controller = OBSController()

def obs_integration(command):
    """
    Main function to handle OBS integration commands
    
    Args:
        command (str): The command to execute ("clip that", "start recording", "stop recording")
    """
    if not obs_controller.client and not obs_controller.connect():
        print("Could not connect to OBS. Please make sure OBS is running and WebSocket server is enabled.")
        return False

    if command.lower() in ["clip that", "clip"]:
        return obs_controller.create_clip()
    elif command.lower() == "start recording":
        return obs_controller.start_recording()
    elif command.lower() == "stop recording":
        return obs_controller.stop_recording()
    else:
        print(f"Unknown command: {command}")
        return False

if __name__ == "__main__":
    # Test the module
    print("Testing OBS integration...")
    test_commands = ["clip that", "start recording", "stop recording"]
    
    for cmd in test_commands:
        print(f"\nTesting command: {cmd}")
        result = obs_integration(cmd)
        print(f"Command {'succeeded' if result else 'failed'}")
        time.sleep(2)  # Wait between commands