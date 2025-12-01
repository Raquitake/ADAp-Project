import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import Layout from '../components/Layout';
import { createPageUrl } from '../utils';

export default function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [acceptedTerms, setAcceptedTerms] = useState(false);
    const [newsletter, setNewsletter] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const registerMutation = useMutation({
        mutationFn: async (userData) => {
            const response = await axios.post('http://localhost:5000/api/register', userData);
            return response.data;
        },
        onSuccess: (data) => {
            navigate('/');
        },
        onError: (err) => {
            setError(err.response?.data?.error || 'Error al registrarse');
        },
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        if (password !== confirmPassword) {
            setError('Las contraseñas no coinciden');
            return;
        }

        if (!acceptedTerms) {
            setError('Debes aceptar la Política de Privacidad y el Aviso Legal');
            return;
        }

        // Extract name from email for now as design doesn't have a name field explicitly shown in the form image provided
        // Wait, the design image DOES NOT show a name field, just Email, Password, Repeat Password.
        // But the backend requires a name. I will use the part before @ in email as default name.
        const name = email.split('@')[0];

        registerMutation.mutate({
            email,
            password,
            nombre: name
        });
    };

    return (
        <Layout currentPageName="Registro">
            <div className="min-h-screen relative flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8" style={{
                backgroundImage: 'url("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80")',
                backgroundSize: 'cover',
                backgroundPosition: 'center',
            }}>
                {/* Dark Overlay */}
                <div className="absolute inset-0 bg-black/60 backdrop-blur-sm z-0"></div>

                <div className="relative z-10 w-full max-w-md space-y-8">
                    {/* Title above card */}
                    <div className="text-center">
                        <h1 className="text-4xl font-bold text-white mb-2 tracking-tight">Únete a nosotros</h1>
                        <p className="text-gray-200 text-lg font-medium">Registra un usuario y comienza a ayudar YA</p>
                    </div>

                    {/* Card */}
                    <div className="bg-white p-8 rounded-2xl shadow-2xl">
                        <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">Crear cuenta</h2>

                        {error && (
                            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded mb-6 text-sm">
                                <p className="font-bold">Error</p>
                                <p>{error}</p>
                            </div>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-5">
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

                            <div>
                                <label htmlFor="confirmPassword" className="block text-sm font-bold text-gray-700 mb-2">Repetir Contraseña</label>
                                <input
                                    type="password"
                                    id="confirmPassword"
                                    placeholder="••••••••"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    className="w-full h-12 px-4 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none transition-all bg-gray-50 focus:bg-white"
                                    required
                                />
                            </div>

                            <div className="pt-2 space-y-4">
                                <div className="flex items-start gap-3">
                                    <input
                                        type="checkbox"
                                        id="terms"
                                        checked={acceptedTerms}
                                        onChange={(e) => setAcceptedTerms(e.target.checked)}
                                        className="mt-1 w-5 h-5 text-[#2E7D32] border-gray-300 rounded focus:ring-[#2E7D32] cursor-pointer shrink-0"
                                    />
                                    <label htmlFor="terms" className="text-sm text-gray-600 cursor-pointer leading-tight">
                                        Acepto la <a href="#" className="text-[#2E7D32] font-bold hover:underline">Política de Privacidad</a> y el <a href="#" className="text-[#2E7D32] font-bold hover:underline">Aviso Legal</a>.
                                    </label>
                                </div>

                                <div className="flex items-start gap-3">
                                    <input
                                        type="checkbox"
                                        id="newsletter"
                                        checked={newsletter}
                                        onChange={(e) => setNewsletter(e.target.checked)}
                                        className="mt-1 w-5 h-5 text-[#2E7D32] border-gray-300 rounded focus:ring-[#2E7D32] cursor-pointer shrink-0"
                                    />
                                    <label htmlFor="newsletter" className="text-sm text-gray-600 cursor-pointer leading-tight">
                                        Quiero recibir información sobre la forma especial de cuidar de la Fundación Cudeca.
                                    </label>
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={registerMutation.isPending}
                                className="w-full bg-[#2E7D32] hover:bg-[#1B5E20] text-white font-bold text-lg py-3.5 rounded-lg transition-all transform hover:scale-[1.02] shadow-md disabled:opacity-70 disabled:cursor-not-allowed mt-4"
                            >
                                {registerMutation.isPending ? 'Creando cuenta...' : 'Registrarse'}
                            </button>
                        </form>

                        <div className="text-center mt-8 pt-6 border-t border-gray-100">
                            <p className="text-gray-600">
                                ¿Ya tienes cuenta?{' '}
                                <Link to={createPageUrl('login')} className="text-[#2E7D32] font-bold hover:underline">
                                    Inicia sesión aquí
                                </Link>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
}
