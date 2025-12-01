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

                <form onSubmit={handleSubmit} className="space-y-8">

                    {/* Section 1: Donation Amount */}
                    <div>
                        <h2 className="text-lg font-bold text-gray-900 mb-4 uppercase">SELECCIONA LA CANTIDAD A DONAR</h2>
                        <div className="flex items-center gap-4 mb-4">
                            <label htmlFor="cantidad" className="font-bold text-gray-900 w-24">Cantidad*:</label>
                            <div className="flex items-center">
                                <input
                                    type="number"
                                    id="cantidad"
                                    placeholder="Cantidad"
                                    value={formData.cantidad}
                                    onChange={(e) => setFormData({ ...formData, cantidad: e.target.value })}
                                    className="border border-gray-400 p-2 w-40"
                                    required
                                />
                                <span className="ml-2 font-bold">€</span>
                            </div>
                        </div>

                        <div className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                id="enMemoria"
                                checked={formData.enMemoria}
                                onChange={(e) => setFormData({ ...formData, enMemoria: e.target.checked })}
                                className="w-4 h-4 border-gray-400"
                            />
                            <label htmlFor="enMemoria" className="font-bold text-gray-900">¿Realizas esta donación en memoria de un familiar o amigo?</label>
                        </div>
                    </div>

                    {/* Section 2: Personal Data */}
                    <div>
                        <h2 className="text-lg font-bold text-gray-900 mb-6 uppercase">INTRODUCE TUS DATOS</h2>

                        <div className="space-y-4 max-w-2xl">
                            <div className="flex items-center gap-4">
                                <label htmlFor="nombre" className="font-bold text-gray-900 w-32 text-right">Nombre*:</label>
                                <input
                                    type="text"
                                    id="nombre"
                                    placeholder="Nombre"
                                    value={formData.nombre}
                                    onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                                    className="border border-gray-400 p-2 flex-grow"
                                    required
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="apellidos" className="font-bold text-gray-900 w-32 text-right">Apellidos*:</label>
                                <input
                                    type="text"
                                    id="apellidos"
                                    placeholder="Apellidos"
                                    value={formData.apellidos}
                                    onChange={(e) => setFormData({ ...formData, apellidos: e.target.value })}
                                    className="border border-gray-400 p-2 flex-grow"
                                    required
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="email" className="font-bold text-gray-900 w-32 text-right">Email*:</label>
                                <input
                                    type="email"
                                    id="email"
                                    placeholder="Email"
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="border border-gray-400 p-2 flex-grow"
                                    required
                                />
                            </div>

                            <p className="text-xs font-bold mt-4 ml-36">Por favor indíquenos su número de teléfono y/o móvil.</p>

                            <div className="flex items-center gap-4">
                                <label htmlFor="telefono" className="font-bold text-gray-900 w-32 text-right">Teléfono:</label>
                                <input
                                    type="tel"
                                    id="telefono"
                                    placeholder="Teléfono"
                                    value={formData.telefono}
                                    onChange={(e) => setFormData({ ...formData, telefono: e.target.value })}
                                    className="border border-gray-400 p-2 w-48"
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="movil" className="font-bold text-gray-900 w-32 text-right">Móvil:</label>
                                <input
                                    type="tel"
                                    id="movil"
                                    placeholder="Móvil"
                                    value={formData.movil}
                                    onChange={(e) => setFormData({ ...formData, movil: e.target.value })}
                                    className="border border-gray-400 p-2 w-48"
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="fechaNacimiento" className="font-bold text-gray-900 w-32 text-right">Fecha de nacimiento:</label>
                                <input
                                    type="text"
                                    id="fechaNacimiento"
                                    placeholder="dd/mm/aaaa"
                                    value={formData.fechaNacimiento}
                                    onChange={(e) => setFormData({ ...formData, fechaNacimiento: e.target.value })}
                                    className="border border-gray-400 p-2 w-48"
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="formaConocernos" className="font-bold text-gray-900 w-32 text-right">Forma de conocernos:</label>
                                <div className="relative w-48">
                                    <select
                                        id="formaConocernos"
                                        value={formData.formaConocernos}
                                        onChange={(e) => setFormData({ ...formData, formaConocernos: e.target.value })}
                                        className="border border-gray-400 p-2 w-full appearance-none bg-white"
                                    >
                                        <option value="">Periódico</option>
                                        <option value="web">Web</option>
                                        <option value="amigo">Amigo</option>
                                    </select>
                                    <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                                        <svg className="w-4 h-4 fill-current text-gray-500" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" /></svg>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="mt-6 space-y-4">
                            <div className="flex items-start gap-2">
                                <input
                                    type="checkbox"
                                    id="datosAdicionales"
                                    checked={formData.datosAdicionales}
                                    onChange={(e) => setFormData({ ...formData, datosAdicionales: e.target.checked })}
                                    className="mt-1 w-4 h-4 border-gray-400"
                                />
                                <label htmlFor="datosAdicionales" className="text-xs font-bold text-gray-900">Quiero dar datos adicionales a cudeca para que les sea más facil contactar conmigo.</label>
                            </div>

                            <div className="flex items-start gap-2">
                                <input
                                    type="checkbox"
                                    id="deduccionesFiscales"
                                    checked={formData.deduccionesFiscales}
                                    onChange={(e) => setFormData({ ...formData, deduccionesFiscales: e.target.checked })}
                                    className="mt-1 w-4 h-4 border-gray-400"
                                />
                                <label htmlFor="deduccionesFiscales" className="text-xs font-bold text-gray-900 leading-tight">
                                    Quiero beneficiarme de las deducciones fiscales disponibles. La Fundación Cudeca está acogida al Régimen Fiscal especial de la Ley 49/2002, por tanto su donación tiene derecho a las máximas deducciones fiscales, que pueden llegar hasta un 80% desde Enero 2020 (más información). Para ello, es imprescindible marcar la opción anterior y completar los campos adicionales.
                                </label>
                            </div>
                        </div>
                    </div>

                    {/* Section 3: Additional Data (Green Box) */}
                    <div className="bg-[#98D898] p-6 max-w-2xl">
                        <div className="space-y-4">
                            <div className="flex items-center gap-4">
                                <label htmlFor="dni" className="font-bold text-gray-900 w-32 text-right">DNI/NIF:</label>
                                <input
                                    type="text"
                                    id="dni"
                                    placeholder="Número de identif..."
                                    value={formData.dni}
                                    onChange={(e) => setFormData({ ...formData, dni: e.target.value })}
                                    className="border border-gray-400 p-2 w-48"
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="direccion" className="font-bold text-gray-900 w-32 text-right">Dirección:</label>
                                <input
                                    type="text"
                                    id="direccion"
                                    placeholder="Móvil" // Placeholder in image says "Móvil" for Address? Probably a copy paste error in mockup, but I'll stick to "Dirección" or empty
                                    value={formData.direccion}
                                    onChange={(e) => setFormData({ ...formData, direccion: e.target.value })}
                                    className="border border-gray-400 p-2 w-48"
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="codigoPostal" className="font-bold text-gray-900 w-32 text-right">Código Postal:</label>
                                <input
                                    type="text"
                                    id="codigoPostal"
                                    placeholder="Código postal"
                                    value={formData.codigoPostal}
                                    onChange={(e) => setFormData({ ...formData, codigoPostal: e.target.value })}
                                    className="border border-gray-400 p-2 w-48"
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="poblacion" className="font-bold text-gray-900 w-32 text-right">Población:</label>
                                <input
                                    type="text"
                                    id="poblacion"
                                    placeholder="Población"
                                    value={formData.poblacion}
                                    onChange={(e) => setFormData({ ...formData, poblacion: e.target.value })}
                                    className="border border-gray-400 p-2 w-48"
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="provincia" className="font-bold text-gray-900 w-32 text-right">Provincia:</label>
                                <input
                                    type="text"
                                    id="provincia"
                                    placeholder="Provincia"
                                    value={formData.provincia}
                                    onChange={(e) => setFormData({ ...formData, provincia: e.target.value })}
                                    className="border border-gray-400 p-2 w-48"
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <label htmlFor="pais" className="font-bold text-gray-900 w-32 text-right">País:</label>
                                <input
                                    type="text"
                                    id="pais"
                                    placeholder="País"
                                    value={formData.pais}
                                    onChange={(e) => setFormData({ ...formData, pais: e.target.value })}
                                    className="border border-gray-400 p-2 w-48"
                                />
                            </div>
                        </div>
                    </div>

                    {/* Section 4: Payment Method */}
                    <div className="flex items-center gap-4">
                        <label htmlFor="metodoPago" className="font-bold text-gray-900 text-lg">Método de pago*:</label>
                        <div className="relative">
                            <select
                                id="metodoPago"
                                value={formData.metodoPago}
                                onChange={(e) => setFormData({ ...formData, metodoPago: e.target.value })}
                                className="border border-gray-400 p-2 pr-8 appearance-none bg-white min-w-[200px]"
                            >
                                <option>Tarjeta de crédito/débito</option>
                                <option>PayPal</option>
                                <option>Bizum</option>
                            </select>
                            <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                                <svg className="w-4 h-4 fill-current text-gray-500" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" /></svg>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-2">
                        <div className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                id="aceptoPolitica"
                                checked={formData.aceptoPolitica}
                                onChange={(e) => setFormData({ ...formData, aceptoPolitica: e.target.checked })}
                                className="w-4 h-4 border-gray-400"
                                required
                            />
                            <label htmlFor="aceptoPolitica" className="text-xs font-bold text-gray-900">
                                Acepto la <a href="#" className="text-[#2E7D32]">Política de Privacidad</a> y el <a href="#" className="text-[#2E7D32]">Aviso Legal</a>.
                            </label>
                        </div>

                        <div className="flex items-start gap-2">
                            <input
                                type="checkbox"
                                id="recibirInformacion"
                                checked={formData.recibirInformacion}
                                onChange={(e) => setFormData({ ...formData, recibirInformacion: e.target.checked })}
                                className="mt-1 w-4 h-4 border-gray-400"
                            />
                            <label htmlFor="recibirInformacion" className="text-xs font-bold text-gray-900">
                                Quiero recibir información sobre la forma especial de cuidar de la Fundación Cudeca y las diferentes actividades que realiza.
                            </label>
                        </div>
                    </div>

                    <div className="flex justify-center pt-8">
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="bg-[#98D898] hover:bg-[#7bc07b] text-[#2E7D32] font-bold text-xl px-12 py-3 rounded-full shadow-md transition-colors"
                        >
                            {isSubmitting ? 'Enviando...' : 'Hacer donación'}
                        </button>
                    </div>

                </form>
            </div>
        </Layout>
    );
}
