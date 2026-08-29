MountForge
Android Recovery Data Mount Patch Tool
A lightweight Python tool designed for Android custom recovery development.
MountForge patches specific fstab encryption-related configurations inside large Android images such as super.img.
Its primary purpose is to assist developers experimenting with modified recoveries where /data fails to mount because of incompatible or unsupported encryption-related fstab options.
Supported recovery development scenarios include:
TWRP
OrangeFox Recovery (OFRP)
SHRP
Other custom or modified Android recoveries
⚠️ Important: This tool does NOT decrypt existing /data, recover passwords, bypass lock-screen credentials, or extract encryption keys.
It only modifies supported fstab configuration strings inside an Android image.
Whether /data can successfully mount afterwards depends on:
Device configuration
Android version
Filesystem
Recovery kernel
Encryption implementation
Metadata configuration
Recovery compatibility
✨ Features
Designed for custom recovery development
Processes very large images safely
No full-image memory mapping
Reads the image in 64 MB chunks
Searches for supported encryption-related fstab patterns
Patches exact matching configurations
Preserves the original byte length
Shows the offset of every successful patch
Uses overlap between chunks to avoid missing patterns at boundaries
Suitable for Android dynamic partition experimentation
🎯 Purpose
Some custom recoveries may fail to mount /data correctly because the recovery environment does not fully support the encryption or metadata configuration used by the stock firmware.
This tool searches for specific fstab configurations containing options such as:
inlinecrypt
fileencryption
metadata_encryption
keydirectory=/metadata/vold/metadata_encryption
When one of the exact patterns supported by the script is found, it patches the configuration inside the supplied image.
The goal is to support recovery development and testing where a developer needs to experiment with /data mounting behavior.
⚠️ Important Limitation
A patched fstab does not automatically mean that /data will mount.
Successful mounting may still require:
Correct recovery kernel
Correct device tree
Required filesystem drivers
Correct logical partition handling
Compatible metadata partition
Proper Android encryption support
Correct SELinux configuration
Correct fstab paths and mount flags
This tool only changes the supported fstab patterns.
📦 Requirements
Python 3
Linux or Termux
Original firmware image compatible with your exact device
⭐ Recommended Source Image
The safest approach is to start with the original stock firmware matching your device.
For devices using dynamic partitions, the required configuration may exist inside:
super.img
Always use firmware matching:
Exact device model
Correct hardware variant
Compatible Android version
Compatible bootloader revision
❌ Never use images from unrelated devices.
💾 Step 1 — Create a Backup
Before patching:
cp super.img super_backup.img
Keep the original image untouched.
The script modifies the supplied image directly.
🔧 Step 2 — Run MountForge
Execute:
python3 patch_super_chunked.py super.img
The image is patched in place.
Example:
super.img  →  patched directly
Always keep:
super_backup.img
as your untouched backup.
📊 Example Output
Successful patch:
File size: 8589934592 bytes
  patched at offset 123456789
DONE. Total occurrences patched: 1
No supported pattern found:
File size: 8589934592 bytes
DONE. Total occurrences patched: 0
WARNING: nothing matched — no changes made.
🔍 How It Works
The image is processed in small sections:
┌───────────────────────────────┐
│           super.img           │
└───────────────┬───────────────┘
                │
                ▼
         Read 64 MB chunk
                │
                ▼
   Search supported fstab data
                │
                ▼
       Exact pattern found?
           │           │
          YES          NO
           │           │
           ▼           ▼
      Patch bytes   Continue
           │
           ▼
     Next image chunk
The script keeps a small overlap between chunks.
This ensures that a matching configuration is not missed when it begins at the end of one chunk and continues into the next.
📱 Custom Recovery Use
MountForge may be useful while developing a modified recovery when:
Recovery boots
      │
      ▼
/data fails to mount
      │
      ▼
Check fstab configuration
      │
      ▼
Check filesystem and metadata support
      │
      ▼
Test compatible recovery configuration
      │
      ▼
