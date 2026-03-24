import React, { useState } from 'react';
import { Send } from 'lucide-react';

const TextInput = ({ onSubmit, isLoading }) => {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    if (text.trim()) {
      onSubmit({ type: 'text', content: text });
    }
  };

  const exampleText = "男方28岁，本科，身高175cm，北京人，家境中等，性格稳重；女方26岁，硕士，身高163cm，上海人，性格温柔，重视沟通";

  return (
    <div className="space-y-4">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800 mb-2">
          <strong>输入提示：</strong>粘贴或输入男女双方的个人条件，无需固定格式
        </p>
        <p className="text-xs text-blue-600">
          示例：{exampleText}
        </p>
      </div>
      
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="请输入男女双方的个人条件..."
        className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        disabled={isLoading}
      />
      
      <button
        onClick={handleSubmit}
        disabled={!text.trim() || isLoading}
        className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center font-medium"
      >
        {isLoading ? (
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
        ) : (
          <Send className="w-5 h-5 mr-2" />
        )}
        开始智能匹配评价
      </button>
    </div>
  );
};

export default TextInput;
