/********************************************
 *  👇 PUT YOUR BACKEND URL HERE (ONLY HERE)
 *
 *  Example after deploying backend:
 *  const API_URL = "https://eric-backend.onrender.com/chat";
 *
 ********************************************/
const API_URL = "YOUR_BACKEND_URL_HERE";  // <-- CHANGE THIS ONLY



/*************** Chat UI logic below ***************/

const chatLog = document.getElementById("chat-log");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Adds messages to the chat window
function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;

  const span = document.createElement("span");
  const label = sender === "user" ? "You: " : "Eric: ";
  span.textContent = label + text;

  div.appendChild(span);
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
}

// Sends a message to the backend
async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  input.focus();

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    const data = await res.json();

    if (data.reply) {
      addMessage(data.reply, "bot");
    } else {
      addMessage("Sorry, something went wrong on the server.", "bot");
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
