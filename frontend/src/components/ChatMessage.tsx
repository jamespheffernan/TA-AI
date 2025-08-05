import React from 'react';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  citations?: number[];
}

export default function ChatMessage({ role, content, citations }: ChatMessageProps) {
  return (
    <div className={`flex ${role === 'assistant' ? 'justify-start' : 'justify-end'} mb-4`}>  
      <div className={`max-w-md p-4 rounded-lg shadow ${role === 'assistant' ? 'bg-white' : 'bg-primary-600 text-white'}`}>
        <ReactMarkdown>{content}</ReactMarkdown>
        {citations && citations.length > 0 && (
          <div className="text-sm text-gray-500 mt-2">
            Citations: {citations.map((id) => <span key={id} className="mr-2">[{id}]</span>)}
          </div>
        )}
      </div>
    </div>
  );
}