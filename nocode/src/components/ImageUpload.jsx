import React, { useState } from 'react';
import { Upload, Image as ImageIcon, X } from 'lucide-react';

const ImageUpload = ({ onSubmit, isLoading }) => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  };

  const handleRemove = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
  };

  const handleSubmit = () => {
    if (selectedImage) {
      onSubmit({ type: 'image', file: selectedImage });
    }
  };

  return (
    <div className="space-y-4">
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <p className="text-sm text-green-800 mb-2">
          <strong>上传提示：</strong>支持上传相亲表、征婚图等图片，AI将自动抽取信息
        </p>
        <p className="text-xs text-green-600">
          支持格式：JPG、PNG、GIF（最大10MB）
        </p>
      </div>

      {!selectedImage ? (
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <ImageIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <div className="space-y-2">
            <p className="text-gray-600">点击上传或拖拽图片到此处</p>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              className="hidden"
              id="image-upload"
              disabled={isLoading}
            />
            <label
              htmlFor="image-upload"
              className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 cursor-pointer disabled:bg-gray-400"
            >
              <Upload className="w-4 h-4 mr-2" />
              选择图片
            </label>
          </div>
        </div>
      ) : (
        <div className="relative">
          <img
            src={previewUrl}
            alt="预览"
            className="mx-auto object-cover w-full h-64 rounded-lg border border-gray-300"
          />
          <button
            onClick={handleRemove}
            className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {selectedImage && (
        <button
          onClick={handleSubmit}
          disabled={isLoading}
          className="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center font-medium"
        >
          {isLoading ? (
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
          ) : (
            <Upload className="w-5 h-5 mr-2" />
          )}
          开始智能匹配评价
        </button>
      )}
    </div>
  );
};

export default ImageUpload;
