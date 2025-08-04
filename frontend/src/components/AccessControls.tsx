import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface User {
  id: number;
  external_id: string;
  role: string;
}

export default function AccessControls() {
  const [users, setUsers] = useState<User[]>([]);
  const roles = ['student', 'professor', 'admin'];

  const fetchUsers = () => {
    axios.get('/api/admin/users')
      .then(res => setUsers(res.data))
      .catch(err => console.error('Error fetching users:', err));
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleRoleChange = async (id: number, newRole: string) => {
    await axios.put('/api/admin/users', { id, role: newRole });
    fetchUsers();
  };

  return (
    <div>
      <h2 className="text-lg font-semibold mb-4">User Access Controls</h2>
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="p-2 text-left">ID</th>
            <th className="p-2 text-left">External ID</th>
            <th className="p-2 text-left">Role</th>
            <th className="p-2 text-left">Change Role</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id} className="border-b">
              <td className="p-2 text-sm">{user.id}</td>
              <td className="p-2 text-sm">{user.external_id}</td>
              <td className="p-2 text-sm">{user.role}</td>
              <td className="p-2 text-sm">
                <select
                  value={user.role}
                  onChange={e => handleRoleChange(user.id, e.target.value)}
                  className="border p-1 rounded"
                >
                  {roles.map(r => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}