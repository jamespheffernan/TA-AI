"use client";
import { useState, useEffect } from 'react';
import CourseSelector from '@/components/CourseSelector';
import QuestionHistory from '@/components/QuestionHistory';

interface Course {
  id: number;
  name: string;
}
interface QAItem {
  id: number;
  question: string;
  answer: string;
  timestamp: string;
  citations?: number[];
}

export default function StudentPortalPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<number | null>(null);
  const [history, setHistory] = useState<QAItem[]>([]);

  useEffect(() => {
    // Placeholder courses
    setCourses([
      { id: 1, name: 'Intro to Algorithms' },
      { id: 2, name: 'Data Structures' },
    ]);
  }, []);

  useEffect(() => {
    if (selectedCourse != null) {
      // Placeholder history data
      setHistory([
        { id: 101, question: 'What is a binary tree?', answer: 'A tree data structure...', timestamp: new Date().toISOString(), citations: [1,2] },
        { id: 102, question: 'Explain quicksort.', answer: 'An efficient sorting algorithm...', timestamp: new Date().toISOString(), citations: [3] },
      ]);
    }
  }, [selectedCourse]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Student Portal</h1>
      <CourseSelector courses={courses} selectedCourseId={selectedCourse} onSelect={setSelectedCourse} />
      {selectedCourse ? (
        <QuestionHistory history={history} />
      ) : (
        <p className="text-gray-500">Please select a course to view history.</p>
      )}
    </div>
  );
}