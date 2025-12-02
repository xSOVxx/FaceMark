import React, { useState, useEffect } from 'react';
import { getProfessors, createProfessor, getStudents, createStudent, getClasses, createClass, assignStudentToClass } from '../api/admin';
import { Users, GraduationCap, BookOpen, Plus } from 'lucide-react';

const AdminDashboard = () => {
    const [activeTab, setActiveTab] = useState('professors');
    const [professors, setProfessors] = useState([]);
    const [students, setStudents] = useState([]);
    const [classes, setClasses] = useState([]);

    // Forms
    const [profForm, setProfForm] = useState({ nombre: '', correo: '', password: '' });
    const [studentForm, setStudentForm] = useState({ nombre: '', codigo: '' });
    const [classForm, setClassForm] = useState({ nombre: '', profesor_id: '' });
    const [assignForm, setAssignForm] = useState({ class_id: '', student_id: '' });

    useEffect(() => {
        fetchData();
    }, [activeTab]);

    const fetchData = async () => {
        if (activeTab === 'professors') {
            const data = await getProfessors();
            setProfessors(data);
        } else if (activeTab === 'students') {
            const data = await getStudents();
            setStudents(data);
        } else if (activeTab === 'classes') {
            const data = await getClasses();
            setClasses(data);
            // Also fetch profs for dropdown
            const profs = await getProfessors();
            setProfessors(profs);
        }
    };

    const handleCreateProfessor = async (e) => {
        e.preventDefault();
        await createProfessor(profForm);
        setProfForm({ nombre: '', correo: '', password: '' });
        fetchData();
    };

    const handleCreateStudent = async (e) => {
        e.preventDefault();
        await createStudent(studentForm);
        setStudentForm({ nombre: '', codigo: '' });
        fetchData();
    };

    const handleCreateClass = async (e) => {
        e.preventDefault();
        await createClass(classForm);
        setClassForm({ nombre: '', profesor_id: '' });
        fetchData();
    };

    const handleAssignStudent = async (e) => {
        e.preventDefault();
        await assignStudentToClass(assignForm.class_id, assignForm.student_id);
        setAssignForm({ class_id: '', student_id: '' });
        alert('Student assigned!');
    };

    return (
        <div className="space-y-6">
            <div className="flex space-x-4 border-b border-gray-200 pb-2">
                <button
                    onClick={() => setActiveTab('professors')}
                    className={`flex items-center px-4 py-2 rounded-lg ${activeTab === 'professors' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'}`}
                >
                    <Users className="w-5 h-5 mr-2" />
                    Professors
                </button>
                <button
                    onClick={() => setActiveTab('students')}
                    className={`flex items-center px-4 py-2 rounded-lg ${activeTab === 'students' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'}`}
                >
                    <GraduationCap className="w-5 h-5 mr-2" />
                    Students
                </button>
                <button
                    onClick={() => setActiveTab('classes')}
                    className={`flex items-center px-4 py-2 rounded-lg ${activeTab === 'classes' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'}`}
                >
                    <BookOpen className="w-5 h-5 mr-2" />
                    Classes
                </button>
            </div>

            {activeTab === 'professors' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-4">Create Professor</h3>
                        <form onSubmit={handleCreateProfessor} className="space-y-4">
                            <input placeholder="Name" value={profForm.nombre} onChange={e => setProfForm({ ...profForm, nombre: e.target.value })} className="w-full border p-2 rounded" required />
                            <input placeholder="Email" value={profForm.correo} onChange={e => setProfForm({ ...profForm, correo: e.target.value })} className="w-full border p-2 rounded" required />
                            <input type="password" placeholder="Password" value={profForm.password} onChange={e => setProfForm({ ...profForm, password: e.target.value })} className="w-full border p-2 rounded" required />
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 flex items-center justify-center">
                                <Plus className="w-4 h-4 mr-2" /> Create
                            </button>
                        </form>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-4">List</h3>
                        <ul className="space-y-2">
                            {professors.map(p => (
                                <li key={p.id} className="border-b pb-2">{p.nombre} ({p.correo})</li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}

            {activeTab === 'students' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-4">Create Student</h3>
                        <form onSubmit={handleCreateStudent} className="space-y-4">
                            <input placeholder="Name" value={studentForm.nombre} onChange={e => setStudentForm({ ...studentForm, nombre: e.target.value })} className="w-full border p-2 rounded" required />
                            <input placeholder="Code" value={studentForm.codigo} onChange={e => setStudentForm({ ...studentForm, codigo: e.target.value })} className="w-full border p-2 rounded" required />
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 flex items-center justify-center">
                                <Plus className="w-4 h-4 mr-2" /> Create
                            </button>
                        </form>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-4">List</h3>
                        <ul className="space-y-2">
                            {students.map(s => (
                                <li key={s.id} className="border-b pb-2">{s.nombre} ({s.codigo})</li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}

            {activeTab === 'classes' && (
                <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h3 className="text-lg font-semibold mb-4">Create Class</h3>
                            <form onSubmit={handleCreateClass} className="space-y-4">
                                <input placeholder="Class Name" value={classForm.nombre} onChange={e => setClassForm({ ...classForm, nombre: e.target.value })} className="w-full border p-2 rounded" required />
                                <select value={classForm.profesor_id} onChange={e => setClassForm({ ...classForm, profesor_id: e.target.value })} className="w-full border p-2 rounded" required>
                                    <option value="">Select Professor</option>
                                    {professors.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
                                </select>
                                <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 flex items-center justify-center">
                                    <Plus className="w-4 h-4 mr-2" /> Create
                                </button>
                            </form>
                        </div>
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h3 className="text-lg font-semibold mb-4">Assign Student</h3>
                            <form onSubmit={handleAssignStudent} className="space-y-4">
                                <input placeholder="Class ID" value={assignForm.class_id} onChange={e => setAssignForm({ ...assignForm, class_id: e.target.value })} className="w-full border p-2 rounded" required />
                                <input placeholder="Student ID" value={assignForm.student_id} onChange={e => setAssignForm({ ...assignForm, student_id: e.target.value })} className="w-full border p-2 rounded" required />
                                <button type="submit" className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 flex items-center justify-center">
                                    <Plus className="w-4 h-4 mr-2" /> Assign
                                </button>
                            </form>
                        </div>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-4">Class List</h3>
                        <ul className="space-y-2">
                            {classes.map(c => (
                                <li key={c.id} className="border-b pb-2 flex justify-between">
                                    <span>{c.nombre}</span>
                                    <span className="text-gray-500 text-sm">ID: {c.id}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdminDashboard;
