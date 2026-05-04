import { useState, useEffect } from "react";

function Profile({ user, goBack, onNameChange, onLogout }) {

  const [name, setName] = useState(user);
  const [avatar, setAvatar] = useState("");
  const [dragging, setDragging] = useState(false);

  useEffect(() => {
    const savedName = localStorage.getItem(user + "_displayName");
    const savedAvatar = localStorage.getItem(user + "_avatar");

    if (savedName) setName(savedName);
    if (savedAvatar) setAvatar(savedAvatar);

  }, [user]);

  function handleSave() {
    localStorage.setItem(user + "_displayName", name);
    localStorage.setItem(user + "_avatar", avatar);

    onNameChange(name);
    alert("Profile updated!");
  }

  function deleteHistory() {
    localStorage.removeItem(user + "_chats");
    alert("Chat history deleted!");
  }

  function deleteAccount() {

    const confirmDelete = window.prompt(
      "Type DELETE to permanently delete your account"
    );

    if (confirmDelete !== "DELETE") return;

    // remove user list entry
    const users = JSON.parse(localStorage.getItem("users")) || [];
    const updatedUsers = users.filter(u => u !== user);
    localStorage.setItem("users", JSON.stringify(updatedUsers));

    // remove all user data
    localStorage.removeItem(user); // password
    localStorage.removeItem(user + "_displayName");
    localStorage.removeItem(user + "_avatar");
    localStorage.removeItem(user + "_chats");

    alert("Account deleted");
    onLogout();
  }

  function handleFile(file) {
    if (!file) return;

    const reader = new FileReader();

    reader.onloadend = () => {
      setAvatar(reader.result);
    };

    reader.readAsDataURL(file);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragging(false);

    const file = e.dataTransfer.files[0];
    handleFile(file);
  }

  function handleDragOver(e) {
    e.preventDefault();
  }

  function handleDragEnter() {
    setDragging(true);
  }

  function handleDragLeave() {
    setDragging(false);
  }

  return (

    <div className="profile-wrapper">

      <div className="profile-container">

        <h2>Profile Settings</h2>

        {/* NAME */}
        <div className="profile-group">
          <label>Name</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        {/* IMAGE UPLOAD */}
        <div className="profile-group">
          <label>Profile Picture</label>

          <div 
            className={`upload-box ${dragging ? "dragging" : ""}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
          >

            {avatar ? (
              <img src={avatar} alt="preview" className="avatar-preview" />
            ) : (
              <p>Drag & Drop Image Here or Click</p>
            )}

            <input
              type="file"
              accept="image/*"
              onChange={(e)=>handleFile(e.target.files[0])}
            />

          </div>
        </div>

        {/* ACTION BUTTONS */}
        <div className="profile-actions">

          <button className="save-btn" onClick={handleSave}>
            Save Changes
          </button>

          <button className="delete-btn" onClick={deleteHistory}>
            Delete Chat History
          </button>

          {/* 🔥 NEW BUTTON */}
          <button className="danger-btn" onClick={deleteAccount}>
            Delete Account
          </button>

          <button className="back-btn" onClick={goBack}>
            Back
          </button>

        </div>

      </div>

    </div>
  );
}

export default Profile;