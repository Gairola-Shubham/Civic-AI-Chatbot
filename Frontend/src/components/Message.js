function Message({ sender, text, intro = false }) {
  return (
    <div className={`message ${sender === "user" ? "user-msg" : "bot-msg"} ${intro ? "intro-msg" : ""}`}>
      {text}
    </div>
  );
}

export default Message;