/**
 * SmartPassLib v1.0.3 - Client-side smart password generator
 * Cross-platform deterministic password generation
 * Same secret + same length = same password across all platforms
 * Decentralized by design — no central servers, no cloud dependency, no third-party trust required
 *
 * Compatible with smartpasslib Python/Go/Kotlin/C# implementations
 *
 * Key derivation:
 * - Private key: 30 iterations of SHA-256 (used for password generation)
 * - Public key: 60 iterations of SHA-256 (used for verification, stored locally)
 *
 * Secret phrase:
 *   - is not transferred anywhere
 *   - is not stored anywhere
 *   - is required to generate the private key when creating a smart password
 *
 * Ecosystem:
 *   - Core library (Python): https://github.com/smartlegionlab/smartpasslib
 *   - Core library (JS): https://github.com/smartlegionlab/smartpasslib-js
 *   - Core library (Kotlin): https://github.com/smartlegionlab/smartpasslib-kotlin
 *   - Core library (Go): https://github.com/smartlegionlab/smartpasslib-go
 *   - Core library (C#): https://github.com/smartlegionlab/smartpasslib-csharp
 *   - Desktop Python: https://github.com/smartlegionlab/smart-password-manager-desktop
 *   - Desktop C#: https://github.com/smartlegionlab/SmartPasswordManagerCsharpDesktop
 *   - CLI Manager Python: https://github.com/smartlegionlab/clipassman
 *   - CLI Manager C#: https://github.com/smartlegionlab/SmartPasswordManagerCsharpCli
 *   - CLI Generator Python: https://github.com/smartlegionlab/clipassgen
 *   - CLI Generator C#: https://github.com/smartlegionlab/SmartPasswordGeneratorCsharpCli
 *   - Web: https://github.com/smartlegionlab/smart-password-manager-web
 *   - Android: https://github.com/smartlegionlab/smart-password-manager-android
 *
 * Author: Alexander Suvorov https://github.com/smartlegionlab
 * License: BSD 3-Clause https://github.com/smartlegionlab/smartpasslib-js/blob/master/LICENSE
 * Copyright (c) 2026, Alexander Suvorov. All rights reserved.
 */

