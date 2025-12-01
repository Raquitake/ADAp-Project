import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import Layout from '../components/Layout';
import { createPageUrl } from '../utils';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const loginMutation = useMutation({
        mutationFn: async (credentials) => {
            const response = await axios.post('http://localhost:5000/api/login', credentials);
            return response.data;
        },
        onSuccess: (data) => {
            // Store user data/token if needed (e.g., localStorage)
            // For now, just redirect to dashboard/home
            navigate('/');
        },
        onError: (err) => {
            setError(err.response?.data?.error || 'Error al iniciar sesión');
        },
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');
        loginMutation.mutate({ email, password });
    };

    return (
        <Layout currentPageName="Login">
            <div className="min-h-screen relative flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8" style={{
                backgroundImage: 'url("https://images.unsplash.com/photo-1559027615-cd4628902d4a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80")',
                backgroundSize: 'cover',
                backgroundPosition: 'center',
            }}>
                {/* Dark Overlay */}
                <div className="absolute inset-0 bg-black/60 backdrop-blur-sm z-0"></div>

                <div className="relative z-10 w-full max-w-md space-y-8">
                    {/* Title above card */}
                    <div className="text-center">
                        <h1 className="text-4xl font-bold text-white mb-2 tracking-tight">Fundación Cudeca</h1>
                        <p className="text-gray-200 text-lg font-medium">Cada pequeño gesto cuenta</p>
                    </div>

                    {/* Card */}
                    <div className="bg-white p-8 rounded-2xl shadow-2xl">
                        <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">Iniciar sesión</h2>

                        {error && (
                            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded mb-6 text-sm">
                                <p className="font-bold">Error</p>
                                <p>{error}</p>
                            </div>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div>
                                <label htmlFor="email" className="block text-sm font-bold text-gray-700 mb-2">Email</label>
                                <input
                                    type="email"
                                    id="email"
                                    placeholder="tu@email.com"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full h-12 px-4 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none transition-all bg-gray-50 focus:bg-white"
                                    required
                                />
                            </div>

                            <div>
                                <label htmlFor="password" className="block text-sm font-bold text-gray-700 mb-2">Contraseña</label>
                                <input
                                    type="password"
                                    id="password"
                                    placeholder="••••••••"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full h-12 px-4 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none transition-all bg-gray-50 focus:bg-white"
                                    required
                                />
                            </div>

                            <button
                                type="submit"
                                disabled={loginMutation.isPending}
                                className="w-full bg-[#2E7D32] hover:bg-[#1B5E20] text-white font-bold text-lg py-3.5 rounded-lg transition-all transform hover:scale-[1.02] shadow-md disabled:opacity-70 disabled:cursor-not-allowed"
                            >
                                {loginMutation.isPending ? 'Iniciando sesión...' : 'Iniciar sesión'}
                            </button>
                        </form>

                        <div className="text-center mt-8 pt-6 border-t border-gray-100">
                            <p className="text-gray-600">
                                ¿Todavía no tienes cuenta?{' '}
                                <Link to={createPageUrl('registro')} className="text-[#2E7D32] font-bold hover:underline">
                                    Regístrate aquí
                                </Link>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
}
