"use client";
import React from 'react';
import CourseManagement from '@/components/CourseManagement';
import AccessControls from '@/components/AccessControls';
import HealthDashboard from '@/components/HealthDashboard';

export default function AdminPage() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Admin Controls</h1>
      <CourseManagement />
      <div className="mt-8">
        <AccessControls />
      </div>
      <div className="mt-8">
        <HealthDashboard />
      </div>
    </div>
  );
}