const SmartPassLib = (function() {
    'use strict';

    // Character set for password generation (must match smartpasslib)
    const CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$&*-_";
    const PRIVATE_ITERATIONS = 30;  // For private key (password generation)
    const PUBLIC_ITERATIONS = 60;   // For public key (verification, stored on server)
    const VERSION = '1.0.3';

    /**
     * SHA-256 hash using Web Crypto API
     * @param {string} text - Text to hash
     * @returns {Promise<string>} Hex string of hash
     */
    async function sha256(text) {
        const encoder = new TextEncoder();
        const hashBuffer = await crypto.subtle.digest('SHA-256', encoder.encode(text));
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Convert hex string to byte array
     * @param {string} hex - Hex string
     * @returns {number[]} Byte array
     */
    function hexToBytes(hex) {
        const bytes = [];
        for (let i = 0; i < hex.length; i += 2) {
            bytes.push(parseInt(hex.substr(i, 2), 16));
        }
        return bytes;
    }

    /**
     * Generate a key from secret phrase with specified number of iterations
     * @param {string} secret - Secret phrase
     * @param {number} iterations - Number of hash iterations
     * @returns {Promise<string>} Key hex string
     */
    async function generateKey(secret, iterations) {
        if (!secret || secret.length < 12) {
            throw new Error(`Secret phrase must be at least 12 characters. Current: ${secret ? secret.length : 0}`);
        }

        let allHash = await sha256(secret);

        for (let i = 0; i < iterations; i++) {
            const tempString = `${allHash}:${secret}:${i}`;
            allHash = await sha256(tempString);
        }

        return allHash;
    }

    /**
     * Generate private key from secret phrase (30 iterations)
     * Used for password generation, never stored or transmitted
     * @param {string} secret - Secret phrase (minimum 12 characters)
     * @returns {Promise<string>} Private key hex string (64 characters = 256 bits)
     */
    async function generatePrivateKey(secret) {
        return await generateKey(secret, PRIVATE_ITERATIONS);
    }

    /**
     * Generate public key from secret phrase (60 iterations)
     * Used for verification, stored on server
     * @param {string} secret - Secret phrase (minimum 12 characters)
     * @returns {Promise<string>} Public key hex string
     */
    async function generatePublicKey(secret) {
        return await generateKey(secret, PUBLIC_ITERATIONS);
    }

    /**
     * Verify that a secret phrase matches a stored public key
     * @param {string} secret - Secret phrase to verify
     * @param {string} publicKey - Public key to check against
     * @returns {Promise<boolean>} True if valid
     */
    async function verifySecret(secret, publicKey) {
        const computedKey = await generatePublicKey(secret);
        return computedKey === publicKey;
    }

    /**
     * Generate deterministic smart password from private key
     * @param {string} privateKey - Private key hex string (from generatePrivateKey)
     * @param {number} length - Desired password length (min 12, max 1000)
     * @returns {Promise<string>} Generated password
     */
    async function generatePasswordFromPrivateKey(privateKey, length) {
        let result = [];
        let counter = 0;

        while (result.length < length) {
            const data = `${privateKey}:${counter}`;
            const hashHex = await sha256(data);
            const hashBytes = hexToBytes(hashHex);

            for (let i = 0; i < hashBytes.length && result.length < length; i++) {
                result.push(CHARS[hashBytes[i] % CHARS.length]);
            }
            counter++;
        }

        return result.join('');
    }

    /**
     * Generate deterministic smart password directly from secret phrase
     * This is the main method for end users
     * @param {string} secret - Secret phrase (minimum 12 characters)
     * @param {number} length - Desired password length (min 12, max 1000)
     * @returns {Promise<string>} Generated password
     */
    async function generateSmartPassword(secret, length) {
        if (!secret || secret.length < 12) {
            throw new Error(`Secret phrase must be at least 12 characters. Current: ${secret ? secret.length : 0}`);
        }
        if (length < 12) {
            throw new Error(`Password length must be at least 12 characters. Current: ${length}`);
        }
        if (length > 1000) {
            throw new Error(`Password length cannot exceed 1000 characters. Current: ${length}`);
        }

        const privateKey = await generatePrivateKey(secret);
        return await generatePasswordFromPrivateKey(privateKey, length);
    }

    /**
     * Generate strong random password (cryptographically secure)
     * @param {number} length - Desired password length (min 12, max 1000)
     * @returns {Promise<string>} Generated random password
     */
    async function generateStrongPassword(length) {
        if (length < 12) {
            throw new Error(`Password length must be at least 12 characters. Current: ${length}`);
        }
        if (length > 1000) {
            throw new Error(`Password length cannot exceed 1000 characters. Current: ${length}`);
        }

        const array = new Uint8Array(length);
        crypto.getRandomValues(array);

        let result = '';
        for (let i = 0; i < length; i++) {
            result += CHARS[array[i] % CHARS.length];
        }
        return result;
    }

    /**
     * Generate base random password (simpler random)
     * @param {number} length - Desired password length (min 12, max 1000)
     * @returns {Promise<string>} Generated random password
     */
    async function generateBasePassword(length) {
        return await generateStrongPassword(length);
    }

    /**
     * Generate authentication code (shorter, for 2FA)
     * @param {number} length - Desired code length (min 4, max 20)
     * @returns {Promise<string>} Generated code
     */
    async function generateCode(length) {
        if (length < 4) {
            throw new Error(`Code length must be at least 4 characters. Current: ${length}`);
        }
        if (length > 20) {
            throw new Error(`Code length cannot exceed 20 characters. Current: ${length}`);
        }

        const array = new Uint8Array(length);
        crypto.getRandomValues(array);

        let result = '';
        for (let i = 0; i < length; i++) {
            result += CHARS[array[i] % CHARS.length];
        }
        return result;
    }

    // Public API
    return {
        VERSION: VERSION,
        CHARS: CHARS,
        PRIVATE_ITERATIONS: PRIVATE_ITERATIONS,
        PUBLIC_ITERATIONS: PUBLIC_ITERATIONS,
        generateKey: generateKey,
        generatePrivateKey: generatePrivateKey,
        generatePublicKey: generatePublicKey,
        verifySecret: verifySecret,
        generatePasswordFromPrivateKey: generatePasswordFromPrivateKey,
        generateSmartPassword: generateSmartPassword,
        generateStrongPassword: generateStrongPassword,
        generateBasePassword: generateBasePassword,
        generateCode: generateCode
    };
})();

// Export for different environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SmartPassLib;
}
if (typeof window !== 'undefined') {
    window.SmartPassLib = SmartPassLib;
}