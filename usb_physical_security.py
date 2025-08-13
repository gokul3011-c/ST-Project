import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import webbrowser
import getpass
from datetime import datetime
import winreg
import ctypes
import sys

class USBPhysicalSecurity:
    def __init__(self):
        self.password = "admin123"
        self.log_file = "usb_physical_security.log"
        self.root = tk.Tk()
        
        # Configuration options
        self.enable_real_time_updates = True  # Set to False to disable real-time status
        self.status_update_interval = 10000   # Status update interval in milliseconds (10 seconds)
        self.gui_update_interval = 1000      # GUI responsiveness interval in milliseconds
        
        self.setup_gui()
        self.create_log_file()
        
        # Check admin privileges on startup
        if not self.is_admin():
            self.root.after(500, self.show_admin_warning)
        
        # DISABLED: Real-time status updates to prevent freezing
        # if self.enable_real_time_updates:
        #     self.root.after(100, self.update_usb_status)
        
        # DISABLED: Periodic GUI updates that may cause freezing
        # self.root.after(self.gui_update_interval, self.keep_gui_responsive)
        
        # Instead, just update status once on startup
        self.root.after(1000, self.update_status_once)
        
    def is_admin(self):
        """Check if the application is running with administrator privileges"""
        try:
            # Simple, fast admin check
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def run_as_admin(self):
        """Restart the application with administrator privileges"""
        if not self.is_admin():
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            self.root.quit()
            return True
        return False
        
    def create_log_file(self):
        """Create log file if it doesn't exist"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("Date,Time,Action,Username,Status\n")
    
    def log_action(self, action, status="Success"):
        """Log USB action to file"""
        timestamp = datetime.now()
        username = getpass.getuser()
        
        with open(self.log_file, 'a') as f:
            f.write(f"{timestamp.strftime('%Y-%m-%d')},{timestamp.strftime('%H:%M:%S')},{action},{username},{status}\n")
    
    def check_usb_status(self):
        """Check current USB status from registry"""
        try:
            # Cache admin status to avoid repeated calls
            if not hasattr(self, '_admin_cache'):
                self._admin_cache = self.is_admin()
                self._admin_cache_time = datetime.now()
            
            # Refresh admin cache every 30 seconds
            if (datetime.now() - self._admin_cache_time).seconds > 30:
                self._admin_cache = self.is_admin()
                self._admin_cache_time = datetime.now()
            
            if not self._admin_cache:
                return "Requires Admin"
            
            # Use cached registry value if available and recent
            if hasattr(self, '_registry_cache') and hasattr(self, '_registry_cache_time'):
                if (datetime.now() - self._registry_cache_time).seconds < 5:  # Cache for 5 seconds
                    return self._registry_cache
            
            # Read from registry
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SYSTEM\CurrentControlSet\Services\USBSTOR", 
                                0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "Start")
            winreg.CloseKey(key)
            
            # Determine status
            if value == 4:
                status = "Disabled"
            elif value == 3:
                status = "Enabled"
            else:
                status = "Unknown"
            
            # Cache the result
            self._registry_cache = status
            self._registry_cache_time = datetime.now()
            
            return status
            
        except Exception as e:
            # Return cached value if available, otherwise return error
            if hasattr(self, '_registry_cache'):
                return self._registry_cache
            return f"Error: {str(e)}"
    
    def update_usb_status(self):
        """Update USB status label"""
        try:
            # Only update if the GUI is still active
            if not self.root.winfo_exists():
                return
                
            status = self.check_usb_status()
            
            # Update status label and frame
            if status == "Enabled":
                self.status_label.config(text="● ENABLED", fg="#00C851", bg="#E8F5E8")
                self.status_frame.config(bg="#E8F5E8")
            elif status == "Disabled":
                self.status_label.config(text="● DISABLED", fg="#FF4444", bg="#FFEBEE")
                self.status_frame.config(bg="#FFEBEE")
            elif status == "Requires Admin":
                self.status_label.config(text="● REQUIRES ADMIN", fg="#FF8800", bg="#FFF3E0")
                self.status_frame.config(bg="#FFF3E0")
            elif status.startswith("Error:"):
                self.status_label.config(text="● ERROR", fg="#FF0000", bg="#FFEBEE")
                self.status_frame.config(bg="#FFEBEE")
            else:
                self.status_label.config(text="● UNKNOWN", fg="#FF8800", bg="#FFF3E0")
                self.status_frame.config(bg="#FFF3E0")
            
            # Schedule next update with longer interval to reduce CPU usage
            if self.root.winfo_exists():
                self.root.after(self.status_update_interval, self.update_usb_status)
                
        except Exception as e:
            # Log error and continue
            print(f"Status update error: {e}")
            # Try to schedule next update even if current one failed
            if self.root.winfo_exists():
                self.root.after(self.status_update_interval * 1.5, self.update_usb_status)  # Longer delay on error
    
    def update_status_once(self):
        """Update USB status only once on startup - prevents freezing"""
        try:
            if self.root.winfo_exists():
                status = self.check_usb_status()
                
                # Update status label and frame
                if status == "Enabled":
                    self.status_label.config(text="● ENABLED", fg="#00C851", bg="#E8F5E8")
                    self.status_frame.config(bg="#E8F5E8")
                elif status == "Disabled":
                    self.status_label.config(text="● DISABLED", fg="#FF4444", bg="#FFEBEE")
                    self.status_frame.config(bg="#FFEBEE")
                elif status == "Requires Admin":
                    self.status_label.config(text="● REQUIRES ADMIN", fg="#FF8800", bg="#FFF3E0")
                    self.status_frame.config(bg="#FFF3E0")
                elif status.startswith("Error:"):
                    self.status_label.config(text="● ERROR", fg="#FF0000", bg="#FFEBEE")
                    self.status_frame.config(bg="#FFEBEE")
                else:
                    self.status_label.config(text="● UNKNOWN", fg="#FF8800", bg="#FFF3E0")
                    self.status_frame.config(bg="#FFF3E0")
                
                print(f"Status updated once: {status}")
        except Exception as e:
            print(f"Status update error: {e}")
    
    def refresh_status_display(self):
        """Refresh the status display after USB operations"""
        try:
            status = self.check_usb_status()
            
            if status == "Enabled":
                self.status_label.config(text="● ENABLED", fg="#00C851", bg="#E8F5E8")
                self.status_frame.config(bg="#E8F5E8")
            elif status == "Disabled":
                self.status_label.config(text="● DISABLED", fg="#FF4444", bg="#FFEBEE")
                self.status_frame.config(bg="#FFEBEE")
            elif status == "Requires Admin":
                self.status_label.config(text="● REQUIRES ADMIN", fg="#FF8800", bg="#FFF3E0")
                self.status_frame.config(bg="#FFF3E0")
            elif status.startswith("Error:"):
                self.status_label.config(text="● ERROR", fg="#FF0000", bg="#FFEBEE")
                self.status_frame.config(bg="#FFEBEE")
            else:
                self.status_label.config(text="● UNKNOWN", fg="#FF8800", bg="#FFF3E0")
                self.status_frame.config(bg="#FFF3E0")
            
            print(f"Status refreshed: {status}")
        except Exception as e:
            print(f"Status refresh error: {e}")
    
    def keep_gui_responsive(self):
        """Keep GUI responsive by processing events periodically"""
        try:
            if self.root.winfo_exists():
                # Process any pending events
                self.root.update_idletasks()
                
                # Schedule next update
                self.root.after(1000, self.keep_gui_responsive)
        except Exception as e:
            print(f"GUI responsiveness error: {e}")
    
    def run_batch_file(self, batch_file, action):
        """Run batch file and log action"""
        try:
            # Check if running as admin
            if not self.is_admin():
                messagebox.showwarning("Administrator Required", 
                                     "This operation requires administrator privileges.\n\n"
                                     "The application will restart with elevated privileges.")
                self.run_as_admin()
                return
            
            # Get current directory and construct file paths
            current_dir = os.path.dirname(os.path.abspath(__file__))
            batch_path = os.path.join(current_dir, batch_file)
            ps1_path = os.path.join(current_dir, batch_file.replace('.bat', '.ps1'))
            
            # Try PowerShell script first if available
            if os.path.exists(ps1_path):
                try:
                    result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps1_path], 
                                          capture_output=True, text=True, 
                                          creationflags=subprocess.CREATE_NO_WINDOW)
                    
                    if result.returncode == 0:
                        self.log_action(action, "Success (PowerShell)")
                        self.refresh_status_display()
                        self.show_success_message(action, "PowerShell")
                        return
                    else:
                        # PowerShell failed, try batch file
                        pass
                except:
                    # PowerShell execution failed, try batch file
                    pass
            
            # Try batch file if PowerShell failed or not available
            if os.path.exists(batch_path):
                result = subprocess.run([batch_path], shell=True, capture_output=True, text=True, 
                                      creationflags=subprocess.CREATE_NO_WINDOW)
                
                if result.returncode == 0:
                    self.log_action(action, "Success (Batch)")
                    self.refresh_status_display()
                    self.show_success_message(action, "Batch")
                else:
                    error_msg = result.stderr if result.stderr else "Unknown error occurred"
                    messagebox.showerror("Error", f"Failed to {action.lower()} USB ports.\nError: {error_msg}")
                    self.log_action(action, f"Failed - {error_msg}")
            else:
                messagebox.showerror("Error", f"Neither batch file nor PowerShell script found for {action}")
                self.log_action(action, "Failed - No execution files found")
                
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.log_action(action, f"Failed - {error_msg}")
    
    def show_success_message(self, action, method):
        """Show enhanced success message after USB operation completion"""
        success_window = tk.Toplevel(self.root)
        success_window.title("USB Operation Completed Successfully")
        success_window.geometry("600x500")
        success_window.configure(bg="#E8F5E8")
        success_window.resizable(False, False)
        
        # Center the window and make it modal
        success_window.transient(self.root)
        success_window.grab_set()
        success_window.focus_force()
        
        # Center the window on screen
        x = (success_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (success_window.winfo_screenheight() // 2) - (500 // 2)
        success_window.geometry(f"600x500+{x}+{y}")
        
        # Main container
        main_container = tk.Frame(success_window, bg="#E8F5E8", padx=40, pady=40)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Success header with icon
        header_frame = tk.Frame(main_container, bg="#27AE60", relief="flat", bd=0)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Icon and title
        icon_label = tk.Label(header_frame, text="✅", font=("Segoe UI", 48),
                              bg="#27AE60", fg="white")
        icon_label.pack(pady=10)
        
        title_label = tk.Label(header_frame, text="OPERATION COMPLETED SUCCESSFULLY", 
                              bg="#27AE60", font=("Segoe UI", 20, "bold"), fg="white")
        title_label.pack(pady=(5, 5))
        
        subtitle_label = tk.Label(header_frame, text=f"USB ports have been {action.lower()}d", 
                            bg="#27AE60", font=("Segoe UI", 14), fg="#E8F5E8")
        subtitle_label.pack(pady=(0, 10))
        
        # Details section
        details_frame = tk.Frame(main_container, bg="#FFFFFF", relief="solid", bd=1)
        details_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Operation details
        details_label = tk.Label(details_frame, text="Operation Details:", 
                            bg="#FFFFFF", font=("Segoe UI", 14, "bold"), fg="#2C3E50")
        details_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Details text
        details_text = tk.Text(details_frame, bg="#FFFFFF", fg="#2C3E50", font=("Segoe UI", 11),
                              relief="flat", bd=0, height=6, wrap=tk.WORD)
        details_text.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        details_content = f"""Operation: {action} USB Ports
