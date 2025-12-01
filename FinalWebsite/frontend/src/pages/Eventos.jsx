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
                            <div className="space-y-12">
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                    {eventos.map((evento) => (
                                        <article
                                            key={evento.id}
                                            className="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 flex flex-col h-full border border-gray-100"
                                        >
                                            {/* Event Image */}
                                            <div className="relative h-48 overflow-hidden group">
                                                {evento.imagen_url ? (
                                                    <img
                                                        src={evento.imagen_url}
                                                        alt={evento.nombre_evento}
                                                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                                                    />
                                                ) : (
                                                    <div className="w-full h-full bg-gray-100 flex items-center justify-center">
                                                        <Calendar className="w-12 h-12 text-gray-300" />
                                                    </div>
                                                )}
                                                <div className="absolute top-0 right-0 bg-[#2E7D32] text-white text-xs font-bold px-3 py-1 rounded-bl-lg">
                                                    EVENTO
                                                </div>
                                            </div>

                                            {/* Event Details */}
                                            <div className="p-6 flex flex-col flex-grow">
                                                <h2 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2 min-h-[3.5rem]">
                                                    {evento.nombre_evento}
                                                </h2>

                                                <div className="space-y-3 text-gray-600 mb-6 flex-grow">
                                                    <p className="flex items-start gap-3 text-sm">
                                                        <MapPin className="w-5 h-5 text-[#2E7D32] flex-shrink-0 mt-0.5" />
                                                        <span className="font-medium">{evento.localizacion || 'Ubicación por confirmar'}</span>
                                                    </p>
                                                    <p className="flex items-start gap-3 text-sm">
                                                        <Calendar className="w-5 h-5 text-[#2E7D32] flex-shrink-0 mt-0.5" />
                                                        <span className="font-medium">
                                                            {evento.fecha
                                                                ? format(new Date(evento.fecha), "d 'de' MMMM, yyyy • HH:mm'h'", { locale: es })
                                                                : 'Fecha por confirmar'
                                                            }
                                                        </span>
                                                    </p>
                                                </div>

                                                <div className="mt-auto pt-4 border-t border-gray-100">
                                                    <Link
                                                        to={createPageUrl(`ComprarEntrada?evento=${evento.id}`)}
                                                        className="block w-full bg-[#2E7D32] hover:bg-[#1B5E20] text-white font-bold py-3 rounded-lg text-center transition-colors uppercase text-sm tracking-wide"
                                                    >
                                                        Comprar Entradas
                                                    </Link>
                                                </div>
                                            </div>
                                        </article>
                                    ))}
                                </div>

                                {/* Pagination Placeholder */}
                                <div className="flex justify-center gap-2 pt-8">
                                    <button className="w-10 h-10 rounded-full bg-[#2E7D32] text-white flex items-center justify-center font-bold text-sm shadow-md transition-transform hover:scale-105">1</button>
                                    <button className="w-10 h-10 rounded-full bg-white border border-gray-300 text-gray-700 flex items-center justify-center font-bold text-sm hover:bg-gray-50 hover:border-[#2E7D32] transition-colors">2</button>
                                    <button className="w-10 h-10 rounded-full bg-white border border-gray-300 text-gray-700 flex items-center justify-center font-bold text-sm hover:bg-gray-50">...</button>
                                    <button className="px-4 h-10 rounded-full bg-white border border-gray-300 text-gray-700 flex items-center justify-center font-bold text-sm hover:bg-gray-50 hover:border-[#2E7D32] transition-colors uppercase">Siguiente</button>
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
