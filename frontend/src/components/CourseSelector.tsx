import React from 'react';

interface Course {
  id: number;
  name: string;
}

interface CourseSelectorProps {
  courses: Course[];
  selectedCourseId: number | null;
  onSelect: (id: number) => void;
}

export default function CourseSelector({ courses, selectedCourseId, onSelect }: CourseSelectorProps) {
  return (
    <div className="mb-4">
      <label htmlFor="course" className="block text-sm font-medium text-gray-700 mb-1">
        Select Course
      </label>
      <select
        id="course"
        className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
        value={selectedCourseId ?? ''}
        onChange={(e) => onSelect(Number(e.target.value))}
      >
        <option value="" disabled>Select a course</option>
        {courses.map((course) => (
          <option key={course.id} value={course.id}>
            {course.name}
          </option>
        ))}
      </select>
    </div>
  );
}