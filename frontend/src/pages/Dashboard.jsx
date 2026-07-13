import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function Dashboard({ userId }) {
  const [injuries, setInjuries] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    injury_type: '',
    severity: 5,
    description: '',
    start_date: new Date().toISOString().split('T')[0],
    expected_recovery_weeks: 12
  });

  useEffect(() => {
    fetchInjuries();
  }, [userId]);

  const fetchInjuries = async () => {
    try {
      const response = await axios.get(`${API_URL}/injuries/${userId}`);
      setInjuries(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching injuries:', error);
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/injuries/${userId}`, formData);
      fetchInjuries();
      setShowForm(false);
      setFormData({
        injury_type: '',
        severity: 5,
        description: '',
        start_date: new Date().toISOString().split('T')[0],
        expected_recovery_weeks: 12
      });
    } catch (error) {
      console.error('Error creating injury:', error);
    }
  };

  if (loading) return <div className="text-center p-8">Loading...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Your Recovery Journey</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600"
        >
          {showForm ? 'Cancel' : 'Log Injury'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Injury Type</label>
              <input
                type="text"
                required
                value={formData.injury_type}
                onChange={(e) => setFormData({...formData, injury_type: e.target.value})}
                placeholder="e.g., ACL tear, Shoulder dislocation"
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Severity (1-10)</label>
              <input
                type="number"
                min="1"
                max="10"
                value={formData.severity}
                onChange={(e) => setFormData({...formData, severity: parseInt(e.target.value)})}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Start Date</label>
              <input
                type="date"
                value={formData.start_date}
                onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Expected Recovery (weeks)</label>
              <input
                type="number"
                value={formData.expected_recovery_weeks}
                onChange={(e) => setFormData({...formData, expected_recovery_weeks: parseInt(e.target.value)})}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                rows="3"
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>
          <button
            type="submit"
            className="mt-4 bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600"
          >
            Save Injury
          </button>
        </form>
      )}

      {injuries.length === 0 ? (
        <div className="bg-white p-8 rounded-lg shadow-md text-center">
          <p className="text-gray-600">No injuries logged yet. Start tracking your recovery!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {injuries.map((injury) => (
            <Link
              key={injury.id}
              to={`/injury/${injury.id}`}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer"
            >
              <h3 className="text-xl font-bold text-gray-900 mb-2">{injury.injury_type}</h3>
              <p className="text-sm text-gray-600 mb-2">Severity: {injury.severity}/10</p>
              <p className="text-sm text-gray-600 mb-2">Started: {new Date(injury.start_date).toLocaleDateString()}</p>
              <p className="text-xs text-blue-500 mt-4">Click to view details →</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default Dashboard;