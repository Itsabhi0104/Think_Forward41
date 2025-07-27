import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/chat', {
        message,
        session_id: 'default'
      });
      setResponse(res.data.response);
    } catch (err) {
      setResponse('❌ Failed to connect to backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '20px auto' }}>
      <textarea
        rows="4"
        style={{ width: '100%', fontSize: '16px' }}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message here..."
      />
      <button onClick={sendMessage} disabled={loading} style={{ marginTop: '10px' }}>
        {loading ? 'Sending...' : 'Send'}
      </button>
      {response && (
        <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
          <strong>Response:</strong>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default Chat;
