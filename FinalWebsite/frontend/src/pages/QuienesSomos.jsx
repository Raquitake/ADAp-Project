import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import { createPageUrl } from '../utils';

export default function QuienesSomos() {
    const sections = [
        {
            title: "Nuestra misión",
            content: "Convertir el proceso de morir en un proceso de vida. Aunque no podemos añadir días a la vida, queremos añadir vida a los días, a través de nuestra forma especial de cuidar.",
            image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&h=600&fit=crop",
            alt: "Cuidados paliativos",
            reverse: false // Text Left, Image Right
        },
        {
            title: "Breve historia de Cudeca",
            content: "Desde nuestros inicios, hemos trabajado incansablemente para ofrecer cuidados paliativos de calidad. Lo que comenzó como un sueño se ha convertido en una realidad que ayuda a miles de personas cada año.",
            image: "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800&h=600&fit=crop",
            alt: "Historia de Cudeca",
            reverse: true // Image Left, Text Right
        },
        {
            title: "El equipo",
            content: "Gracias a un equipo entregado de médicos, enfermeros, psicólogos y trabajadores sociales, junto a voluntarios solidarios, Cudeca transforma el cuidado en humanidad, ofreciendo consuelo, respeto y esperanza.",
            image: "https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?w=800&h=600&fit=crop",
            alt: "Equipo de Cudeca",
            reverse: false // Text Left, Image Right
        },
        {
            title: "Nuestro centro",
            content: "En nuestro centro de cuidados paliativos encontrarás instalaciones modernas y acogedoras: la unidad de Hospitalización y la unidad de Día y Rehabilitación. También enviamos profesionales a dar atención domiciliaria.",
            image: "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&h=600&fit=crop",
            alt: "Centro de Cudeca",
            reverse: true // Image Left, Text Right
        }
    ];

    return (
        <Layout currentPageName="QuienesSomos">
            <div className="bg-white">
                {/* Hero / Intro Title - Optional, keeping it clean as per request, starting directly with sections */}

                {sections.map((section, index) => (
                    <section key={index} className="py-20 border-b border-gray-100 last:border-0">
                        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                            <div className="flex flex-col md:flex-row items-center gap-12 lg:gap-20">
                                {/* 
                                    Mobile: Image always first (order-1). Text second (order-2).
                                    Desktop: 
                                        If reverse (Image Left): Image order-1, Text order-2.
                                        If not reverse (Text Left): Text order-1, Image order-2.
                                    
                                    Wait, the requirement is:
                                    Mobile: Image Top -> Text Bottom.
                                    
                                    Let's handle the DOM order:
                                    If we put Image first in DOM, it's top on mobile.
                                    Then on desktop, if we want Text Left (not reverse), we need flex-row-reverse.
                                    If we want Image Left (reverse), we need flex-row.
                                */}

                                {/* Image Column */}
                                <div className={`w-full md:w-1/2 ${section.reverse ? 'md:order-1' : 'md:order-2'}`}>
                                    <div className="aspect-[4/3] w-full relative rounded-xl shadow-lg overflow-hidden group">
                                        <img
                                            src={section.image}
                                            alt={section.alt}
                                            className="w-full h-full object-cover transform transition-transform duration-700 group-hover:scale-105"
                                        />
                                    </div>
                                </div>

                                {/* Text Column */}
                                <div className={`w-full md:w-1/2 flex flex-col justify-center ${section.reverse ? 'md:order-2' : 'md:order-1'}`}>
                                    <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                                        {section.title}
                                    </h2>
                                    <p className="text-lg leading-relaxed text-gray-600">
                                        {section.content}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </section>
                ))}

                {/* CTA Section */}
                <section className="py-24 bg-gray-50">
                    <div className="max-w-4xl mx-auto px-4 text-center">
                        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                            Únete a nuestra causa
                        </h2>
                        <p className="text-xl text-gray-600 mb-12">
                            Tu apoyo es fundamental para que podamos seguir cuidando.
                        </p>

                        <div className="flex flex-col sm:flex-row justify-center items-center gap-6">
                            <Link
                                to={createPageUrl('socios')}
                                className="w-full sm:w-auto px-8 py-4 bg-[#2E7D32] text-white font-bold rounded-full shadow-lg hover:bg-[#1B5E20] transition-all hover:scale-105 text-center min-w-[200px]"
                            >
                                Hazte socio
                            </Link>
                            <Link
                                to={createPageUrl('voluntariado')} // Assuming route exists or will be created
                                className="w-full sm:w-auto px-8 py-4 bg-white text-[#2E7D32] border-2 border-[#2E7D32] font-bold rounded-full shadow-lg hover:bg-gray-50 transition-all hover:scale-105 text-center min-w-[200px]"
                            >
                                Voluntario
                            </Link>
                            <Link
                                to={createPageUrl('donar')}
                                className="w-full sm:w-auto px-8 py-4 bg-[#FBC02D] text-gray-900 font-bold rounded-full shadow-lg hover:bg-[#F9A825] transition-all hover:scale-105 text-center min-w-[200px]"
                            >
                                Dona
                            </Link>
                        </div>
                    </div>
                </section>
            </div>
        </Layout>
    );
}
