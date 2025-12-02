import React, { useState, useEffect } from 'react';
import { getMyClasses } from '../api/professor';
import { useNavigate } from 'react-router-dom';
import { Calendar, UserCheck } from 'lucide-react';

const ProfessorDashboard = () => {
    const [classes, setClasses] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchClasses();
    }, []);

    const fetchClasses = async () => {
        const data = await getMyClasses();
        setClasses(data);
    };

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-800">My Classes</h1>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {classes.map((cls) => (
                    <div key={cls.id} className="bg-white p-6 rounded-lg shadow hover:shadow-md transition">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-xl font-semibold text-gray-900">{cls.nombre}</h3>
                            <Calendar className="text-blue-500 w-6 h-6" />
                        </div>
                        <p className="text-gray-500 mb-4">ID: {cls.id}</p>
                        <button
                            onClick={() => navigate(`/attendance/${cls.id}`)}
                            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 flex items-center justify-center"
                        >
                            <UserCheck className="w-5 h-5 mr-2" />
                            Take Attendance
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ProfessorDashboard;
