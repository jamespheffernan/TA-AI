import React from 'react';

interface QAItem {
  id: number;
  question: string;
  answer: string;
  timestamp: string;
  citations?: number[];
}

interface QuestionHistoryProps {
  history: QAItem[];
}

export default function QuestionHistory({ history }: QuestionHistoryProps) {
  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">Question History</h2>
      <div className="space-y-4">
        {history.map((item) => (
          <div key={item.id} className="border p-4 rounded-md bg-white">
            <div className="text-sm text-gray-500 mb-1">{new Date(item.timestamp).toLocaleString()}</div>
            <div className="mb-2"><strong>Q:</strong> {item.question}</div>
            <div className="mb-2"><strong>A:</strong> {item.answer}</div>
            {item.citations && (
              <div className="text-sm text-gray-500">
                Citations: {item.citations.map((c) => `[${c}] `)}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}