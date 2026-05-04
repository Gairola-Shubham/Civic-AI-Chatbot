import { useState, useEffect } from "react";
import Chatbot from "./components/Chatbot";
import Sidebar from "./components/Sidebar";
import Login from "./components/Login";
import Profile from "./components/Profile";
import "./App.css";

function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState("chat");
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);

  useEffect(() => {
    if (user) {
      const saved = JSON.parse(localStorage.getItem(user + "_chats")) || [];
      setChats(saved);

      if (saved.length > 0) {
        setActiveChat(saved[0].id);
      }
    }
  }, [user]);

  useEffect(() => {
    if (user) {
      localStorage.setItem(user + "_chats", JSON.stringify(chats));
    }
  }, [chats, user]);

  function handleLogout() {
    setUser(null);
    setView("chat");
  }

  function handleGuest() {
    setUser("Guest");
    setView("chat");
  }

  function handleLogin(username) {
    setUser(username);
    setView("chat");
  }
  function handleNameChange(newName) {
    localStorage.setItem(user + "_displayName", newName);
  }
  function handleNewChat() {

    const newChat = {
      id: Date.now(),
      messages: []
    };

    setChats(prev => [newChat, ...prev]);
    setActiveChat(newChat.id);
  }
  function updateMessages(newMessages) {

    setChats(prev =>
      prev.map(chat =>
        chat.id === activeChat
          ? { ...chat, messages: newMessages }
          : chat
      )
    );
  }
  const currentChat = chats.find(c => c.id === activeChat);

  return (
    <div>
      {user ? (
        <div className="app-container">

          <div className="hover-zone"></div>

          <Sidebar
            user={user}
            chats={chats}
            activeChat={activeChat}
            setActiveChat={setActiveChat}
            onLogout={handleLogout}
            onGuest={handleGuest}
            onSwitchUser={handleLogin}
            onProfile={() => setView("profile")}
            onNewChat={handleNewChat}
          />

          <div className="chat-section">

            {view === "chat" ? (
              <Chatbot
                messages={currentChat?.messages || []}
                setMessages={updateMessages}
                user={user}
              />
            ) : (
              <Profile
                user={user}
                goBack={() => setView("chat")}
                onNameChange={handleNameChange}
                onLogout={handleLogout}
              />
            )}

          </div>

        </div>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;