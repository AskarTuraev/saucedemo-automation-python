import os
import sys
import ctypes
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def remove_old_keys():
    """Removes old registry keys to avoid duplicates."""
    old_keys = ["GeminiReview"]
    reg_path = r"Software\Classes\*\shell"
    
    try:
        parent_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        return

    for key_name in old_keys:
        try:
            # Try to open the key to see if it exists
            key_to_delete = winreg.OpenKey(parent_key, key_name, 0, winreg.KEY_ALL_ACCESS)
            
            # Delete subkeys first (command)
            try:
                winreg.DeleteKey(key_to_delete, "command")
            except FileNotFoundError:
                pass
                
            winreg.CloseKey(key_to_delete)
            
            # Delete the main key
            winreg.DeleteKey(parent_key, key_name)
            print(f"Removed old context menu item: {key_name}")
            
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Could not remove old key {key_name}: {e}")

    winreg.CloseKey(parent_key)

def register_context_menu():
    # Remove old keys first
    remove_old_keys()

    # Get paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    reviewer_script = os.path.join(current_dir, "reviewer.py")
    python_exe = sys.executable
    
    # Check if script exists
    if not os.path.exists(reviewer_script):
        print(f"Error: reviewer.py not found at {reviewer_script}")
        return

    # Key name for context menu
    key_name = "LocalCodeReviewer"
    menu_name = "Local Code Reviewer"
    
    # Command to run
    # Use "pause" or "cmd /k" to keep window open to see results
    command = f'cmd /k "{python_exe}" "{reviewer_script}" --file "%1"'

    print(f"Registering context menu '{menu_name}'...")
    print(f"Script: {reviewer_script}")
    
    try:
        # Open HKCU\Software\Classes\*\shell (Create if doesn't exist)
        # We use HKCU so we don't always need Admin rights (though Admin is better for system-wide)
        # Using * applies to all files.
        
        reg_path = r"Software\Classes\*\shell"
        
        # Create/Open the parent key
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        
        # Create our subkey
        app_key = winreg.CreateKey(key, key_name)
        winreg.SetValue(app_key, None, winreg.REG_SZ, menu_name)
        winreg.SetValueEx(app_key, "Icon", 0, winreg.REG_SZ, "cmd.exe") # Use cmd icon or python icon
        
        # Create command subkey
        cmd_key = winreg.CreateKey(app_key, "command")
        winreg.SetValue(cmd_key, None, winreg.REG_SZ, command)
        
        winreg.CloseKey(cmd_key)
        winreg.CloseKey(app_key)
        winreg.CloseKey(key)
        
        print("Successfully registered context menu!")
        print("Right-click any file and select 'Local Code Reviewer'.")
        
    except Exception as e:
        print(f"Error registering context menu: {e}")
        if not is_admin():
            print("Try running this script as Administrator.")

if __name__ == "__main__":
    register_context_menu()
