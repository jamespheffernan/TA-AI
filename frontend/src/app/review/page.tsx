"use client";
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import QAReviewTable from '@/components/QAReviewTable';

interface QAReviewItem {
  id: number;
  question: string;
  answer: string;
  timestamp: string;
  flagged: boolean;
  feedback?: string;
}

export default function ReviewPage() {
  const [filterText, setFilterText] = useState('');
  const [showFlaggedOnly, setShowFlaggedOnly] = useState(false);
  const [items, setItems] = useState<QAReviewItem[]>([]);

  useEffect(() => {
    axios.get('/api/review')
      .then((res) => setItems(res.data))
      .catch((err) => console.error('Error fetching review logs:', err));
  }, []);

  const filteredItems = items.filter((item) =>
    (item.question.toLowerCase().includes(filterText.toLowerCase()) ||
      item.answer.toLowerCase().includes(filterText.toLowerCase())) &&
    (!showFlaggedOnly || item.flagged)
  );

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Review Q&A Log</h1>
      <div className="mb-4 flex space-x-4">
        <input
          type="text"
          placeholder="Search..."
          value={filterText}
          onChange={(e) => setFilterText(e.target.value)}
          className="border p-2 rounded-md flex-grow"
        />
        <label className="flex items-center space-x-1">
          <input
            type="checkbox"
            checked={showFlaggedOnly}
            onChange={(e) => setShowFlaggedOnly(e.target.checked)}
            className="form-checkbox"
          />
          <span>Flagged only</span>
        </label>
      </div>
      <QAReviewTable items={filteredItems} />
    </div>
  );
}