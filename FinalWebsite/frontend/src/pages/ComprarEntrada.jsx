import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { MapPin, Calendar, Loader2, CreditCard, Minus, Plus, CheckCircle } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import axios from 'axios';
import Layout from '../components/Layout';

export default function ComprarEntrada() {
    const urlParams = new URLSearchParams(window.location.search);
    const eventoId = urlParams.get('evento');

    const [formData, setFormData] = useState({
        nombre: '',
        apellidos: '',
        email: '',
        cantidad_entradas: 1,
        donacion_adicional: 0,
        metodo_pago: 'tarjeta',
        suscripcion_newsletter: false,
    });

    const [submitted, setSubmitted] = useState(false);

    const { data: evento, isLoading } = useQuery({
        queryKey: ['evento', eventoId],
        queryFn: async () => {
            const response = await axios.get('http://localhost:5000/api/eventos');
            const eventos = response.data;
            return eventos.find(e => e.id === parseInt(eventoId));
        },
        enabled: !!eventoId,
    });

    const createCompra = useMutation({
        mutationFn: async (data) => {
            await new Promise(resolve => setTimeout(resolve, 1500));
            return { success: true };
        },
        onSuccess: () => {
            setSubmitted(true);
        },
    });

    const precio = 10;
    const total = evento
        ? (precio * formData.cantidad_entradas) + formData.donacion_adicional
        : 0;

    const handleSubmit = (e) => {
        e.preventDefault();
        createCompra.mutate({
            ...formData,
            evento_id: eventoId,
            total: total,
            estado: 'pendiente',
        });
    };

    const updateQuantity = (delta) => {
        setFormData(prev => ({
            ...prev,
            cantidad_entradas: Math.max(1, prev.cantidad_entradas + delta)
        }));
    };

    if (isLoading) {
        return (
            <Layout currentPageName="Eventos">
                <div className="min-h-[60vh] flex items-center justify-center">
                    <Loader2 className="w-12 h-12 text-[#2E7D32] animate-spin" />
                </div>
            </Layout>
        );
    }

    if (submitted) {
        return (
            <Layout currentPageName="Eventos">
                <div className="min-h-[60vh] flex items-center justify-center px-4">
                    <div className="text-center max-w-md">
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                            <CheckCircle className="w-10 h-10 text-[#2E7D32]" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">¡Gracias por tu compra!</h2>
                        <p className="text-gray-600 mb-6">
                            Hemos recibido tu solicitud. Recibirás un correo electrónico con los detalles de tu entrada.
                        </p>
                    </div>
                </div>
            </Layout>
        );
    }

    if (!evento) {
        return (
            <Layout currentPageName="Eventos">
                <div className="min-h-[60vh] flex items-center justify-center">
                    <p className="text-gray-500">Evento no encontrado</p>
                </div>
            </Layout>
        );
    }

    return (
        <Layout currentPageName="Eventos">
            <div>
                {/* Event Banner Image */}
                <section className="relative">
                    {evento.imagen_url ? (
                        <div className="w-full">
                            <img
                                src={evento.imagen_url}
                                alt={evento.nombre_evento}
                                className="w-full h-auto object-cover max-h-[500px]"
                            />
                        </div>
                    ) : (
                        <div className="bg-[#2E7D32] py-24 text-center">
                            <h1 className="text-4xl font-bold text-white">{evento.nombre_evento}</h1>
                        </div>
                    )}
                </section>

                {/* Purchase Button */}
                <section className="bg-white py-8 text-center">
                    <button
                        onClick={() => document.getElementById('form-section').scrollIntoView({ behavior: 'smooth' })}
                        className="bg-[#FBC02D] hover:bg-[#F9A825] text-gray-900 font-bold px-12 py-4 rounded-full text-xl uppercase shadow-lg transition-transform hover:scale-105"
                    >
                        COMPRAR ENTRADA
                    </button>
                </section>

                {/* Event Details */}
                <section className="py-8 bg-white max-w-5xl mx-auto px-4">
                    <h2 className="text-3xl font-bold text-gray-900 mb-6">{evento.nombre_evento}</h2>

                    <div className="flex flex-col gap-4 mb-8">
                        <div className="flex items-start gap-3">
                            <MapPin className="w-6 h-6 text-black mt-1" />
                            <span className="font-bold text-lg">{evento.localizacion || 'Ubicación por confirmar'}</span>
                        </div>
                        <div className="flex items-start gap-3">
                            <Calendar className="w-6 h-6 text-black mt-1" />
                            <span className="font-bold text-lg">
                                {evento.fecha
                                    ? format(new Date(evento.fecha), "d/MM/yyyy, HH:mm'H.'", { locale: es })
                                    : 'Fecha por confirmar'
                                }
                            </span>
                        </div>
                    </div>

                    <div className="mb-8">
                        <h3 className="text-2xl font-bold text-gray-900 mb-4">Detalles del evento</h3>
                        <p className="text-gray-800 font-bold text-sm leading-relaxed whitespace-pre-line">
                            {evento.informacion || 'Descripción no disponible.'}
                        </p>
                        <button className="text-[#2E7D32] font-bold text-sm mt-2 hover:underline">Leer más</button>
                    </div>

                    <div className="border-t-2 border-[#2E7D32] pt-4">
                        <p className="font-bold text-xl">
                            Categoría: <span className="font-normal text-base">Cena, Gala.</span>
                        </p>
                    </div>
                </section>

                {/* Purchase Form */}
                <section id="form-section" className="py-12 bg-gray-50">
                    <div className="max-w-3xl mx-auto px-4">
                        <form onSubmit={handleSubmit} className="space-y-8">
                            {/* Step 1: Personal Data */}
                            <div>
                                <h3 className="text-lg font-bold text-gray-900 mb-6">PASO 1: Tus datos</h3>

                                <div className="space-y-4">
                                    <div className="flex items-center gap-4">
                                        <label htmlFor="nombre" className="font-bold text-gray-900 w-24 text-right">Nombre* :</label>
                                        <input
                                            id="nombre"
                                            value={formData.nombre}
                                            onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                                            required
                                            className="border border-gray-400 p-2 flex-grow"
                                        />
                                    </div>
                                    <div className="flex items-center gap-4">
                                        <label htmlFor="apellidos" className="font-bold text-gray-900 w-24 text-right">Apellidos*:</label>
                                        <input
                                            id="apellidos"
                                            value={formData.apellidos}
                                            onChange={(e) => setFormData({ ...formData, apellidos: e.target.value })}
                                            required
                                            className="border border-gray-400 p-2 flex-grow"
                                        />
                                    </div>
                                    <div className="flex items-center gap-4">
                                        <label htmlFor="email" className="font-bold text-gray-900 w-24 text-right">Correo* :</label>
                                        <input
                                            id="email"
                                            type="email"
                                            value={formData.email}
                                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                            required
                                            className="border border-gray-400 p-2 flex-grow"
                                        />
                                    </div>

                                    <div className="flex items-center gap-2 pt-2 ml-28">
                                        <input
                                            type="checkbox"
                                            id="newsletter"
                                            checked={formData.suscripcion_newsletter}
                                            onChange={(e) => setFormData({ ...formData, suscripcion_newsletter: e.target.checked })}
                                            className="w-4 h-4 border-gray-400"
                                        />
                                        <label htmlFor="newsletter" className="text-sm font-bold text-gray-900">
                                            Deseo suscribirme a comunicaciones de Cudeca.
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <div className="border-t-4 border-[#2E7D32] my-8"></div>

                            {/* Step 2: Summary and Payment */}
                            <div>
                                <h3 className="text-lg font-bold text-gray-900 mb-6">PASO 2: Resumen y Pago</h3>

                                <div className="border-t border-gray-300 pt-4 mb-8">
                                    <div className="flex items-center justify-between mb-4 max-w-md">
                                        <div className="flex items-center gap-2">
                                            <span className="font-bold text-gray-900 w-24 text-right">Entradas* :</span>
                                            <div className="border border-gray-400 p-2 w-32 bg-white h-10"></div>
                                            <span className="font-bold">€</span>
                                        </div>
                                        <div className="text-center">
                                            <span className="font-bold text-sm block mb-1">Cantidad</span>
                                            <div className="flex items-center border border-black">
                                                <button type="button" onClick={() => updateQuantity(-1)} className="px-2 py-1 border-r border-black hover:bg-gray-100">-</button>
                                                <span className="px-3 font-bold">{formData.cantidad_entradas}</span>
                                                <button type="button" onClick={() => updateQuantity(1)} className="px-2 py-1 border-l border-black hover:bg-gray-100">+</button>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="flex items-center gap-2 mb-4">
                                        <span className="font-bold text-gray-900 w-24 text-right">Donación* :</span>
                                        <input
                                            type="number"
                                            value={formData.donacion_adicional}
                                            onChange={(e) => setFormData({ ...formData, donacion_adicional: parseFloat(e.target.value) || 0 })}
                                            className="border border-gray-400 p-2 w-32"
                                        />
                                        <span className="font-bold">€</span>
                                    </div>

                                    <div className="flex items-center gap-2">
                                        <span className="font-bold text-gray-900 w-24 text-right">Total* :</span>
                                        <div className="border border-gray-400 p-2 w-32 bg-white h-10 flex items-center">
                                            {total.toFixed(2)}
                                        </div>
                                        <span className="font-bold">€</span>
                                    </div>
                                </div>

                                {/* Payment Methods */}
                                <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto">
                                    <button
                                        type="button"
                                        onClick={() => setFormData({ ...formData, metodo_pago: 'tarjeta' })}
                                        className={`rounded-full py-2 px-4 font-bold text-center transition-colors ${formData.metodo_pago === 'tarjeta' ? 'bg-gray-300' : 'bg-gray-200 hover:bg-gray-300'}`}
                                    >
                                        Pago con tarjeta
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setFormData({ ...formData, metodo_pago: 'paypal' })}
                                        className={`rounded-full py-2 px-4 font-bold text-center transition-colors ${formData.metodo_pago === 'paypal' ? 'bg-gray-300' : 'bg-gray-200 hover:bg-gray-300'}`}
                                    >
                                        Paypal
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setFormData({ ...formData, metodo_pago: 'bizum' })}
                                        className={`rounded-full py-2 px-4 font-bold text-center transition-colors ${formData.metodo_pago === 'bizum' ? 'bg-gray-300' : 'bg-gray-200 hover:bg-gray-300'}`}
                                    >
                                        Bizum
                                    </button>
                                </div>

                                <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto mt-8 items-center">
                                    {/* Placeholders for payment logos */}
                                    <div className="text-center text-4xl font-bold text-blue-800 italic">VISA</div>
                                    <div className="text-center text-4xl font-bold text-blue-600 italic">PayPal</div>
                                    <div className="text-center text-4xl font-bold text-cyan-500 italic">bizum</div>
                                </div>
                            </div>

                            <div className="border-t-4 border-[#2E7D32] my-8"></div>

                            <div className="text-center">
                                <div className="inline-block bg-gray-300 rounded-full px-8 py-2 font-bold text-gray-700 text-sm">
                                    Pago 100% seguro. Sin gastos de gestión
                                </div>
                            </div>

                        </form>
                    </div>
                </section>
            </div>
        </Layout>
    );
}
