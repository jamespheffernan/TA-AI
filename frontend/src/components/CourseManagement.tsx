import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Course {
  id: number;
  name: string;
}

export default function CourseManagement() {
  const [courses, setCourses] = useState<Course[]>([]);
  const fetchCourses = () => {
    axios.get('/api/admin/courses')
      .then((res) => setCourses(res.data))
      .catch((err) => console.error('Error fetching courses:', err));
  };

  useEffect(() => {
    fetchCourses();
  }, []);
  const handleAdd = async () => {
    const name = prompt('Enter course name');
    if (!name) return;
    await axios.post('/api/admin/courses', { name });
    fetchCourses();
  };
  const handleEdit = async (id: number) => {
    const course = courses.find((c) => c.id === id);
    const newName = prompt('Enter new course name', course?.name);
    if (!newName) return;
    await axios.put('/api/admin/courses', { id, name: newName });
    fetchCourses();
  };
  const handleDelete = async (id: number) => {
    if (!confirm('Delete this course?')) return;
    await axios.delete(`/api/admin/courses?id=${id}`);
    fetchCourses();
  };

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
                <button onClick={() => handleEdit(course.id)} className="text-blue-600 hover:underline mr-2">Edit</button>
                <button onClick={() => handleDelete(course.id)} className="text-red-600 hover:underline">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleAdd} className="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
        Add Course
      </button>
    </div>
  );
}