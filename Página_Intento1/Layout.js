import React from 'react';
import Header from '@/components/cudeca/Header';
import Footer from '@/components/cudeca/Footer';

export default function Layout({ children, currentPageName }) {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <style>{`
        :root {
          --cudeca-green: #2E7D32;
          --cudeca-green-dark: #1B5E20;
          --cudeca-yellow: #FFC107;
          --cudeca-orange: #FF9800;
        }
        
        body {
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .cudeca-btn {
          background-color: var(--cudeca-green);
          color: white;
          padding: 12px 32px;
          border-radius: 25px;
          font-weight: 600;
          transition: all 0.3s ease;
        }
        
        .cudeca-btn:hover {
          background-color: var(--cudeca-green-dark);
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
        }
        
        .cudeca-btn-outline {
          background-color: transparent;
          border: 2px solid var(--cudeca-green);
          color: var(--cudeca-green);
        }
        
        .cudeca-btn-outline:hover {
          background-color: var(--cudeca-green);
          color: white;
        }
      `}</style>
      
      <Header currentPage={currentPageName} />
      
      <main className="flex-grow">
        {children}
      </main>
      
      <Footer />
    </div>
  );
}