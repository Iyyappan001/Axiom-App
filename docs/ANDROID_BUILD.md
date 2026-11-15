# Build and install the Android APK

The supported development path is a debug APK built by Buildozer on Linux. Buildozer reads [buildozer.spec](../buildozer.spec); the root [main.py](../main.py) is the Android entry point.

## GitHub Actions build

1. Push the project to GitHub.
2. Open **Actions → Android debug APK**.
3. Select **Run workflow**, or push to `main`.
4. Open the completed workflow run and download the `lifeos-debug-apk` artifact.
5. Unzip it to obtain the `.apk` file.

## Install with ADB

Enable Developer options and USB debugging on the phone, connect it by USB, then run:

```bash
adb devices
adb install -r bin/lifeos-*-debug.apk
```

If Android reports an existing incompatible signature, uninstall the old debug build first:

```bash
adb uninstall org.lifeos.lifeos
adb install bin/lifeos-*-debug.apk
```

## Install without ADB

Transfer the APK to the phone, open it from Files, allow installation from that source when prompted, and install it. Use only a debug APK you built yourself; do not enter real financial data until the physical-device security checks in [TEST_PLAN.md](./TEST_PLAN.md) pass.

## Current limitations

This is a debug build. SQLCipher, Android Keystore, biometric unlock, backup/restore, and release signing still require implementation and physical-device validation before a production APK.
