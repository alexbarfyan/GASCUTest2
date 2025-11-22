const chatLog = document.getElementById("chat-log");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  const span = document.createElement("span");
  span.textContent = text;
  div.appendChild(span);
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  input.focus();

  try {
    const res = await fetch("https://YOUR-BACKEND-URL/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    const data = await res.json();
    if (data.reply) {
      addMessage(data.reply, "bot");
    } else {
      addMessage("Sorry, something went wrong.", "bot");
    }
  } catch (err) {
    console.error(err);
    addMessage("Error contacting server.", "bot");
  }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});
