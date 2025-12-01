import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { createPageUrl } from '../utils';
import { Menu, X } from 'lucide-react';

export default function Header({ currentPage }) {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const navItems = [
        { name: 'INICIO', page: 'Inicio' },
        { name: 'QUIÉNES SOMOS', page: 'QuienesSomos' },
        { name: 'EVENTOS', page: 'Eventos' },
        { name: 'DONAR', page: 'Donar' },
        { name: 'SOCIOS', page: 'Socios' },
        { name: 'CONTACTO', page: 'Contacto' },
    ];

    // Import images directly if possible, or use relative paths assuming they are in public or handled by vite
    // Since we are in src/components, and images are in src/assets/images
    // We should import them to ensure they are bundled correctly.
    // However, the user provided paths like @[FinalWebsite/frontend/src/assets/images/logo.png]
    // I will assume standard Vite import behavior.

    return (
        <header className="relative font-sans">
            {/* Top section with logo and background */}
            <div
                className="relative h-32 md:h-40 bg-cover bg-center overflow-hidden"
                style={{ backgroundImage: "url('/src/assets/images/fondo-header-middle.png')" }}
            >
                {/* Overlay for better text readability if needed, though the image might be enough */}
                <div className="absolute inset-0 bg-green-900/10"></div>

                <div className="max-w-7xl mx-auto px-4 h-full flex items-center justify-between relative z-10">
                    {/* Logo */}
                    <div className="flex-shrink-0 py-2">
                        <img
                            src="/src/assets/images/logo.png"
                            alt="Fundación Cudeca"
                            className="h-24 md:h-32 w-auto object-contain drop-shadow-md"
                        />
                    </div>

                    {/* Sunflower decoration - Positioned absolutely to the right */}
                    <div className="absolute right-0 bottom-0 h-full w-auto flex items-end justify-end pointer-events-none">
                        <img
                            src="/src/assets/images/girasol-menu.png"
                            alt="Sunflower Decoration"
                            className="h-[120%] w-auto object-contain translate-y-4 translate-x-4 md:translate-x-0"
                        />
                    </div>

                    {/* Mobile menu button */}
                    <button
                        className="md:hidden z-20 text-white bg-[#2E7D32] p-2 rounded shadow-lg"
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    >
                        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>
            </div>

            {/* Navigation Bar */}
            <nav className="bg-[#2E7D32] border-t border-green-800 shadow-md relative z-20">
                <div className="max-w-7xl mx-auto px-4">
                    {/* Desktop navigation */}
                    <div className="hidden md:flex justify-between items-center">
                        <ul className="flex space-x-1">
                            {navItems.map((item) => (
                                <li key={item.page}>
                                    <Link
                                        to={createPageUrl(item.page)}
                                        className={`block px-5 py-4 text-sm font-bold tracking-wide transition-all duration-200 uppercase
                                            ${currentPage === item.page
                                                ? 'bg-[#1B5E20] text-yellow-400 shadow-inner'
                                                : 'text-white hover:bg-[#256628] hover:text-yellow-200'
                                            }`}
                                    >
                                        {item.name}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                        <div className="py-2">
                            <Link
                                to={createPageUrl('login')}
                                className="bg-[#556B2F] hover:bg-[#4a5e29] text-[#FFD700] font-bold px-6 py-2 rounded shadow-md transition-colors uppercase text-sm tracking-wider border border-[#6b853b]"
                            >
                                LOG IN
                            </Link>
                        </div>
                    </div>

                    {/* Mobile navigation */}
                    {mobileMenuOpen && (
                        <ul className="md:hidden bg-[#2E7D32] border-t border-green-600 animate-in slide-in-from-top-2">
                            {navItems.map((item) => (
                                <li key={item.page}>
                                    <Link
                                        to={createPageUrl(item.page)}
                                        className={`block px-6 py-4 text-sm font-bold border-b border-green-700 uppercase
                                            ${currentPage === item.page
                                                ? 'bg-[#1B5E20] text-yellow-400'
                                                : 'text-white hover:bg-[#256628]'
                                            }`}
                                        onClick={() => setMobileMenuOpen(false)}
                                    >
                                        {item.name}
                                    </Link>
                                </li>
                            ))}
                            <li className="p-4">
                                <Link
                                    to={createPageUrl('login')}
                                    className="block w-full text-center bg-[#556B2F] text-[#FFD700] font-bold px-6 py-3 rounded shadow-md uppercase text-sm"
                                    onClick={() => setMobileMenuOpen(false)}
                                >
                                    LOG IN
                                </Link>
                            </li>
                        </ul>
                    )}
                </div>
            </nav>
        </header>
    );
}