Method: {method} Script
Status: Completed Successfully
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
User: {getpass.getuser()}

What this means:
• USB storage devices are now {'blocked' if action == 'Disable' else 'accessible'}
• Changes have been applied to the Windows registry
• The operation has been logged for audit purposes
• USB {'input devices (keyboards, mice) continue to work normally' if action == 'Disable' else 'storage devices should now be accessible'}

Note: {'You may need to reconnect USB devices for changes to take effect' if action == 'Enable' else 'USB storage devices will be blocked until re-enabled'}"""
        
        details_text.insert(tk.END, details_content)
        details_text.config(state="disabled")
        
        # Current status section
        status_frame = tk.Frame(main_container, bg="#E8F5E8", relief="flat", bd=0)
        status_frame.pack(fill=tk.X, pady=(0, 25))
        
        status_title = tk.Label(status_frame, text="Current USB Status:", 
                               font=("Segoe UI", 12, "bold"), bg="#E8F5E8", fg="#2C3E50")
        status_title.pack(anchor="w", pady=(0, 10))
        
        # Get current status
        current_status = self.check_usb_status()
        status_color = "#00C851" if current_status == "Enabled" else "#FF4444" if current_status == "Disabled" else "#FF8800"
        
        status_display = tk.Label(status_frame, text=f"● {current_status}", 
                                 font=("Segoe UI", 16, "bold"), bg="#E8F5E8", fg=status_color)
        status_display.pack(anchor="w")
        
        # Buttons
        button_frame = tk.Frame(main_container, bg="#E8F5E8")
        button_frame.pack(pady=20)
        
        # View logs button
        logs_button = tk.Button(button_frame, text="📊 View Logs", 
                               command=lambda: [success_window.destroy(), self.view_logs()],
                               bg="#3498DB", fg="white", font=("Segoe UI", 12, "bold"),
                               width=15, height=2, relief="flat", bd=0,
                               activebackground="#2980B9", activeforeground="white",
                               cursor="hand2")
        logs_button.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_button = tk.Button(button_frame, text="✅ Close", 
                                command=success_window.destroy,
                                bg="#27AE60", fg="white", font=("Segoe UI", 12, "bold"),
                                width=15, height=2, relief="flat", bd=0,
                                activebackground="#229954", activeforeground="white",
                                cursor="hand2")
        close_button.pack(side=tk.LEFT, padx=10)
        
        # Auto-close after 10 seconds
        success_window.after(10000, success_window.destroy)
        
        # Play success sound (system beep)
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_OK)
        except:
            # Fallback to console beep if winsound not available
            print('\a')  # ASCII bell character
    
    def show_admin_warning(self):
        """Show warning about administrator privileges"""
        warning_window = tk.Toplevel(self.root)
        warning_window.title("Administrator Privileges Required")
        warning_window.geometry("500x400")
        warning_window.configure(bg="#FFF3E0")
        warning_window.resizable(False, False)
        
        # Center the window
        warning_window.transient(self.root)
        warning_window.grab_set()
        
        main_frame = tk.Frame(warning_window, bg="#FFF3E0", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Warning icon
        warning_icon = tk.Label(main_frame, text="⚠️", font=("Segoe UI", 48), 
                               bg="#FFF3E0", fg="#FF8800")
        warning_icon.pack(pady=(0, 20))
        
        # Warning title
        warning_title = tk.Label(main_frame, text="Administrator Access Required", 
                                font=("Segoe UI", 18, "bold"), bg="#FFF3E0", fg="#FF8800")
        warning_title.pack(pady=(0, 20))
        
        # Warning message
        warning_text = tk.Text(main_frame, bg="#FFFFFF", fg="#2C3E50", font=("Segoe UI", 11),
                              relief="solid", bd=1, height=8, wrap=tk.WORD)
        warning_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        warning_content = """This application requires administrator privileges to:
