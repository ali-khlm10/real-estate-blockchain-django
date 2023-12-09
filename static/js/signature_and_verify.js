document.getElementById("signButton").addEventListener("click", async () => {
  const privateKeyPEM =
    "-----BEGIN PRIVATE KEY-----\nMIHuAgEAMBAGByqGSM49AgEGBSuBBAAjBIHWMIHTAgEBBEIBUYDkFqgWhgz41ksu\n/TC+1vTHWVabQU2stT72tEVohIwxyys+14OGd5Hg0xYPsjGc4hhlKVsKEuGLSMIx\npwAPHWahgYkDgYYABAHCMUyGLW3TNAbIlx2erpVCGI6OBAUWNdrqqM7zAxYHwech\nTqg0EqgEK2ZOCX+Tv/FzKmtsM2/rRJOlkNnTqjWlzAHcj4MexOt4DjI78Jtgimhx\n0+zGRsCR7eFBOuP7yBJb7vzHXOnzOyWRf12ZOLLi97c3Z86vZ7iwM4MfvCGK4hGT\nnw==\n-----END PRIVATE KEY-----\n";

  const publicKeyPEM =
    "-----BEGIN PUBLIC KEY-----\nMIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQBwjFMhi1t0zQGyJcdnq6VQhiOjgQF\nFjXa6qjO8wMWB8HnIU6oNBKoBCtmTgl/k7/xcyprbDNv60STpZDZ06o1pcwB3I+D\nHsTreA4yO/CbYIpocdPsxkbAke3hQTrj+8gSW+78x1zp8zslkX9dmTiy4ve3N2fO\nr2e4sDODH7whiuIRk58=\n-----END PUBLIC KEY-----\n";

  const messageToSign = "Hello, World!";
  try {
    const signature = await signMessage(privateKeyPEM, messageToSign);
    console.log(signature);
    // شما می‌توانید از 'signature' همینجا استفاده کنید، مثل ارسال به سرور...
  } catch (error) {
    console.error("Error signing message:", error);
  }
});

async function signMessage(privateKeyPem, message) {
  const privateKey = await window.crypto.subtle.importKey(
    "pkcs8",
    pemToArrayBuffer(privateKeyPem),
    {
      name: "ECDSA",
      namedCurve: "P-521",
    },
    true,
    ["sign"]
  );

  const signature = await window.crypto.subtle.sign(
    {
      name: "ECDSA",
      hash: { name: "SHA-512" },
    },
    privateKey,
    new TextEncoder().encode(message)
  );

  return arrayBufferToHex(signature);
}

function pemToArrayBuffer(pem) {
  const base64String = window.atob(pem.split("\n").slice(1, -2).join(""));
  const byteArray = new Uint8Array(base64String.length);
  for (let i = 0; i < base64String.length; i++) {
    byteArray[i] = base64String.charCodeAt(i);
  }
  return byteArray.buffer;
}

function arrayBufferToHex(buffer) {
  return Array.from(new Uint8Array(buffer))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}
