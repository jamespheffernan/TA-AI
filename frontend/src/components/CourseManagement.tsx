import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Course {
  id: number;
  name: string;
}

export default function CourseManagement() {
  const [courses, setCourses] = useState<Course[]>([]);

  useEffect(() => {
    axios.get('/api/admin/courses')
      .then((res) => setCourses(res.data))
      .catch((err) => console.error('Error fetching courses:', err));
  }, []);

  return (
    <div>
      <h2 className="text-lg font-semibold mb-4">Course Management</h2>
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="p-2 text-left">ID</th>
            <th className="p-2 text-left">Name</th>
            <th className="p-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {courses.map((course) => (
            <tr key={course.id} className="border-b">
              <td className="p-2 text-sm">{course.id}</td>
              <td className="p-2 text-sm">{course.name}</td>
              <td className="p-2 text-sm">
                <button className="text-blue-600 hover:underline mr-2">Edit</button>
                <button className="text-red-600 hover:underline">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button className="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
        Add Course
      </button>
    </div>
  );
}