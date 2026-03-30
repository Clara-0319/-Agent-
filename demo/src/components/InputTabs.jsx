import React from 'react';
import { FileText, Image, Table } from 'lucide-react';

const InputTabs = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'text', label: '文字描述', icon: FileText },
    { id: 'image', label: '图片上传', icon: Image },
    { id: 'table', label: '表格上传', icon: Table }
  ];

  return (
    <div className="flex border-b border-gray-200 mb-6">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        return (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center px-6 py-3 font-medium text-sm border-b-2 transition-colors ${
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600 bg-blue-50'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Icon className="w-4 h-4 mr-2" />
            {tab.label}
          </button>
        );
      })}
    </div>
  );
};

export default InputTabs;
