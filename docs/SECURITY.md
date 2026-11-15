# Security baseline

The database key is random, wrapped by a non-exportable Android Keystore AES-GCM key, and released only after biometric/device-credential authentication. Database files remain in private app storage. Sensitive fields must never appear in logs, fixtures, or network requests.

MVP has no SMS, contacts, location, accessibility, microphone, camera, or broad storage permission. Backup/restore must be authenticated, versioned, encrypted, and tested on another device before release.
