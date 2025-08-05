import React, { useCallback, useState } from 'react';

interface DragAndDropUploaderProps {
  onFilesSelected: (files: File[]) => void;
}

export default function DragAndDropUploader({ onFilesSelected }: DragAndDropUploaderProps) {
  const [dragOver, setDragOver] = useState(false);
  const [files, setFiles] = useState<File[]>([]);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles(droppedFiles);
    onFilesSelected(droppedFiles);
  }, [onFilesSelected]);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
  };

  return (
    <div
      className={`p-8 border-2 border-dashed rounded-md text-center ${dragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
    >
      {files.length > 0 ? (
        <div>
          <p className="mb-2 font-medium">{files.length} file{files.length > 1 ? 's' : ''} selected</p>
          <ul className="text-sm list-disc list-inside">
            {files.map((file, idx) => (
              <li key={idx}>{file.name}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p className="text-gray-500">Drag & drop files here, or click to select</p>
      )}
    </div>
  );
}