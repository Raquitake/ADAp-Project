import React from 'react';
import Header from './Header';
import Footer from './Footer';

export default function Layout({ children, currentPageName }) {
    return (
        <div className="min-h-screen flex flex-col bg-white">
            {/* Styles are handled by Tailwind, but custom variables can be defined in index.css if needed */}

            <Header currentPage={currentPageName} />

            <main className="flex-grow">
                {children}
            </main>

            <Footer />
        </div>
    );
}
