import React, { useState } from 'react';
import { CreditCard, CheckCircle, Loader2 } from 'lucide-react';
import Layout from '../components/Layout';

export default function Donar() {
    const [formData, setFormData] = useState({
        cantidad: '',
        enMemoria: false,
        nombre: '',
        apellidos: '',
        email: '',
        telefono: '',
        movil: '',
        fechaNacimiento: '',
        formaConocernos: '',
        datosAdicionales: false,
        deduccionesFiscales: false,
        dni: '',
        direccion: '',
        codigoPostal: '',
        poblacion: '',
        provincia: '',
        pais: '',
        metodoPago: 'Tarjeta de crédito/débito',
        aceptoPolitica: false,
        recibirInformacion: false
    });

    const [submitted, setSubmitted] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        setSubmitted(true);
        setIsSubmitting(false);
    };

    if (submitted) {
        return (
            <Layout currentPageName="Donar">
                <div className="min-h-[60vh] flex items-center justify-center px-4">
                    <div className="text-center max-w-md">
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                            <CheckCircle className="w-10 h-10 text-[#2E7D32]" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">¡Gracias por tu donación!</h2>
                        <p className="text-gray-600 mb-6">
                            Tu generosidad nos ayuda a seguir cuidando.
                        </p>
                    </div>
                </div>
            </Layout>
        );
    }

    return (
        <Layout currentPageName="Donar">
            <div className="max-w-4xl mx-auto px-4 py-8">

                <form onSubmit={handleSubmit} className="space-y-10">

                    {/* Section 1: Donation Amount */}
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                        <h2 className="text-xl font-bold text-[#2E7D32] mb-6 uppercase border-b border-gray-200 pb-2">Selecciona la cantidad a donar</h2>
                        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
                            <div className="md:col-span-3">
                                <label htmlFor="cantidad" className="font-bold text-gray-700 block">Cantidad*:</label>
                            </div>
                            <div className="md:col-span-9 flex items-center">
                                <div className="relative w-40">
                                    <input
                                        type="number"
                                        id="cantidad"
                                        placeholder="0"
                                        value={formData.cantidad}
                                        onChange={(e) => setFormData({ ...formData, cantidad: e.target.value })}
                                        className="border border-gray-300 p-2 w-full rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none pr-8 text-right font-bold text-lg"
                                        required
                                    />
                                    <span className="absolute right-3 top-1/2 -translate-y-1/2 font-bold text-gray-500">€</span>
                                </div>
                            </div>

                            <div className="md:col-span-12">
                                <div className="flex items-center gap-3 bg-gray-50 p-3 rounded">
                                    <input
                                        type="checkbox"
                                        id="enMemoria"
                                        checked={formData.enMemoria}
                                        onChange={(e) => setFormData({ ...formData, enMemoria: e.target.checked })}
                                        className="w-5 h-5 text-[#2E7D32] focus:ring-[#2E7D32] border-gray-300 rounded"
                                    />
                                    <label htmlFor="enMemoria" className="font-medium text-gray-700 cursor-pointer">¿Realizas esta donación en memoria de un familiar o amigo?</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Section 2: Personal Data */}
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                        <h2 className="text-xl font-bold text-[#2E7D32] mb-6 uppercase border-b border-gray-200 pb-2">Introduce tus datos</h2>

                        <div className="grid grid-cols-1 md:grid-cols-12 gap-y-4 gap-x-6">
                            {/* Nombre */}
                            <div className="md:col-span-3 md:text-right self-center">
                                <label htmlFor="nombre" className="font-bold text-gray-700">Nombre*:</label>
                            </div>
                            <div className="md:col-span-9">
                                <input
                                    type="text"
                                    id="nombre"
                                    value={formData.nombre}
                                    onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                                    className="border border-gray-300 p-2 w-full rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none"
                                    required
                                />
                            </div>

                            {/* Apellidos */}
                            <div className="md:col-span-3 md:text-right self-center">
                                <label htmlFor="apellidos" className="font-bold text-gray-700">Apellidos*:</label>
                            </div>
                            <div className="md:col-span-9">
                                <input
                                    type="text"
                                    id="apellidos"
                                    value={formData.apellidos}
                                    onChange={(e) => setFormData({ ...formData, apellidos: e.target.value })}
                                    className="border border-gray-300 p-2 w-full rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none"
                                    required
                                />
                            </div>

                            {/* Email */}
                            <div className="md:col-span-3 md:text-right self-center">
                                <label htmlFor="email" className="font-bold text-gray-700">Email*:</label>
                            </div>
                            <div className="md:col-span-9">
                                <input
                                    type="email"
                                    id="email"
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="border border-gray-300 p-2 w-full rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none"
                                    required
                                />
                            </div>

                            {/* Phone Info Text */}
                            <div className="md:col-span-3"></div>
                            <div className="md:col-span-9">
                                <p className="text-xs font-bold text-gray-500 mt-2 mb-1">Por favor indíquenos su número de teléfono y/o móvil.</p>
                            </div>

                            {/* Teléfono */}
                            <div className="md:col-span-3 md:text-right self-center">
                                <label htmlFor="telefono" className="font-bold text-gray-700">Teléfono:</label>
                            </div>
                            <div className="md:col-span-9">
                                <input
                                    type="tel"
                                    id="telefono"
                                    value={formData.telefono}
                                    onChange={(e) => setFormData({ ...formData, telefono: e.target.value })}
                                    className="border border-gray-300 p-2 w-full md:w-1/2 rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none"
                                />
                            </div>

                            {/* Móvil */}
                            <div className="md:col-span-3 md:text-right self-center">
                                <label htmlFor="movil" className="font-bold text-gray-700">Móvil:</label>
                            </div>
                            <div className="md:col-span-9">
                                <input
                                    type="tel"
                                    id="movil"
                                    value={formData.movil}
                                    onChange={(e) => setFormData({ ...formData, movil: e.target.value })}
                                    className="border border-gray-300 p-2 w-full md:w-1/2 rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none"
                                />
                            </div>

                            {/* Fecha Nacimiento */}
                            <div className="md:col-span-3 md:text-right self-center">
                                <label htmlFor="fechaNacimiento" className="font-bold text-gray-700">Fecha de nacimiento:</label>
                            </div>
                            <div className="md:col-span-9">
                                <input
                                    type="text"
                                    id="fechaNacimiento"
                                    placeholder="dd/mm/aaaa"
                                    value={formData.fechaNacimiento}
                                    onChange={(e) => setFormData({ ...formData, fechaNacimiento: e.target.value })}
                                    className="border border-gray-300 p-2 w-full md:w-1/2 rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none"
                                />
                            </div>

                            {/* Forma de conocernos */}
                            <div className="md:col-span-3 md:text-right self-center">
                                <label htmlFor="formaConocernos" className="font-bold text-gray-700">Forma de conocernos:</label>
                            </div>
                            <div className="md:col-span-9">
                                <div className="relative w-full md:w-1/2">
                                    <select
                                        id="formaConocernos"
                                        value={formData.formaConocernos}
                                        onChange={(e) => setFormData({ ...formData, formaConocernos: e.target.value })}
                                        className="border border-gray-300 p-2 w-full rounded appearance-none bg-white focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none"
                                    >
                                        <option value="">Seleccionar...</option>
                                        <option value="periodico">Periódico</option>
                                        <option value="web">Web</option>
                                        <option value="amigo">Amigo</option>
                                        <option value="redes">Redes Sociales</option>
                                    </select>
                                    <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                                        <svg className="w-4 h-4 fill-current text-gray-500" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" /></svg>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="mt-8 space-y-4 bg-gray-50 p-4 rounded border border-gray-100">
                            <div className="flex items-start gap-3">
                                <input
                                    type="checkbox"
                                    id="datosAdicionales"
                                    checked={formData.datosAdicionales}
                                    onChange={(e) => setFormData({ ...formData, datosAdicionales: e.target.checked })}
                                    className="mt-1 w-5 h-5 text-[#2E7D32] focus:ring-[#2E7D32] border-gray-300 rounded"
                                />
                                <label htmlFor="datosAdicionales" className="text-sm font-medium text-gray-700 cursor-pointer">Quiero dar datos adicionales a cudeca para que les sea más facil contactar conmigo.</label>
                            </div>

                            <div className="flex items-start gap-3">
                                <input
                                    type="checkbox"
                                    id="deduccionesFiscales"
                                    checked={formData.deduccionesFiscales}
                                    onChange={(e) => setFormData({ ...formData, deduccionesFiscales: e.target.checked })}
                                    className="mt-1 w-5 h-5 text-[#2E7D32] focus:ring-[#2E7D32] border-gray-300 rounded"
                                />
                                <label htmlFor="deduccionesFiscales" className="text-sm font-medium text-gray-700 leading-relaxed cursor-pointer">
                                    Quiero beneficiarme de las deducciones fiscales disponibles. La Fundación Cudeca está acogida al Régimen Fiscal especial de la Ley 49/2002, por tanto su donación tiene derecho a las máximas deducciones fiscales, que pueden llegar hasta un 80% desde Enero 2020 (más información). Para ello, es imprescindible marcar la opción anterior y completar los campos adicionales.
                                </label>
                            </div>
                        </div>
                    </div>

                    {/* Section 3: Additional Data (Green Box) */}
                    <div className={`transition-all duration-300 ${formData.deduccionesFiscales || formData.datosAdicionales ? 'opacity-100 max-h-[1000px]' : 'opacity-50 max-h-[1000px]'}`}>
                        <div className="bg-[#E8F5E9] p-6 rounded-lg border border-[#C8E6C9]">
                            <h3 className="text-lg font-bold text-[#2E7D32] mb-4 uppercase">Datos Adicionales</h3>
                            <div className="grid grid-cols-1 md:grid-cols-12 gap-y-4 gap-x-6">
                                <div className="md:col-span-3 md:text-right self-center">
                                    <label htmlFor="dni" className="font-bold text-gray-700">DNI/NIF:</label>
                                </div>
                                <div className="md:col-span-9">
                                    <input
                                        type="text"
                                        id="dni"
                                        value={formData.dni}
                                        onChange={(e) => setFormData({ ...formData, dni: e.target.value })}
                                        className="border border-gray-300 p-2 w-full md:w-1/2 rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none bg-white"
                                    />
                                </div>

                                <div className="md:col-span-3 md:text-right self-center">
                                    <label htmlFor="direccion" className="font-bold text-gray-700">Dirección:</label>
                                </div>
                                <div className="md:col-span-9">
                                    <input
                                        type="text"
                                        id="direccion"
                                        value={formData.direccion}
                                        onChange={(e) => setFormData({ ...formData, direccion: e.target.value })}
                                        className="border border-gray-300 p-2 w-full rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none bg-white"
                                    />
                                </div>

                                <div className="md:col-span-3 md:text-right self-center">
                                    <label htmlFor="codigoPostal" className="font-bold text-gray-700">Código Postal:</label>
                                </div>
                                <div className="md:col-span-9">
                                    <input
                                        type="text"
                                        id="codigoPostal"
                                        value={formData.codigoPostal}
                                        onChange={(e) => setFormData({ ...formData, codigoPostal: e.target.value })}
                                        className="border border-gray-300 p-2 w-full md:w-1/3 rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none bg-white"
                                    />
                                </div>

                                <div className="md:col-span-3 md:text-right self-center">
                                    <label htmlFor="poblacion" className="font-bold text-gray-700">Población:</label>
                                </div>
                                <div className="md:col-span-9">
                                    <input
                                        type="text"
                                        id="poblacion"
                                        value={formData.poblacion}
                                        onChange={(e) => setFormData({ ...formData, poblacion: e.target.value })}
                                        className="border border-gray-300 p-2 w-full md:w-1/2 rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none bg-white"
                                    />
                                </div>

                                <div className="md:col-span-3 md:text-right self-center">
                                    <label htmlFor="provincia" className="font-bold text-gray-700">Provincia:</label>
                                </div>
                                <div className="md:col-span-9">
                                    <input
                                        type="text"
                                        id="provincia"
                                        value={formData.provincia}
                                        onChange={(e) => setFormData({ ...formData, provincia: e.target.value })}
                                        className="border border-gray-300 p-2 w-full md:w-1/2 rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none bg-white"
                                    />
                                </div>

                                <div className="md:col-span-3 md:text-right self-center">
                                    <label htmlFor="pais" className="font-bold text-gray-700">País:</label>
                                </div>
                                <div className="md:col-span-9">
                                    <input
                                        type="text"
                                        id="pais"
                                        value={formData.pais}
                                        onChange={(e) => setFormData({ ...formData, pais: e.target.value })}
                                        className="border border-gray-300 p-2 w-full md:w-1/2 rounded focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none bg-white"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Section 4: Payment Method */}
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                        <h2 className="text-xl font-bold text-[#2E7D32] mb-6 uppercase border-b border-gray-200 pb-2">Método de pago</h2>
                        <div className="flex flex-col md:flex-row md:items-center gap-4">
                            <label htmlFor="metodoPago" className="font-bold text-gray-700">Seleccione método*:</label>
                            <div className="relative flex-grow max-w-md">
                                <select
                                    id="metodoPago"
                                    value={formData.metodoPago}
                                    onChange={(e) => setFormData({ ...formData, metodoPago: e.target.value })}
                                    className="border border-gray-300 p-3 w-full rounded appearance-none bg-white focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent outline-none font-medium"
                                >
                                    <option>Tarjeta de crédito/débito</option>
                                    <option>PayPal</option>
                                    <option>Bizum</option>
                                </select>
                                <div className="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none">
                                    <CreditCard className="w-5 h-5 text-gray-400" />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-4 bg-gray-50 p-6 rounded-lg border border-gray-100">
                        <div className="flex items-start gap-3">
                            <input
                                type="checkbox"
                                id="aceptoPolitica"
                                checked={formData.aceptoPolitica}
                                onChange={(e) => setFormData({ ...formData, aceptoPolitica: e.target.checked })}
                                className="mt-1 w-5 h-5 text-[#2E7D32] focus:ring-[#2E7D32] border-gray-300 rounded"
                                required
                            />
                            <label htmlFor="aceptoPolitica" className="text-sm text-gray-700">
                                Acepto la <a href="#" className="text-[#2E7D32] font-bold hover:underline">Política de Privacidad</a> y el <a href="#" className="text-[#2E7D32] font-bold hover:underline">Aviso Legal</a>.
                            </label>
                        </div>

                        <div className="flex items-start gap-3">
                            <input
                                type="checkbox"
                                id="recibirInformacion"
                                checked={formData.recibirInformacion}
                                onChange={(e) => setFormData({ ...formData, recibirInformacion: e.target.checked })}
                                className="mt-1 w-5 h-5 text-[#2E7D32] focus:ring-[#2E7D32] border-gray-300 rounded"
                            />
                            <label htmlFor="recibirInformacion" className="text-sm text-gray-700">
                                Quiero recibir información sobre la forma especial de cuidar de la Fundación Cudeca y las diferentes actividades que realiza.
                            </label>
                        </div>
                    </div>

                    <div className="flex justify-center pt-4 pb-8">
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="bg-[#2E7D32] hover:bg-[#1B5E20] text-white font-bold text-lg px-12 py-4 rounded-full shadow-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                        >
                            {isSubmitting && <Loader2 className="animate-spin w-5 h-5" />}
                            {isSubmitting ? 'Procesando...' : 'Realizar Donación'}
                        </button>
                    </div>

                </form>
            </div>
        </Layout>
    );
}
