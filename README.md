# USB Physical Security - Enhanced Version

A professional Windows application for managing USB port security with enhanced features, better error handling, and improved user experience.

## 🚀 Features

- **USB Port Management**: Enable/disable USB storage devices
- **Real-time Status Monitoring**: Live USB port status updates
- **Enhanced Security**: Password-protected operations with attempt limiting
- **Comprehensive Logging**: Detailed activity logs with status tracking
- **Modern UI**: Professional interface with hover effects and animations
- **Dual Execution Methods**: Supports both batch files and PowerShell scripts
- **Administrator Privilege Management**: Automatic detection and elevation

## 📋 Requirements

- **Operating System**: Windows 10/11 (64-bit recommended)
- **Python**: Python 3.7 or higher
- **Privileges**: Administrator privileges required for USB operations
- **Dependencies**: No external packages required (uses Python standard library)

## 🛠️ Installation

1. **Download the application** to your desired location
2. **Extract all files** to a folder
3. **Run as Administrator**: Right-click on `usb_physical_security.py` and select "Run as administrator"

## 🔐 Default Credentials

- **Username**: Not required (uses current Windows user)
- **Password**: `admin123`

⚠️ **Security Note**: Change the default password in the source code for production use.

## 🚨 Important Notes

### Administrator Privileges Required
This application requires administrator privileges to:
- Modify Windows registry settings
- Execute system commands
- Control USB port access

### USB Storage vs. USB Devices
- **USB Storage Devices**: Flash drives, external hard drives, memory cards
- **USB Input Devices**: Keyboards, mice, game controllers (unaffected)

## 📖 Usage Instructions

### 1. Starting the Application
```bash
# Method 1: Direct execution (requires admin)
python usb_physical_security.py

# Method 2: Run as administrator from Windows
# Right-click → Run as administrator
```

### 2. Main Operations

#### Enable USB Ports
1. Click "🔓 Enable USB Ports"
2. Enter password: `admin123`
3. Click "🔓 Verify"
4. Wait for success confirmation

#### Disable USB Ports
1. Click "🔒 Disable USB Ports"
2. Enter password: `admin123`
3. Click "🔓 Verify"
4. Wait for success confirmation

#### View Logs
1. Click "📊 View Activity Logs"
2. Browse through USB activity history
3. Use refresh button to update logs

### 3. Status Monitoring
The application displays real-time USB status:
- 🟢 **ENABLED**: USB storage devices are accessible
- 🔴 **DISABLED**: USB storage devices are blocked
- 🟡 **REQUIRES ADMIN**: Administrator privileges needed
- 🔴 **ERROR**: Operation failed

## 🔧 Troubleshooting

### Common Issues

#### 1. "Administrator Privileges Required"
**Problem**: Application shows "REQUIRES ADMIN" status
**Solution**: 
- Close the application
- Right-click on `usb_physical_security.py`
- Select "Run as administrator"

#### 2. "Failed to Enable/Disable USB Ports"
**Problem**: Operations fail with error messages
**Solutions**:
- Ensure running as administrator
- Check Windows Defender/Antivirus settings
- Verify registry access permissions
- Try PowerShell scripts as alternative

#### 3. "Batch File Not Found"
**Problem**: Execution files missing
**Solution**: Ensure all files are in the same directory:
- `usb_physical_security.py`
- `block_usb.bat`
- `unblock_usb.bat`
- `block_usb.ps1`
- `unblock_usb.ps1`

#### 4. PowerShell Execution Policy
**Problem**: PowerShell scripts blocked
**Solution**: Run PowerShell as administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Advanced Troubleshooting

#### Registry Access Issues
If registry operations fail:
1. Check Group Policy settings
2. Verify Windows Defender settings
3. Check for corporate security policies
4. Ensure Windows Update is current

#### Antivirus Interference
Some antivirus software may block registry modifications:
1. Add application to antivirus exclusions
2. Temporarily disable real-time protection
3. Check antivirus logs for blocked operations

## 📁 File Structure

```
USB-Physical-Security/
├── usb_physical_security.py    # Main application
├── block_usb.bat              # Batch file for blocking USB
├── unblock_usb.bat            # Batch file for unblocking USB
├── block_usb.ps1              # PowerShell script for blocking USB
├── unblock_usb.ps1            # PowerShell script for unblocking USB
├── requirements.txt            # Python dependencies (none required)
├── README.md                  # This file
├── project_info.html          # Project information
└── usb_activity.log          # Activity log file (auto-generated)
```

## 🔒 Security Features

- **Password Protection**: All USB operations require authentication
- **Attempt Limiting**: Maximum 3 password attempts per session
- **Session Security**: Password verification for each operation
- **Audit Logging**: Complete activity tracking with timestamps
- **Privilege Escalation**: Automatic administrator privilege detection

## 📊 Logging

The application maintains detailed logs in `usb_activity.log`:
- **Date**: Operation date (YYYY-MM-DD)
- **Time**: Operation time (HH:MM:SS)
- **Action**: Operation performed (Enable/Disable)
- **Username**: Windows user who performed the operation
- **Status**: Operation result (Success/Failed + details)

## 🚀 Performance Tips

1. **Run as Administrator**: Always run with elevated privileges
2. **Close Unnecessary Applications**: Free up system resources
3. **Regular Updates**: Keep Windows and Python updated
4. **Monitor Logs**: Check logs for any recurring issues

## 🆘 Support

### Getting Help
1. Check this README for common solutions
2. Review the activity logs for error details
3. Ensure administrator privileges are active
4. Verify all files are present and accessible

### Error Reporting
When reporting issues, include:
- Windows version and build
- Python version
- Error messages from the application
- Contents of the activity log
- Steps to reproduce the issue

## 📝 Changelog

### Version 2.0 (Enhanced)
- ✅ Improved error handling and user feedback
- ✅ PowerShell script alternatives
- ✅ Better administrator privilege management
- ✅ Enhanced logging with status tracking
- ✅ Modern UI with hover effects
- ✅ Comprehensive troubleshooting guide

### Version 1.0 (Original)
- Basic USB port management
- Simple batch file execution
- Basic logging functionality

## 📄 License

This project is provided as-is for educational and security purposes. Use responsibly and in accordance with your organization's security policies.

## ⚠️ Disclaimer

This application modifies Windows registry settings and system configurations. Use at your own risk and ensure you have proper backups. The developers are not responsible for any data loss or system issues that may occur.

---

**USB Physical Security - Enhanced Version**  
*Professional USB Port Management for Windows*
