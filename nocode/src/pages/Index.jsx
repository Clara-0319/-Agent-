import React, { useState } from 'react';
import { Heart, Sparkles } from 'lucide-react';
import InputTabs from '../components/InputTabs.jsx';
import TextInput from '../components/TextInput.jsx';
import ImageUpload from '../components/ImageUpload.jsx';
import TableUpload from '../components/TableUpload.jsx';
import MatchResult from '../components/MatchResult.jsx';
import useMatchAnalysis from '../hooks/useMatchAnalysis.js';

const Index = () => {
  const [activeTab, setActiveTab] = useState('text');
  const { isLoading, result, analyzeMatch, resetResult } = useMatchAnalysis();

  const handleInputSubmit = (inputData) => {
    analyzeMatch(inputData);
  };

  const renderInputComponent = () => {
    switch (activeTab) {
      case 'text':
        return <TextInput onSubmit={handleInputSubmit} isLoading={isLoading} />;
      case 'image':
        return <ImageUpload onSubmit={handleInputSubmit} isLoading={isLoading} />;
      case 'table':
        return <TableUpload onSubmit={handleInputSubmit} isLoading={isLoading} />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* 头部标题 */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Heart className="w-8 h-8 text-pink-500 mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">
              智能婚恋匹配评价系统
            </h1>
            <Sparkles className="w-8 h-8 text-blue-500 ml-3" />
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            基于大模型Agent与婚恋数据结论，为您提供专业的匹配度分析和个性化建议
          </p>
        </div>

        <div className="max-w-6xl mx-auto">
          {!result ? (
            /* 输入区域 */
            <div className="bg-white rounded-xl shadow-lg p-8">
              <InputTabs activeTab={activeTab} setActiveTab={setActiveTab} />
              {renderInputComponent()}
            </div>
          ) : (
            /* 结果展示区域 */
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-bold text-gray-900">匹配分析结果</h2>
                  <button
                    onClick={resetResult}
                    className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                  >
                    重新分析
                  </button>
                </div>
                <MatchResult result={result} />
              </div>
            </div>
          )}
        </div>

        {/* 底部说明 */}
        <div className="mt-12 text-center">
          <div className="bg-white rounded-lg shadow p-6 max-w-4xl mx-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">系统特色</h3>
            <div className="grid md:grid-cols-3 gap-6 text-sm text-gray-600">
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-3">
                  <Sparkles className="w-6 h-6 text-blue-600" />
                </div>
                <h4 className="font-medium text-gray-900 mb-2">多模态输入</h4>
                <p>支持文字、图片、表格三种输入方式，满足不同场景需求</p>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3">
                  <Heart className="w-6 h-6 text-green-600" />
                </div>
                <h4 className="font-medium text-gray-900 mb-2">可解释性评价</h4>
                <p>基于真实婚恋数据，提供有依据的匹配分析和建议</p>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-3">
                  <div className="w-6 h-6 bg-purple-600 rounded-full"></div>
                </div>
                <h4 className="font-medium text-gray-900 mb-2">数据驱动</h4>
                <p>依托大数据分析，确保匹配结果的准确性和专业性</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
