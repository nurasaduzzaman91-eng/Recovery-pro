import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function InjuryDetail({ userId }) {
  const { injuryId } = useParams();
  const [injury, setInjury] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showExerciseForm, setShowExerciseForm] = useState(false);
  const [exerciseLogs, setExerciseLogs] = useState([]);
  const [formData, setFormData] = useState({
    exercise_id: 1,
    pain_level: 5,
    difficulty: 5,
    notes: ''
  });

  useEffect(() => {
    fetchData();
  }, [injuryId]);

  const fetchData = async () => {
    try {
      const injuryRes = await axios.get(`${API_URL}/injuries/detail/${injuryId}`);
      setInjury(injuryRes.data);
      
      const predictionRes = await axios.get(`${API_URL}/analytics/predict/${injuryId}`);
      setPrediction(predictionRes.data);
      
      const analyticsRes = await axios.get(`${API_URL}/analytics/injury-analytics/${injuryId}`);
      setAnalytics(analyticsRes.data);
      
      const logsRes = await axios.get(`${API_URL}/exercises/logs/${injuryId}`);
      setExerciseLogs(logsRes.data);
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const handleExerciseSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/exercises/logs/${injuryId}?user_id=${userId}`, formData);
      fetchData();
      setShowExerciseForm(false);
      setFormData({ exercise_id: 1, pain_level: 5, difficulty: 5, notes: '' });
    } catch (error) {
      console.error('Error logging exercise:', error);
    }
  };

  if (loading) return <div className="text-center p-8">Loading...</div>;
  if (!injury) return <div className="text-center p-8">Injury not found</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">{injury.injury_type}</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Severity</h3>
          <p className="text-4xl font-bold text-red-500">{injury.severity}/10</p>
        </div>
        
        {prediction && (
          <>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Estimated Recovery</h3>
              <p className="text-2xl font-bold text-blue-500">{prediction.days_until_recovery} days</p>
              <p className="text-sm text-gray-600 mt-2">Recovery by: {new Date(prediction.estimated_recovery_date).toLocaleDateString()}</p>
              <p className="text-sm text-gray-600">Confidence: {prediction.confidence_percentage.toFixed(0)}%</p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Progress</h3>
              <div className="w-full bg-gray-300 rounded-full h-8">
                <div
                  className="bg-green-500 h-8 rounded-full flex items-center justify-center text-white font-bold"
                  style={{width: `${prediction.current_progress_percentage}%`}}
                >
                  {prediction.current_progress_percentage.toFixed(0)}%
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {analytics && (
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Analytics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Exercise Adherence</h3>
              <p className="text-2xl font-bold text-blue-500">{analytics.exercise_adherence_rate.toFixed(0)}%</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Recommendations</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                {analytics.recommended_next_steps.map((step, i) => (
                  <li key={i}>• {step}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Exercise Logs</h2>
        <button
          onClick={() => setShowExerciseForm(!showExerciseForm)}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          {showExerciseForm ? 'Cancel' : 'Log Exercise'}
        </button>
      </div>

      {showExerciseForm && (
        <form onSubmit={handleExerciseSubmit} className="bg-white p-6 rounded-lg shadow-md mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Pain Level (1-10)</label>
              <input
                type="number"
                min="1"
                max="10"
                value={formData.pain_level}
                onChange={(e) => setFormData({...formData, pain_level: parseInt(e.target.value)})}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Difficulty (1-10)</label>
              <input
                type="number"
                min="1"
                max="10"
                value={formData.difficulty}
                onChange={(e) => setFormData({...formData, difficulty: parseInt(e.target.value)})}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700">Notes</label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({...formData, notes: e.target.value})}
                rows="2"
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>
          <button
            type="submit"
            className="mt-4 bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600"
          >
            Log Exercise
          </button>
        </form>
      )}

      {exerciseLogs.length > 0 && (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Date</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Pain Level</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Difficulty</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Notes</th>
              </tr>
            </thead>
            <tbody>
              {exerciseLogs.map((log) => (
                <tr key={log.id} className="border-t border-gray-200 hover:bg-gray-50">
                  <td className="px-6 py-3 text-sm text-gray-600">{new Date(log.completed_at).toLocaleDateString()}</td>
                  <td className="px-6 py-3 text-sm text-gray-600">{log.pain_level}/10</td>
                  <td className="px-6 py-3 text-sm text-gray-600">{log.difficulty}/10</td>
                  <td className="px-6 py-3 text-sm text-gray-600">{log.notes || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default InjuryDetail;