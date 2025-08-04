import React, { useState } from 'react';
import axios from 'axios';

interface QAReviewItem {
  id: number;
  question: string;
  answer: string;
  timestamp: string;
  flagged: boolean;
  feedback?: string;
}

interface QAReviewTableProps {
  items: QAReviewItem[];
}

export default function QAReviewTable({ items }: QAReviewTableProps) {
  const [data, setData] = useState<QAReviewItem[]>(items);

  const toggleFlag = async (id: number) => {
    const item = data.find((i) => i.id === id);
    if (!item) return;
    const newFlagged = !item.flagged;
    try {
      await axios.post('/api/review', { id, flagged: newFlagged, feedback: item.feedback });
      setData((prev) =>
        prev.map((i) => (i.id === id ? { ...i, flagged: newFlagged } : i))
      );
    } catch (err) {
      console.error('Error updating flag:', err);
    }
  };

  const submitFeedback = async (id: number, feedback: string) => {
    try {
      await axios.post('/api/review', { id, flagged: data.find((i) => i.id === id)?.flagged, feedback });
      setData((prev) =>
        prev.map((item) => (item.id === id ? { ...item, feedback } : item))
      );
    } catch (err) {
      console.error('Error submitting feedback:', err);
    }
  };

  return (
    <table className="min-w-full bg-white">
      <thead>
        <tr>
          <th className="p-2 text-left">Time</th>
          <th className="p-2 text-left">Question</th>
          <th className="p-2 text-left">Answer</th>
          <th className="p-2 text-left">Flagged</th>
          <th className="p-2 text-left">Feedback</th>
          <th className="p-2 text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id} className="border-b">
            <td className="p-2 text-sm">{new Date(item.timestamp).toLocaleString()}</td>
            <td className="p-2 text-sm">{item.question}</td>
            <td className="p-2 text-sm">{item.answer}</td>
            <td className="p-2 text-sm">{item.flagged ? '🚩' : ''}</td>
            <td className="p-2 text-sm">
              <input
                type="text"
                defaultValue={item.feedback || ''}
                className="border px-1 py-0.5 rounded w-full"
                onBlur={(e) => submitFeedback(item.id, e.target.value)}
              />
            </td>
            <td className="p-2 text-sm">
              <button
                onClick={() => toggleFlag(item.id)}
                className="text-blue-600 hover:underline"
              >
                {item.flagged ? 'Unflag' : 'Flag'}
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}