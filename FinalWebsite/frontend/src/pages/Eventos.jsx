import React from 'react';
import { Link } from 'react-router-dom';
import { createPageUrl } from '../utils';
import { useQuery } from '@tanstack/react-query';
import { MapPin, Calendar, Loader2 } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import axios from 'axios';
import Layout from '../components/Layout';

export default function Eventos() {
    const { data: eventos, isLoading } = useQuery({
        queryKey: ['eventos'],
        queryFn: async () => {
            const response = await axios.get('http://localhost:5000/api/eventos');
            return response.data;
        },
    });

    return (
        <Layout currentPageName="Eventos">
            <div>
                {/* Header Banner */}
                <section className="py-8">
                    <div className="max-w-7xl mx-auto px-4">
                        <div className="bg-[#2E7D32] rounded-full py-3 px-8 inline-block w-full">
                            <h1 className="text-2xl md:text-3xl font-bold text-white uppercase ml-4">PRÓXIMOS EVENTOS</h1>
                        </div>
                    </div>
                </section>

                {/* Events List */}
                <section className="pb-12 bg-white">
                    <div className="max-w-7xl mx-auto px-4">
                        {isLoading ? (
                            <div className="flex justify-center py-12">
                                <Loader2 className="w-12 h-12 text-[#2E7D32] animate-spin" />
                            </div>
                        ) : eventos && eventos.length > 0 ? (
                            <div className="space-y-8">
                                {eventos.map((evento) => (
                                    <article
                                        key={evento.id}
                                        className="bg-white rounded-lg overflow-hidden flex flex-col md:flex-row gap-6"
                                    >
                                        {/* Event Image */}
                                        <div className="md:w-64 flex-shrink-0">
                                            {evento.imagen_url ? (
                                                <img
                                                    src={evento.imagen_url}
                                                    alt={evento.nombre_evento}
                                                    className="w-full h-auto object-cover rounded shadow-md"
                                                />
                                            ) : (
                                                <div className="w-full h-64 bg-gray-200 flex items-center justify-center rounded shadow-md">
                                                    <Calendar className="w-16 h-16 text-gray-400" />
                                                </div>
                                            )}
                                        </div>

                                        {/* Event Details */}
                                        <div className="flex-grow py-2 flex flex-col">
                                            <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-4">
                                                {evento.nombre_evento}
                                            </h2>

                                            <div className="space-y-3 text-gray-800 mb-6 flex-grow">
                                                <p className="flex items-center gap-2 font-bold text-sm">
                                                    <MapPin className="w-4 h-4" />
                                                    {evento.localizacion || 'Ubicación por confirmar'}
                                                </p>
                                                <p className="flex items-center gap-2 font-bold text-sm">
                                                    <Calendar className="w-4 h-4" />
                                                    {evento.fecha
                                                        ? format(new Date(evento.fecha), "d/MM/yyyy, HH:mm'H.'", { locale: es })
                                                        : 'Fecha por confirmar'
                                                    }
                                                </p>
                                            </div>

                                            <div className="flex justify-end mt-auto">
                                                <Link
                                                    to={createPageUrl(`ComprarEntrada?evento=${evento.id}`)}
                                                    className="bg-[#2E7D32] hover:bg-[#1B5E20] text-white font-bold px-8 py-2 rounded-full transition-colors text-sm uppercase"
                                                >
                                                    Ver más
                                                </Link>
                                            </div>
                                        </div>
                                    </article>
                                ))}

                                {/* Pagination Placeholder */}
                                <div className="border-t-2 border-[#2E7D32] mt-12 pt-4 flex gap-2">
                                    <button className="bg-[#1B5E20] text-white w-8 h-8 flex items-center justify-center font-bold text-sm">1</button>
                                    <button className="bg-gray-200 text-gray-700 w-8 h-8 flex items-center justify-center font-bold text-sm hover:bg-gray-300">2</button>
                                    <button className="bg-gray-200 text-gray-700 w-8 h-8 flex items-center justify-center font-bold text-sm hover:bg-gray-300">...</button>
                                    <button className="bg-gray-300 text-gray-800 px-3 h-8 flex items-center justify-center font-bold text-sm hover:bg-gray-400">Próxima página</button>
                                </div>

                            </div>
                        ) : (
                            <div className="text-center py-16">
                                <Calendar className="w-20 h-20 text-gray-300 mx-auto mb-4" />
                                <h3 className="text-xl font-semibold text-gray-600 mb-2">No hay eventos próximos</h3>
                                <p className="text-gray-500">Vuelve pronto para ver nuevos eventos benéficos</p>
                            </div>
                        )}
                    </div>
                </section>
            </div>
        </Layout>
    );
}
