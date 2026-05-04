import { useState } from "react";
import Message from "./Message";

function Chatbot({ messages, setMessages }) {

  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const hasStarted = messages.length > 0;

  async function sendMessage() {

    if (input.trim() === "" || isTyping) return;

    const userText = input;
    const userMessage = { sender: "user", text: userText };

    setInput("");
    setIsTyping(true);

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);

    try {

      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: userText })
      });

      if (!res.ok) throw new Error("Server error");

      const data = await res.json();

      let botText = data.answer || "No answer found.";

      if (data.sources && data.sources.length > 0) {
        const sourceText = data.sources
          .slice(0, 3)
          .map(s => `• ${s.state} (${s.domain}) - Page ${s.page}`)
          .join("\n");

        botText += `\n\n📌 Sources:\n${sourceText}`;
      }

      const botReply = { sender: "bot", text: botText };

      setMessages([...newMessages, botReply]);

    } catch (error) {

      setMessages([
        ...newMessages,
        { sender: "bot", text: "⚠️ Error connecting to server." }
      ]);

    } finally {
      setIsTyping(false);
    }
  }

  return (

    <div className="chatbot-shell">

      {/* TITLE */}
      <div className={hasStarted ? "chat-title active" : "chat-title idle"}>
        Civic AI Assistant
      </div>

      {/* INTRO TEXT */}
      {!hasStarted && (
        <div className="intro-text">
          Hello, I am Civic AI. How can I help you?
        </div>
      )}

      {/* MESSAGES */}
      <div className="chat-messages">

        {messages.map((msg, index) => (
          <Message key={index} sender={msg.sender} text={msg.text} />
        ))}

        {isTyping && (
          <div className="bot-msg typing">...</div>
        )}

      </div>

      {/* INPUT */}
      <div className="chat-input-bar">

        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Civic AI..."
          disabled={isTyping}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button onClick={sendMessage} disabled={isTyping}>
          ➤
        </button>

      </div>

    </div>
  );
}

export default Chatbot;