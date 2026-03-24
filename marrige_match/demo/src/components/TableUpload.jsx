import React, { useState } from 'react';
import { Upload, FileSpreadsheet, X, Play } from 'lucide-react';

const TableUpload = ({ onSubmit, isLoading }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewData, setPreviewData] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && (file.name.endsWith('.xlsx') || file.name.endsWith('.csv'))) {
      setSelectedFile(file);
      // 模拟表格数据预览
      const mockData = [
        { id: 1, male: '28岁，本科，175cm，北京，家境中等，稳重', female: '26岁，硕士，163cm，上海，性格温柔，重视沟通' },
        { id: 2, male: '30岁，硕士，180cm，深圳，家境良好，外向', female: '27岁，本科，165cm，广州，性格开朗，独立' }
      ];
      setPreviewData(mockData);
    }
  };

  const handleRemove = () => {
    setSelectedFile(null);
    setPreviewData(null);
  };

  const handleSubmit = () => {
    if (selectedFile) {
      onSubmit({ type: 'table', file: selectedFile, data: previewData });
    }
  };

  return (
    <div className="space-y-4">
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
        <p className="text-sm text-purple-800 mb-2">
          <strong>上传提示：</strong>支持Excel/CSV格式，可批量匹配多组数据
        </p>
        <p className="text-xs text-purple-600">
          文件格式：包含男女双方条件的表格文件
        </p>
      </div>

      {!selectedFile ? (
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <FileSpreadsheet className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <div className="space-y-2">
            <p className="text-gray-600">点击上传表格文件</p>
            <input
              type="file"
              accept=".xlsx,.csv"
              onChange={handleFileSelect}
              className="hidden"
              id="table-upload"
              disabled={isLoading}
            />
            <label
              htmlFor="table-upload"
              className="inline-flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 cursor-pointer disabled:bg-gray-400"
            >
              <Upload className="w-4 h-4 mr-2" />
              选择表格
            </label>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
            <div className="flex items-center">
              <FileSpreadsheet className="w-5 h-5 text-purple-600 mr-2" />
              <span className="text-sm font-medium">{selectedFile.name}</span>
            </div>
            <button
              onClick={handleRemove}
              className="text-red-500 hover:text-red-700"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {previewData && (
            <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              <div className="bg-gray-50 px-4 py-2 border-b">
                <h4 className="font-medium text-gray-900">数据预览</h4>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left">序号</th>
                      <th className="px-4 py-2 text-left">男方条件</th>
                      <th className="px-4 py-2 text-left">女方条件</th>
                    </tr>
                  </thead>
                  <tbody>
                    {previewData.map((row) => (
                      <tr key={row.id} className="border-t">
                        <td className="px-4 py-2">{row.id}</td>
                        <td className="px-4 py-2">{row.male}</td>
                        <td className="px-4 py-2">{row.female}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className="w-full bg-purple-600 text-white py-3 px-4 rounded-lg hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center font-medium"
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            ) : (
              <Play className="w-5 h-5 mr-2" />
            )}
            开始批量匹配评价
          </button>
        </div>
      )}
    </div>
  );
};

export default TableUpload;
