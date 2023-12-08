document.getElementById("signButton").addEventListener("click", async () => {
  // const messageToSign = document.getElementById('messageInput').value;
  messageToSign = "hello";
  // درخواست امضای دیجیتال از کلاینت
  const signature = await signMessage(messageToSign);

//   // ارسال امضا و پیام به سرور (جنگو)
//   const response = await fetch("", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": "{{ csrf_token }}", // اضافه کردن توکن CSRF
//     },
//     body: JSON.stringify({
//       message: messageToSign,
//       signature: signature,
//     }),
//   });

//   const responseData = await response.json();
//   const signatureVerified = responseData.signature_verified;

  // نمایش نتیجه
  console.log("Signature verification result:", signature);
});

async function signMessage(message) {
  // درخواست امضای دیجیتال از کتابخانه SubtleCrypto
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  const key = await window.crypto.subtle.generateKey(
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
      hash: { name: "SHA-256" },
    },
    key.privateKey,
    data
  );

  // تبدیل امضا به رشته hex
  const signatureArray = new Uint8Array(signature);
  const signatureHex = Array.from(signatureArray, (byte) =>
    byte.toString(16).padStart(2, "0")
  ).join("");
  return signatureHex;
}
