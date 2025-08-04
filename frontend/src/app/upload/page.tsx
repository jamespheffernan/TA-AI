"use client";
import React, { useState } from 'react';
import axios from 'axios';
import DragAndDropUploader from '@/components/DragAndDropUploader';

export default function UploadPage() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);

  const handleFilesSelected = (files: File[]) => {
    setSelectedFiles(files);
    console.log('Files selected for upload:', files);
  };

  const uploadFiles = async () => {
    if (selectedFiles.length === 0) return;
    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append('file', file));
    setUploading(true);
    setUploadMessage(null);
    try {
      const response = await axios.post('/api/ingest', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setUploadMessage('Upload successful');
      console.log('Ingestion response:', response.data);
    } catch (err: any) {
      setUploadMessage('Upload failed: ' + err.message);
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Upload Course Materials</h1>
      <DragAndDropUploader onFilesSelected={handleFilesSelected} />
      {selectedFiles.length > 0 && (
        <div className="mt-4">
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            onClick={uploadFiles}
            disabled={uploading}
          >
            {uploading ? 'Uploading...' : 'Start Upload'}
          </button>
        </div>
      )}
      {uploadMessage && <p className="mt-2 text-sm text-gray-700">{uploadMessage}</p>}
    </div>
  );
}