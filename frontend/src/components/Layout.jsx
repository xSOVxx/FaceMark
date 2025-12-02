import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, User, LayoutDashboard } from 'lucide-react';

const Layout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            <nav className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex items-center">
                            <LayoutDashboard className="h-8 w-8 text-blue-600" />
                            <span className="ml-2 text-xl font-bold text-gray-900">FaceMark</span>
                        </div>
                        <div className="flex items-center space-x-4">
                            <div className="flex items-center text-gray-700">
                                <User className="h-5 w-5 mr-2" />
                                <span>{user?.username}</span>
                            </div>
                            <button
                                onClick={handleLogout}
                                className="flex items-center text-red-600 hover:text-red-800 transition"
                            >
                                <LogOut className="h-5 w-5 mr-1" />
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </nav>
            <main className="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;