• Modify USB port settings
• Access Windows registry
• Execute system commands

To continue:
1. Close this application
2. Right-click on the application
3. Select "Run as administrator"
4. Restart the application

This ensures proper functionality and security."""
        
        warning_text.insert(tk.END, warning_content)
        warning_text.config(state="disabled")
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg="#FFF3E0")
        button_frame.pack(pady=20)
        
        restart_button = tk.Button(button_frame, text="🔄 Restart as Admin", 
                                  command=self.run_as_admin,
                                  bg="#FF8800", fg="white", font=("Segoe UI", 12, "bold"),
                                  width=15, height=2, relief="flat", bd=0,
                                  activebackground="#E67E22", activeforeground="white",
                                  cursor="hand2")
        restart_button.pack(side=tk.LEFT, padx=10)
        
        close_button = tk.Button(button_frame, text="❌ Close", 
                                command=warning_window.destroy,
                                bg="#95A5A6", fg="white", font=("Segoe UI", 12, "bold"),
                                width=15, height=2, relief="flat", bd=0,
                                activebackground="#7F8C8D", activeforeground="white",
                                cursor="hand2")
        close_button.pack(side=tk.LEFT, padx=10)
    
    def show_password_prompt(self, action, batch_file):
        """Show enhanced password prompt window"""
        password_window = tk.Toplevel(self.root)
        password_window.title("Security Verification Required")
        password_window.geometry("600x500")  # Larger window size
        password_window.configure(bg="#1A1A2E")
        password_window.resizable(False, False)
        
        # Center the window and make it modal
        password_window.transient(self.root)
        password_window.grab_set()
        password_window.focus_force()
        
        # Make sure window is on top
        password_window.attributes('-topmost', True)
        
        # Center the window on screen
        x = (password_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (password_window.winfo_screenheight() // 2) - (500 // 2)
        password_window.geometry(f"600x500+{x}+{y}")
        
        # Remove the flashing effect that causes lag
        # Instead, use a single highlight effect
        password_window.configure(highlightbackground="#FF4444", highlightthickness=5)
        
        # Main container
        main_container = tk.Frame(password_window, bg="#1A1A2E", padx=40, pady=40)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Security header with icon
        header_frame = tk.Frame(main_container, bg="#16213E", relief="flat", bd=0)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Icon and title
        icon_label = tk.Label(header_frame, text="🔐", font=("Segoe UI", 48),
                              bg="#16213E", fg="#FF4444")
        icon_label.pack(pady=10)
        
        title_label = tk.Label(header_frame, text="SECURITY VERIFICATION", 
                              bg="#16213E", font=("Segoe UI", 24, "bold"), fg="white")
        title_label.pack(pady=(5, 5))
        
        subtitle_label = tk.Label(header_frame, text=f"Enter password to {action} USB ports", 
                            bg="#16213E", font=("Segoe UI", 14), fg="#A8A8A8")
        subtitle_label.pack(pady=(0, 10))
        
        # Password entry section
        entry_frame = tk.Frame(main_container, bg="#0F3460", relief="flat", bd=0)
        entry_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Password label
        password_label = tk.Label(entry_frame, text="🔑 PASSWORD", 
                            bg="#0F3460", font=("Segoe UI", 18, "bold"), fg="#FF9900")
        password_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Password entry with clear styling
        password_entry = tk.Entry(entry_frame, show="●", font=("Segoe UI", 20),
                                 bg="#FFFFFF", fg="#000000", insertbackground="#000000",
                                 relief="solid", bd=3, width=20)
        password_entry.pack(fill=tk.X, padx=20, pady=15)
        password_entry.focus()
        
        # Show/Hide password toggle
        toggle_frame = tk.Frame(entry_frame, bg="#0F3460")
        toggle_frame.pack(anchor="e", padx=20, pady=(0, 15))
        
        show_password_var = tk.BooleanVar()
        
        def toggle_password():
            if show_password_var.get():
                password_entry.config(show="")
                show_toggle.config(text="🙈 Hide Password")
            else:
                password_entry.config(show="●")
                show_toggle.config(text="👁️ Show Password")
        
        show_toggle = tk.Checkbutton(toggle_frame, text="👁️ Show Password", 
                                    variable=show_password_var, command=toggle_password,
                                    bg="#0F3460", fg="#A8A8A8", selectcolor="#1A1A2E",
                                    font=("Segoe UI", 10), activebackground="#0F3460",
                                    activeforeground="#4ECDC4")
        show_toggle.pack()
        
        # Error label
        error_frame = tk.Frame(main_container, bg="#1A1A2E")
        error_frame.pack(fill=tk.X, pady=(0, 15))
        
        error_label = tk.Label(error_frame, text="", font=("Segoe UI", 11), 
                              fg="#FF6B6B", bg="#1A1A2E")
        error_label.pack()
        
        # Attempt counter
        attempt_frame = tk.Frame(main_container, bg="#1A1A2E")
        attempt_frame.pack(fill=tk.X, pady=(0, 15))
        
        attempt_count = 0
        attempt_label = tk.Label(attempt_frame, text="", font=("Segoe UI", 10), 
                                fg="#A8A8A8", bg="#1A1A2E")
        attempt_label.pack()
        
        def validate_password():
            nonlocal attempt_count
            if password_entry.get() == self.password:
                # Success animation
                success_frame = tk.Frame(main_container, bg="#27AE60", relief="flat", bd=0)
                success_frame.pack(fill=tk.X, pady=(0, 20))
                
                success_label = tk.Label(success_frame, text="✅ Password Verified Successfully!", 
                                       bg="#27AE60", font=("Segoe UI", 12, "bold"), fg="white")
                success_label.pack(pady=15)
                
                # Close window after delay
                password_window.after(1000, lambda: [password_window.destroy(), self.run_batch_file(batch_file, action)])
            else:
                attempt_count += 1
                error_label.config(text="❌ Incorrect password. Please try again.")
                attempt_label.config(text=f"Attempts: {attempt_count}/3")
                
                # Clear password field and focus
                password_entry.delete(0, tk.END)
                password_entry.focus()
                
                # Shake animation for wrong password
                self.shake_window(password_window)
                
                # Lock after 3 attempts
                if attempt_count >= 3:
                    error_label.config(text="🚫 Too many failed attempts. Please restart the application.")
                    password_entry.config(state="disabled")
                    ok_button.config(state="disabled")
                    show_toggle.config(state="disabled")
        
        def on_enter(event):
            validate_password()
        
        # Bind Enter key and Escape key
        password_entry.bind('<Return>', on_enter)
        password_window.bind('<Escape>', lambda e: password_window.destroy())
        
        # Buttons frame
        button_frame = tk.Frame(main_container, bg="#1A1A2E")
        button_frame.pack(pady=20)
        
        # Verify button
        ok_button = tk.Button(button_frame, text="🔓 Verify", command=validate_password, 
                             bg="#4ECDC4", fg="white", font=("Segoe UI", 12, "bold"),
                             width=10, height=1, relief="flat", bd=0,
                             activebackground="#45B7AF", activeforeground="white",
                             cursor="hand2")
        ok_button.pack(side=tk.LEFT, padx=10)
        
        # Cancel button
        cancel_button = tk.Button(button_frame, text="❌ Cancel", command=password_window.destroy,
                                 bg="#E94560", fg="white", font=("Segoe UI", 12, "bold"),
                                 width=10, height=1, relief="flat", bd=0,
                                 activebackground="#D13B56", activeforeground="white",
                                 cursor="hand2")
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Help button
        help_button = tk.Button(button_frame, text="❓ HELP", 
                               command=lambda: self.show_password_help(),
                               bg="#533483", fg="white", font=("Segoe UI", 10),
                               width=10, height=2, relief="flat", bd=0,
                               activebackground="#4A2F75", activeforeground="white",
                               cursor="hand2")
        help_button.pack(side=tk.LEFT, padx=15)
        
        # Footer with additional security info
        footer_frame = tk.Frame(main_container, bg="#1A1A2E")
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        footer_text = tk.Label(footer_frame, text="🔒 Secure USB Port Management | Administrator Access Required", 
                              font=("Segoe UI", 9), bg="#1A1A2E", fg="#A8A8A8")
        footer_text.pack()
    
    def shake_window(self, window):
        """Shake animation for wrong password"""
        def shake():
            x = window.winfo_x()
            y = window.winfo_y()
            for i in range(5):
                window.geometry(f"+{x+5}+{y}")
                window.update()
                window.after(50)
                window.geometry(f"+{x-5}+{y}")
                window.update()
                window.after(50)
            window.geometry(f"+{x}+{y}")
        
        shake()
    
    def show_password_help(self):
        """Show password help information"""
        help_window = tk.Toplevel()
        help_window.title("Password Help")
        help_window.geometry("400x300")
        help_window.configure(bg="#1A1A2E")
        help_window.resizable(False, False)
        
        # Center the help window
        help_window.transient(self.root)
        help_window.grab_set()
        
        main_frame = tk.Frame(help_window, bg="#1A1A2E", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Help icon
        help_icon = tk.Label(main_frame, text="❓", font=("Segoe UI", 48), 
                            bg="#1A1A2E", fg="#4ECDC4")
        help_icon.pack(pady=(0, 20))
        
        # Help title
        help_title = tk.Label(main_frame, text="Password Information", 
                             font=("Segoe UI", 16, "bold"), bg="#1A1A2E", fg="white")
        help_title.pack(pady=(0, 20))
        
        # Help content
        help_content = tk.Text(main_frame, bg="#16213E", fg="white", font=("Segoe UI", 10),
                              relief="flat", bd=0, height=8, wrap=tk.WORD)
        help_content.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        help_text = """Default Password: admin123

