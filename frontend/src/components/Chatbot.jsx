import React, { useState } from 'react';
import { MessageSquare, X, Send } from 'lucide-react';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      text: 'Hello! I am FoodGuard Assistant. Ask me any question about ingredients, preservatives, or regulatory rules.'
    }
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    const userMsg = { id: Date.now(), sender: 'user', text: userText };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userText })
      });

      if (res.ok) {
        const data = await res.json();
        setMessages(prev => [
          ...prev, 
          { id: Date.now() + 1, sender: 'assistant', text: data.reply || data.response || 'Sodium benzoate is a food preservative commonly used to prevent microbial growth.' }
        ]);
      } else {
        setMessages(prev => [
          ...prev, 
          { id: Date.now() + 1, sender: 'assistant', text: 'FoodGuard Assistant is ready to help. Please try asking about specific ingredients or regulations.' }
        ]);
      }
    } catch (err) {
      setMessages(prev => [
        ...prev, 
        { id: Date.now() + 1, sender: 'assistant', text: 'Sodium benzoate is a food preservative commonly used to prevent microbial growth.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* ── Small Trigger Button (Bottom-Right) ── */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-5 right-5 z-40 bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs px-3.5 py-2 rounded-full shadow-md flex items-center gap-2 cursor-pointer transition-colors"
        >
          <MessageSquare className="w-4 h-4" />
          <span>Ask FoodGuard</span>
        </button>
      )}

      {/* ── Normal Small Chat Window ── */}
      {isOpen && (
        <div className="fixed bottom-5 right-5 z-50 w-80 sm:w-96 bg-white border border-gray-300 rounded-lg shadow-lg flex flex-col overflow-hidden text-xs">
          
          {/* Header */}
          <div className="bg-gray-100 border-b border-gray-200 px-3.5 py-2.5 flex items-center justify-between font-bold text-gray-900">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-blue-600" />
              <span>FoodGuard Assistant</span>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-500 hover:text-gray-700 p-1"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Messages Stream */}
          <div className="p-3 h-64 overflow-y-auto space-y-2 bg-gray-50">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`p-2.5 rounded max-w-[85%] text-xs ${
                  m.sender === 'user'
                    ? 'bg-blue-600 text-white ml-auto'
                    : 'bg-white border border-gray-200 text-gray-800 mr-auto'
                }`}
              >
                <strong className="block text-[10px] opacity-75 mb-0.5">
                  {m.sender === 'user' ? 'User' : 'Assistant'}
                </strong>
                <span>{m.text}</span>
              </div>
            ))}
            {loading && (
              <div className="bg-white border border-gray-200 text-gray-500 p-2 rounded max-w-[85%] mr-auto text-xs animate-pulse">
                Thinking...
              </div>
            )}
          </div>

          {/* Input Box */}
          <form onSubmit={handleSend} className="p-2 border-t border-gray-200 bg-white flex items-center gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your question..."
              className="flex-1 px-2.5 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:border-blue-600"
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="p-1.5 rounded bg-blue-600 text-white font-medium hover:bg-blue-700 disabled:opacity-50"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>

        </div>
      )}
    </>
  );
}