Rebuild or test recovery
It can be included in a recovery development workflow alongside:
Device tree modifications
Recovery fstab testing
Kernel configuration
Filesystem driver testing
Dynamic partition testing
Metadata partition handling
🗑️ IMPORTANT — FORMAT DATA MAY BE REQUIRED
After modifying encryption-related fstab settings, the existing /data layout may no longer be compatible with the modified recovery configuration.
If /data cannot mount correctly after testing the modified recovery or image, a Format Data operation may be required.
⚠️ WARNING: Formatting /data permanently deletes user data, installed applications, internal storage files, and encryption-related metadata.
Recommended testing workflow:
Boot modified recovery
        │
        ▼
Try to mount /data
        │
        ▼
Does /data mount correctly?
      │             │
     YES            NO
      │             │
      ▼             ▼
 Continue      Check recovery,
 testing       fstab and metadata
                    │
                    ▼
             If a clean data layout
             is required for testing
                    │
                    ▼
                FORMAT DATA
                    │
                    ▼
              Reboot recovery
                    │
                    ▼
              Test /data again
🔥 TWRP / OrangeFox Format Data
When a clean /data partition is required during development:
Boot into the modified recovery.
Back up important files first.
Use the recovery's Format Data function.
Confirm the operation when requested.
Reboot the recovery.
Test /data mounting again.
⚠️ Format Data permanently erases all data stored in /data.
Always create a backup before formatting.
⚠️ Format Data Does Not Fix Everything
Formatting /data is not guaranteed to solve every mounting problem.
If /data still fails to mount after formatting, investigate:
Recovery kernel support
Device tree configuration
Recovery fstab
Filesystem drivers
Dynamic/logical partition handling
Metadata partition handling
SELinux configuration
Android version compatibility
📲 Samsung / Odin Workflow
For Samsung devices, always begin with firmware matching your exact device.
Typical Samsung firmware archives include:
BL_*.tar.md5
AP_*.tar.md5
CP_*.tar.md5
CSC_*.tar.md5
HOME_CSC_*.tar.md5
General development workflow:
Original Samsung Firmware
          │
          ▼
Extract required image
          │
          ▼
Create backup
          │
          ▼
Run MountForge
          │
          ▼
Verify modifications
          │
          ▼
Repackage correctly
          │
          ▼
Flash/test using a compatible
development workflow
⚠️ Do not mix partitions from different device models.
Always keep the complete original firmware available so the device can be restored if testing fails.
🧩 Supported Patterns
The current version of MountForge supports only the exact byte patterns defined in:
patch_super_chunked.py
The script searches for specific combinations of:
inlinecrypt
fileencryption
metadata_encryption
keydirectory
Checkpoint configuration
If your device uses another format, the script may report:
WARNING: nothing matched — no changes made.
This does not necessarily mean encryption is absent.
It only means that the image does not contain one of the exact patterns currently supported by the script.
🛡️ Safety
Before testing:
✅ Make a complete backup
✅ Keep the original firmware
✅ Use the exact device model
✅ Test on a copy of the image
✅ Verify the partition layout
✅ Verify recovery compatibility
⚠️ Back up important data before Format Data
⚠️ Format Data permanently erases /data
❌ Do not use images from another device
❌ Do not assume a successful patch guarantees /data mounting
⚠️ Disclaimer
This project is intended for:
Android development
Custom recovery development
TWRP development
OrangeFox development
SHRP development
Dynamic partition research
fstab experimentation
This project does not decrypt user data or recover encryption credentials.
The author is not responsible for:
Bootloops
Data loss
Corrupted partitions
Recovery boot failures
Failed /data mounting
Incorrect firmware packaging
Device damage caused by incompatible images
Always keep an untouched copy of the original firmware before testing.
🚀 Quick Usage
# Create backup
cp super.img super_backup.img

# Run MountForge
python3 patch_super_chunked.py super.img
📂 Project Structure
MountForge/
│
├── patch_super_chunked.py
├── README.md
└── LICENSE
🤝 Credits
Created for Android custom recovery development and experimentation with:
TWRP
OrangeFox Recovery
SHRP
Android Dynamic Partitions
Recovery fstab
/data mounting
Samsung firmware testing
📄 License
This project is released under the MIT License.
See the LICENSE file for more information.
