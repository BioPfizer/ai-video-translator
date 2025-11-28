'use client'

import { useState } from 'react'
import { FileUpload } from '@/components/ui/file-upload'

export default function TestUpload() {
  const [file, setFile] = useState<File | null>(null)

  return (
    <div className="min-h-screen bg-slate-900 p-8">
      <h1 className="text-white text-2xl mb-4">Test File Upload</h1>
      
      <div className="max-w-2xl mx-auto">
        <FileUpload 
          onChange={(selectedFile) => {
            console.log('File selected:', selectedFile)
            setFile(selectedFile)
          }} 
        />
        
        {file && (
          <div className="mt-8 p-6 bg-white rounded-lg">
            <h2 className="text-xl font-bold mb-2">File Details:</h2>
            <p className="text-black">Name: {file.name}</p>
            <p className="text-black">Size: {(file.size / 1024 / 1024).toFixed(2)} MB</p>
            <p className="text-black">Type: {file.type}</p>
          </div>
        )}
        
        <button 
          onClick={() => console.log('Current file state:', file)}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Log File State
        </button>
      </div>
    </div>
  )
}
