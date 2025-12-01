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
                    <h2 className="text-2xl font-bold text-gray-900 mb-8">Información de contacto:</h2>

                    <div className="space-y-8">
                        {/* Phone Numbers */}
                        <div className="flex gap-4">
                            <div className="w-2 bg-[#2E7D32] self-stretch shrink-0"></div>
                            <div>
                                <h3 className="text-lg font-bold text-gray-900 mb-2">Números de teléfono:</h3>
                                <p className="text-gray-800 text-lg">
                                    <span className="font-bold">Número principal:</span> <span className="text-[#2E7D32] font-bold">+34 952 564 910</span>
                                </p>
                            </div>
                        </div>

                        {/* Emails */}
                        <div className="flex gap-4">
                            <div className="w-2 bg-[#2E7D32] self-stretch shrink-0"></div>
                            <div>
                                <h3 className="text-lg font-bold text-gray-900 mb-2">Correos:</h3>
                                <div className="space-y-1 text-lg">
                                    <p className="text-gray-800">
                                        <span className="font-bold">Correo principal:</span> <a href="mailto:cudeca@cudeca.org" className="text-[#2E7D32] font-bold hover:underline">cudeca@cudeca.org</a>
                                    </p>
                                    <p className="text-gray-800">
                                        <span className="font-bold">Socios:</span> <a href="mailto:socios@cudeca.org" className="text-[#2E7D32] font-bold hover:underline">socios@cudeca.org</a>
                                    </p>
                                    <p className="text-gray-800">
                                        <span className="font-bold">Voluntariado:</span> <a href="mailto:voluntariado@cudeca.org" className="text-[#2E7D32] font-bold hover:underline">voluntariado@cudeca.org</a>
                                    </p>
                                    <p className="text-gray-800">
                                        <span className="font-bold">Eventos:</span> <a href="mailto:eventos@cudeca.org" className="text-[#2E7D32] font-bold hover:underline">eventos@cudeca.org</a>
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Physical Address */}
                        <div className="flex gap-4">
                            <div className="w-2 bg-[#2E7D32] self-stretch shrink-0"></div>
                            <div>
                                <h3 className="text-lg font-bold text-gray-900 mb-2">Direcciones físicas:</h3>
                                <p className="text-gray-800 text-lg font-bold">
                                    Centro de cuidados paliativos / oficina central: Avenida del<br />
                                    Cosmos, s/n - 29631 - Arroyo de la Miel, Málaga
                                </p>
                            </div>
                        </div>

                        {/* Social Media */}
                        <div className="flex gap-4">
                            <div className="w-2 bg-[#2E7D32] self-stretch shrink-0"></div>
                            <div>
                                <h3 className="text-lg font-bold text-gray-900 mb-2">Redes sociales:</h3>
                                <div className="space-y-1 text-lg font-bold text-[#2E7D32]">
                                    <a href="https://www.instagram.com/voluntariadocudeca" target="_blank" rel="noopener noreferrer" className="block hover:underline">
                                        https://www.instagram.com/voluntariadocudeca
                                    </a>
                                    <a href="https://www.facebook.com/voluntarioscudeca" target="_blank" rel="noopener noreferrer" className="block hover:underline">
                                        https://www.facebook.com/voluntarioscudeca
                                    </a>
                                    <a href="https://api.whatsapp.com/send?phone=34671048304" target="_blank" rel="noopener noreferrer" className="block hover:underline">
                                        https://api.whatsapp.com/send?phone=34671048304
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
