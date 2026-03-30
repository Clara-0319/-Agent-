import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, AlertTriangle, CheckCircle, User } from 'lucide-react';

const MatchResult = ({ result }) => {
  if (!result) return null;

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLevel = (score) => {
    if (score >= 80) return '优质匹配';
    if (score >= 60) return '良好匹配';
    if (score >= 40) return '一般匹配';
    return '低匹配';
  };

  const getScoreBgColor = (score) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-blue-100';
    if (score >= 40) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="space-y-6">
      {/* 综合评分 */}
      <div className={`${getScoreBgColor(result.overallScore)} border rounded-lg p-6 text-center`}>
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">综合匹配评分</h3>
          <div className={`text-4xl font-bold ${getScoreColor(result.overallScore)}`}>
            {result.overallScore}
          </div>
          <div className={`text-lg font-medium ${getScoreColor(result.overallScore)}`}>
            {getScoreLevel(result.overallScore)}
          </div>
        </div>
      </div>

      {/* 维度得分 */}
      <div className="bg-white border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">维度得分分析</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={result.dimensionScores}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="score" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 匹配优势 */}
      <div className="bg-white border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
          匹配优势
        </h3>
        <div className="space-y-3">
          {result.advantages.map((advantage, index) => (
            <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-sm text-green-800">
                <strong>{advantage.title}：</strong>{advantage.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* 潜在风险 */}
      <div className="bg-white border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <AlertTriangle className="w-5 h-5 text-red-600 mr-2" />
          潜在风险
        </h3>
        <div className="space-y-3">
          {result.risks.map((risk, index) => (
            <div key={index} className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-800">
                <strong>{risk.title}：</strong>{risk.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* 个性化建议 */}
      <div className="bg-white border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <TrendingUp className="w-5 h-5 text-blue-600 mr-2" />
          个性化建议
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2 flex items-center">
              <User className="w-4 h-4 mr-1" />
              男方建议
            </h4>
            <ul className="text-sm text-blue-800 space-y-1">
              {result.maleAdvice.map((advice, index) => (
                <li key={index}>• {advice}</li>
              ))}
            </ul>
          </div>
          <div className="bg-pink-50 border border-pink-200 rounded-lg p-4">
            <h4 className="font-medium text-pink-900 mb-2 flex items-center">
              <User className="w-4 h-4 mr-1" />
              女方建议
            </h4>
            <ul className="text-sm text-pink-800 space-y-1">
              {result.femaleAdvice.map((advice, index) => (
                <li key={index}>• {advice}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MatchResult;
