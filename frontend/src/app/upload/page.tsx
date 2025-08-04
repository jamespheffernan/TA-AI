"use client";
import React, { useState } from 'react';
import DragAndDropUploader from '@/components/DragAndDropUploader';

export default function UploadPage() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleFilesSelected = (files: File[]) => {
    setSelectedFiles(files);
    console.log('Files selected for upload:', files);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Upload Course Materials</h1>
      <DragAndDropUploader onFilesSelected={handleFilesSelected} />
      {selectedFiles.length > 0 && (
        <div className="mt-4">
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            onClick={() => alert('Upload started (placeholder)')}
          >
            Start Upload
          </button>
        </div>
      )}
    </div>
  );
}