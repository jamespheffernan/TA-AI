"use client";
import { useState, useRef } from 'react';
import axios from 'axios';
import ChatMessage from '@/components/ChatMessage';

export default function ChatPage() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string; citations?: number[] }>>([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user' as const, content: input };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    const question = input;
    setInput('');
    try {
      const response = await axios.post('/api/query', { course_id: 1, question });
      const { answer, citations } = response.data;
      const assistantMsg = { role: 'assistant' as const, content: answer, citations };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (e: any) {
      const errorMsg = { role: 'assistant' as const, content: 'Error: ' + e.message };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
      setTimeout(() => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-grow p-4 overflow-auto">
        {messages.map((msg, idx) => (
          <ChatMessage key={idx} {...msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 border-t border-gray-200">
        <div className="flex">
          <input
            className="flex-grow p-2 border border-gray-300 rounded-l-md"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question..."
            disabled={loading}
          />
          <button
            className="px-4 bg-primary-600 text-white rounded-r-md"
            onClick={sendMessage}
            disabled={loading}
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
