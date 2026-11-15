# Architecture

LifeOS is a modular monolith. Kivy screens call application services, services enforce domain rules, repositories persist through the encrypted database boundary, and adapters isolate Android APIs and market-price providers.

## Feasibility gates

1. Launch a minimal Kivy APK on physical Android hardware.
2. Package and verify SQLCipher encryption on-device.
3. Verify Keystore and BiometricPrompt behavior through the native bridge.
4. Restore an encrypted backup on a second physical device.

Until these gates pass, use fictional data only.