Security Features:
• Password is required for all USB operations
• Maximum 3 attempts allowed
• Session-based security
• Administrator privileges required

Tips:
• Keep your password secure
• Don't share with unauthorized users
• Contact system administrator if locked out"""
        
        help_content.insert(tk.END, help_text)
        help_content.config(state="disabled")
        
        # Close button
        close_button = tk.Button(main_frame, text="Close", command=help_window.destroy,
                                bg="#4ECDC4", fg="white", font=("Segoe UI", 12, "bold"),
                                width=15, height=2, relief="flat", bd=0,
                                activebackground="#45B7AF", activeforeground="white")
        close_button.pack()
    
    def view_logs(self):
        """Show logs in a new window"""
        log_window = tk.Toplevel(self.root)
        log_window.title("USB Activity Logs")
        log_window.geometry("900x700")
        log_window.configure(bg="#ECF0F1")
        log_window.resizable(True, True)
        
        # Title bar
        title_frame = tk.Frame(log_window, bg="#2C3E50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📊 USB Activity Logs", 
                              font=("Segoe UI", 20, "bold"), bg="#2C3E50", fg="white")
        title_label.pack(expand=True)
        
        # Create Treeview for logs
        tree_frame = tk.Frame(log_window, bg="#ECF0F1")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                       background="#FFFFFF",
                       foreground="#2C3E50",
                       rowheight=30,
                       fieldbackground="#FFFFFF",
                       font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                       background="#34495E",
                       foreground="white",
                       font=("Segoe UI", 11, "bold"))
        
        # Create Treeview with scrollbars
        tree = ttk.Treeview(tree_frame, columns=("Date", "Time", "Action", "Username", "Status"), 
                           show="headings", height=20)
        
        # Define columns
        tree.heading("Date", text="📅 Date")
        tree.heading("Time", text="🕒 Time")
        tree.heading("Action", text="⚡ Action")
        tree.heading("Username", text="👤 Username")
        tree.heading("Status", text="📊 Status")
        
        # Column widths
        tree.column("Date", width=120, anchor="center")
        tree.column("Time", width=100, anchor="center")
        tree.column("Action", width=120, anchor="center")
        tree.column("Username", width=150, anchor="center")
        tree.column("Status", width=100, anchor="center")
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Load logs
        self.load_logs_to_tree(tree)
        
        # Buttons
        button_frame = tk.Frame(log_window, bg="#ECF0F1")
        button_frame.pack(pady=30)
        
        refresh_button = tk.Button(button_frame, text="🔄 Refresh Logs", 
                                 command=lambda: self.load_logs_to_tree(tree),
                                 bg="#3498DB", fg="white", font=("Segoe UI", 12, "bold"),
                                 width=18, height=2, relief="flat", bd=0,
                                 activebackground="#2980B9", activeforeground="white",
                                 cursor="hand2")
        refresh_button.pack(side=tk.LEFT, padx=15)
        
        back_button = tk.Button(button_frame, text="← Back to Dashboard", 
                               command=log_window.destroy,
                               bg="#95A5A6", fg="white", font=("Segoe UI", 12, "bold"),
                               width=18, height=2, relief="flat", bd=0,
                               activebackground="#7F8C8D", activeforeground="white",
                               cursor="hand2")
        back_button.pack(side=tk.LEFT, padx=15)
    
    def load_logs_to_tree(self, tree):
        """Load logs from file to treeview"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()
                    
                # Skip header line and add data
                for line in lines[1:]:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 5: # Ensure all columns are present
                            tree.insert("", "end", values=(parts[0], parts[1], parts[2], parts[3], parts[4]))
                        elif len(parts) >= 4: # Handle old format logs
                            tree.insert("", "end", values=(parts[0], parts[1], parts[2], parts[3], "N/A"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load logs: {str(e)}")
    
    def open_project_info(self):
        """Open project information in default browser"""
        try:
            # Open the README file instead since project_info.html was removed
            current_dir = os.path.dirname(os.path.abspath(__file__))
            readme_path = os.path.join(current_dir, "README.md")
            
            if os.path.isfile(readme_path):
                # Try to open with default markdown viewer or text editor
                os.startfile(readme_path)
            else:
                messagebox.showinfo("Information", "README.md file not found. Please check the documentation.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open documentation: {str(e)}")
    
    def on_button_hover(self, event, button, hover_color):
        """Button hover effect"""
        button.configure(bg=hover_color)
    
    def on_button_leave(self, event, button, original_color):
        """Button leave effect"""
        button.configure(bg=original_color)
    
    def setup_gui(self):
        """Setup the main GUI"""
        self.root.title("USB Physical Security - Enhanced Version")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#ECF0F1")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#ECF0F1")
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        
        # Header section
        header_frame = tk.Frame(main_container, bg="#2C3E50", relief="flat", bd=0)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Title and subtitle
        title_label = tk.Label(header_frame, text="🔒 USB PHYSICAL SECURITY", 
                              font=("Segoe UI", 28, "bold"), bg="#2C3E50", fg="white")
        title_label.pack(pady=(30, 10))
        
        subtitle_label = tk.Label(header_frame, text="Enhanced Version - Professional Security Management", 
                                font=("Segoe UI", 14), bg="#2C3E50", fg="#BDC3C7")
        subtitle_label.pack(pady=(0, 30))
        
        # Status section
        status_container = tk.Frame(main_container, bg="#ECF0F1")
        status_container.pack(fill=tk.X, pady=(0, 30))
        
        status_title = tk.Label(status_container, text="Current USB Status:", 
                               font=("Segoe UI", 16, "bold"), bg="#ECF0F1", fg="#2C3E50")
        status_title.pack(anchor="w", pady=(0, 10))
        
        self.status_frame = tk.Frame(status_container, bg="#E8F5E8", relief="flat", bd=0)
        self.status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = tk.Label(self.status_frame, text="● CHECKING...", 
                                    font=("Segoe UI", 18, "bold"), bg="#E8F5E8", fg="#2C3E50")
        self.status_label.pack(pady=20)
        
        # Buttons section
        buttons_frame = tk.Frame(main_container, bg="#ECF0F1")
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # Button configurations with modern design
        button_configs = [
            ("🔓 Enable USB Ports", "#27AE60", "#229954", lambda: self.show_password_prompt("Enable", "unblock_usb.bat")),
            ("🔒 Disable USB Ports", "#E74C3C", "#C0392B", lambda: self.show_password_prompt("Disable", "block_usb.bat")),
            ("📊 View Activity Logs", "#3498DB", "#2980B9", self.view_logs),
            ("📖 View Documentation", "#F39C12", "#E67E22", self.open_project_info),
            ("🚪 Exit Application", "#95A5A6", "#7F8C8D", self.root.quit)
        ]
        
        # Create buttons in a grid layout
        for i, (text, bg_color, hover_color, command) in enumerate(button_configs):
            row = i // 2
            col = i % 2
            
            button = tk.Button(buttons_frame, text=text, command=command,
                             bg=bg_color, fg="white", font=("Segoe UI", 14, "bold"),
                             width=25, height=3, relief="flat", bd=0, cursor="hand2",
                             activebackground=hover_color, activeforeground="white")
            button.grid(row=row, column=col, padx=15, pady=15, sticky="ew")
            
            # Bind hover events
            button.bind("<Enter>", lambda e, b=button, c=hover_color: self.on_button_hover(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=bg_color: self.on_button_leave(e, b, c))
        
        # Configure grid weights for buttons
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Footer
        footer_frame = tk.Frame(main_container, bg="#ECF0F1")
        footer_frame.pack(fill=tk.X, pady=(30, 0))
        
        footer_text = tk.Label(footer_frame, text="© 2025 USB Physical Security - Enhanced Version | Professional Security Management", 
                              font=("Segoe UI", 10), bg="#ECF0F1", fg="#7F8C8D")
        footer_text.pack()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = USBPhysicalSecurity()
    app.run()
