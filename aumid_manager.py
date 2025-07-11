import subprocess
import os
import sys
import winreg
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class AUMIDManager:
    """Manages AUMID registration for toast notifications"""
    
    def __init__(self, app_id="Trixinous.App.THRESHER", app_name="THRESHER"):
        self.app_id = app_id
        self.app_name = app_name
        self.registry_path = f"SOFTWARE\\Classes\\AppUserModelId\\{app_id}"
        
    def is_aumid_registered(self):
        """Check if AUMID is already registered in the registry"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_path):
                logger.info(f"AUMID {self.app_id} is already registered")
                return True
        except FileNotFoundError:
            logger.info(f"AUMID {self.app_id} is not registered")
            return False
        except Exception as e:
            logger.error(f"Error checking AUMID registration: {e}")
            return False
    
    def get_bundled_exe_path(self):
        """Get path to bundled register_hkey_aumid.exe"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable (PyInstaller)
            base_path = Path(sys._MEIPASS)
        else:
            # Running as script
            base_path = Path(__file__).parent
        
        exe_path = base_path / "register_hkey_aumid.exe"
        
        if not exe_path.exists():
            raise FileNotFoundError(f"register_hkey_aumid.exe not found at {exe_path}")
        
        return str(exe_path)
    
    def get_icon_path(self):
        """Get path to application icon"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = Path(sys._MEIPASS)
        else:
            # Running as script
            base_path = Path(__file__).parent
        
        # Look for icon in common locations
        icon_paths = [
            base_path / "res" / ".ico" / "THRESHER.ico",  # Your specific path
            base_path / "res" / "ico" / "THRESHER.ico",   # Alternative (without dot)
            base_path / "icon.ico",
            base_path / "assets" / "icon.ico",
            base_path / "resources" / "icon.ico",
            base_path / f"{self.app_name.lower()}.ico"
        ]
        
        for icon_path in icon_paths:
            if icon_path.exists():
                logger.info(f"Found icon at: {icon_path}")
                return str(icon_path)
        
        logger.warning("No icon file found, will use default")
        return None
    
    def register_aumid(self, force=False):
        """Register AUMID using bundled executable"""
        
        # Skip if already registered (unless forcing)
        if not force and self.is_aumid_registered():
            logger.info("AUMID already registered, skipping")
            return True
        
        try:
            # Get paths
            exe_path = self.get_bundled_exe_path()
            icon_path = self.get_icon_path()
            
            # Build command
            cmd = [
                exe_path,
                "--app_id", self.app_id,
                "--name", self.app_name
            ]
            
            # Add icon if available
            if icon_path:
                cmd.extend(["--icon", icon_path])
            
            logger.info(f"Registering AUMID with command: {' '.join(cmd)}")
            
            # Run registration
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            
            logger.info(f"AUMID registration successful: {result.stdout}")
            
            # Verify registration worked
            if self.is_aumid_registered():
                logger.info("AUMID registration verified")
                return True
            else:
                logger.error("AUMID registration failed verification")
                return False
                
        except FileNotFoundError as e:
            logger.error(f"Registration executable not found: {e}")
            return False
        except subprocess.TimeoutExpired:
            logger.error("AUMID registration timed out")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"AUMID registration failed: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during AUMID registration: {e}")
            return False
    
    def ensure_aumid_registered(self):
        """Ensure AUMID is registered, register if not"""
        if not self.is_aumid_registered():
            logger.info("AUMID not registered, attempting registration...")
            return self.register_aumid()
        return True


# Usage example
def setup_notifications():
    """Setup notifications with automatic AUMID registration"""
    aumid_manager = AUMIDManager()
    
    # Ensure AUMID is registered
    if aumid_manager.ensure_aumid_registered():
        logger.info("AUMID setup complete")
        return True
    else:
        logger.error("AUMID setup failed")
        return False


def send_toast_notification(title, message, icon_path=None):
    """Send toast notification with automatic AUMID setup"""
    from windows_toasts import WindowsToaster, Toast, ToastDisplayImage
    
    # Setup AUMID if needed
    aumid_manager = AUMIDManager()
    if not aumid_manager.ensure_aumid_registered():
        logger.warning("AUMID registration failed, toast may not work properly")
    
    try:
        # Create toast with registered AUMID
        toaster = WindowsToaster(aumid_manager.app_id)
        newToast = Toast()
        newToast.text_fields = [title, message]
        
        if icon_path and os.path.exists(icon_path):
            newToast.AddImage(ToastDisplayImage.fromPath(icon_path))
        
        toaster.show_toast(newToast)
        logger.info("Toast notification sent successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send toast notification: {e}")
        return False


# Example usage in your main application
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Setup notifications on app startup
    if setup_notifications():
        # Send a test notification
        send_toast_notification(
            "THRESHER Started", 
            "Application is ready to use",
            "path/to/icon.ico"
        )
    else:
        print("Failed to setup notifications")