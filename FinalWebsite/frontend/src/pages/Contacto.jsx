import React from 'react';
import Layout from '../components/Layout';

export default function Contacto() {
    return (
        <Layout currentPageName="Contacto">
            <div>
                {/* Header */}
                <section className="bg-[#2E7D32] py-4">
                    <div className="max-w-7xl mx-auto px-4">
                        {/* Breadcrumb or Title if needed, but image shows just nav bar then content */}
                    </div>
                </section>

                <div className="max-w-7xl mx-auto px-4 py-12">
                    <h2 className="text-3xl font-bold text-[#2E7D32] mb-12 border-b-2 border-[#2E7D32] pb-4 inline-block">Información de contacto</h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                        {/* Phone Numbers */}
                        <div className="flex gap-6 p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="w-1.5 bg-[#2E7D32] self-stretch shrink-0 rounded-full"></div>
                            <div>
                                <h3 className="text-xl font-bold text-gray-900 mb-3">Números de teléfono</h3>
                                <p className="text-gray-700 text-lg">
                                    <span className="font-medium">Número principal:</span> <br />
                                    <a href="tel:+34952564910" className="text-[#2E7D32] font-bold text-2xl hover:underline">+34 952 564 910</a>
                                </p>
                            </div>
                        </div>

                        {/* Emails */}
                        <div className="flex gap-6 p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="w-1.5 bg-[#2E7D32] self-stretch shrink-0 rounded-full"></div>
                            <div className="flex-grow">
                                <h3 className="text-xl font-bold text-gray-900 mb-3">Correos electrónicos</h3>
                                <div className="space-y-3 text-lg">
                                    <div className="flex flex-col sm:flex-row sm:justify-between border-b border-gray-100 pb-2 last:border-0">
                                        <span className="font-medium text-gray-600">General:</span>
                                        <a href="mailto:cudeca@cudeca.org" className="text-[#2E7D32] font-bold hover:underline">cudeca@cudeca.org</a>
                                    </div>
                                    <div className="flex flex-col sm:flex-row sm:justify-between border-b border-gray-100 pb-2 last:border-0">
                                        <span className="font-medium text-gray-600">Socios:</span>
                                        <a href="mailto:socios@cudeca.org" className="text-[#2E7D32] font-bold hover:underline">socios@cudeca.org</a>
                                    </div>
                                    <div className="flex flex-col sm:flex-row sm:justify-between border-b border-gray-100 pb-2 last:border-0">
                                        <span className="font-medium text-gray-600">Voluntariado:</span>
                                        <a href="mailto:voluntariado@cudeca.org" className="text-[#2E7D32] font-bold hover:underline">voluntariado@cudeca.org</a>
                                    </div>
                                    <div className="flex flex-col sm:flex-row sm:justify-between border-b border-gray-100 pb-2 last:border-0">
                                        <span className="font-medium text-gray-600">Eventos:</span>
                                        <a href="mailto:eventos@cudeca.org" className="text-[#2E7D32] font-bold hover:underline">eventos@cudeca.org</a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Physical Address */}
                        <div className="flex gap-6 p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="w-1.5 bg-[#2E7D32] self-stretch shrink-0 rounded-full"></div>
                            <div>
                                <h3 className="text-xl font-bold text-gray-900 mb-3">Dirección física</h3>
                                <p className="text-gray-700 text-lg leading-relaxed">
                                    <span className="font-bold block mb-1">Centro de cuidados paliativos / Oficina central:</span>
                                    Avenida del Cosmos, s/n<br />
                                    29631 - Arroyo de la Miel, Málaga
                                </p>
                            </div>
                        </div>

                        {/* Social Media */}
                        <div className="flex gap-6 p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="w-1.5 bg-[#2E7D32] self-stretch shrink-0 rounded-full"></div>
                            <div>
                                <h3 className="text-xl font-bold text-gray-900 mb-3">Redes sociales</h3>
                                <div className="space-y-2 text-lg font-medium text-[#2E7D32]">
                                    <a href="https://www.instagram.com/voluntariadocudeca" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:underline hover:text-[#1B5E20] transition-colors">
                                        <span>Instagram Voluntariado</span>
                                    </a>
                                    <a href="https://www.facebook.com/voluntarioscudeca" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:underline hover:text-[#1B5E20] transition-colors">
                                        <span>Facebook Voluntarios</span>
                                    </a>
                                    <a href="https://api.whatsapp.com/send?phone=34671048304" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:underline hover:text-[#1B5E20] transition-colors">
                                        <span>WhatsApp</span>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
}
