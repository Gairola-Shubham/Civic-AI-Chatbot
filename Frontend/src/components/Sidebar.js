import { useState } from "react";

function Sidebar({ 
  user, 
  chats,
  activeChat,
  setActiveChat,
  onLogout, 
  onGuest, 
  onSwitchUser, 
  onProfile,
  onNewChat
}) {

  const [showMenu, setShowMenu] = useState(false);
  const [showAccounts, setShowAccounts] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [password, setPassword] = useState("");

  const users = JSON.parse(localStorage.getItem("users")) || [];
  const isGuest = user === "Guest";

  const displayName = localStorage.getItem(user + "_displayName") || user;
  const avatar = localStorage.getItem(user + "_avatar");

  function handleAccountLogin(){
    const storedPassword = localStorage.getItem(selectedUser);

    if(storedPassword === password){
      onSwitchUser(selectedUser);
      setShowAccounts(false);
      setPassword("");
    } else {
      alert("Wrong password");
    }
  }

return (

  <div className="sidebar">

    {/* TOP */}
    <div className="sidebar-top">

      <h2 className="logo">CIVIC A.I+</h2>

      <button className="new-chat" onClick={onNewChat}>
        + New Chat
      </button>

      <div className="conversations">

        <p className="conv-title">Your Conversations</p>

        {isGuest && (
          <p className="guest-text">Logged in As A Guest</p>
        )}

        <ul>
          {chats.length === 0 && (
            <li style={{opacity:0.6}}>No chats yet</li>
          )}

          {chats.map(chat => {

            const title = chat.messages[0]?.text?.slice(0, 25) || "New Chat";

            return (
              <li
                key={chat.id}
                className={chat.id === activeChat ? "active-chat" : ""}
                onClick={() => setActiveChat(chat.id)}
              >
                {title}
              </li>
            );
          })}
        </ul>

      </div>

    </div>


    {/* BOTTOM */}
    <div className="sidebar-bottom">

      <div className="user-profile">

        {avatar ? (
          <img src={avatar} alt="avatar" className="user-avatar" />
        ) : (
          <div className="avatar-placeholder">
            {displayName.charAt(0).toUpperCase()}
          </div>
        )}

        <span className="user-name">{displayName}</span>

        <button 
          className="menu-btn"
          onClick={()=>setShowMenu(!showMenu)}
        >
          ...
        </button>

        {showMenu && (
          <div className="dropdown">

            <p onClick={()=>{ onProfile(); setShowMenu(false); }}>
              Profile
            </p>

            <p onClick={()=>{ onLogout(); setShowMenu(false); }}>
              Logout
            </p>

            <p onClick={()=>{ onGuest(); setShowMenu(false); }}>
              Continue as Guest
            </p>

            <p onClick={()=>{ setShowAccounts(true); setShowMenu(false); }}>
              Change Account
            </p>

          </div>
        )}

      </div>

    </div>


    {/* MODAL */}
    {showAccounts && (
      <div className="modal">

        <h3>Select Account</h3>

        {users.length === 0 && <p>No accounts found</p>}

        {users.map((u,i)=>(
          <p 
            key={i} 
            onClick={()=>setSelectedUser(u)}
            style={{cursor:"pointer"}}
          >
            {u}
          </p>
        ))}

        {selectedUser && (
          <>
            <input
              type="password"
              placeholder={`Enter password for ${selectedUser}`}
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
            />

            <button onClick={handleAccountLogin}>
              Login
            </button>
          </>
        )}

        <button onClick={()=>setShowAccounts(false)}>
          Close
        </button>

      </div>
    )}

  </div>
);
}

export default Sidebar;