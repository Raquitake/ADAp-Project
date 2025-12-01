import React, { useState } from 'react';
import { Loader2, CheckCircle } from 'lucide-react';
import Layout from '../components/Layout';

export default function Socios() {
    const [tipoPersona, setTipoPersona] = useState('persona');
    const [periodicidad, setPeriodicidad] = useState('mensual');
    const [cantidad, setCantidad] = useState(25);
    const [customAmount, setCustomAmount] = useState('');
    const [showFiscalData, setShowFiscalData] = useState(false);
    const [showExtraData, setShowExtraData] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitted, setSubmitted] = useState(false);

    const [formData, setFormData] = useState({
        empresa: '',
        nombre: '',
        apellidos: '',
        email: '',
        telefono: '',
        movil: '',
        fechaNacimiento: '',
        formaConocernos: '',
        dni: '',
        direccion: '',
        codigoPostal: '',
        poblacion: '',
        provincia: '',
        pais: '',
        metodoPago: 'tarjeta',
        aceptaPrivacidad: false,
        recibirInfo: false,
    });

    const amountOptions = [
        { value: 15, image: 'https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=200&h=150&fit=crop', label: 'Un mes en la Unidad de Día y Rehabilitación', subLabel: '125€ por paciente' },
        { value: 25, image: 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=200&h=150&fit=crop', label: 'Un mes en el Programa de Atención Domiciliaria', subLabel: '1.000€ por paciente' },
        { value: 40, image: 'https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=200&h=150&fit=crop', label: 'Una semana en la Unidad de Ingresos', subLabel: '2.100€ por paciente' },
    ];

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        // Simulate submission
        await new Promise(resolve => setTimeout(resolve, 1500));

        setIsSubmitting(false);
        setSubmitted(true);
    };

    if (submitted) {
        return (
            <Layout currentPageName="Socios">
                <div className="min-h-[60vh] flex items-center justify-center px-4">
                    <div className="text-center max-w-md">
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                            <CheckCircle className="w-10 h-10 text-[#2E7D32]" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">¡Gracias por hacerte socio!</h2>
                        <p className="text-gray-600 mb-6">
                            Hemos recibido tu solicitud. Te contactaremos pronto para completar el proceso.
                        </p>
                        <p className="text-[#2E7D32] font-semibold">Tu apoyo hace la diferencia.</p>
                    </div>
                </div>
            </Layout>
        );
    }

    return (
        <Layout currentPageName="Socios">
            <div>
                {/* Header */}
                <section className="bg-[#2E7D32] py-6">
                    <div className="max-w-4xl mx-auto px-4">
                        <h1 className="text-2xl md:text-3xl font-bold text-white">Hazte socio</h1>
                    </div>
                </section>

                <div className="max-w-4xl mx-auto px-4 py-8">
                    <form onSubmit={handleSubmit} className="space-y-8">

                        {/* Periodicidad */}
                        <div className="border-t-4 border-[#2E7D32] pt-6">
                            <h2 className="text-lg font-semibold text-gray-900 mb-4">¿Con qué periodicidad desea colaborar? *</h2>
                            <div className="flex flex-wrap gap-4">
                                {['mensual', 'bimensual', 'trimestral', 'semestral', 'anual'].map((p) => (
                                    <label key={p} className="flex items-center gap-2 cursor-pointer">
                                        <input
                                            type="radio"
                                            name="periodicidad"
                                            value={p}
                                            checked={periodicidad === p}
                                            onChange={(e) => setPeriodicidad(e.target.value)}
                                            className="w-4 h-4 text-[#2E7D32] border-gray-300 focus:ring-[#2E7D32]"
                                        />
                                        <span className="capitalize">{p}</span>
                                    </label>
                                ))}
                            </div>
                        </div>

                        {/* Cantidad */}
                        <div className="border-t-4 border-[#2E7D32] pt-6">
                            <h2 className="text-lg font-semibold text-gray-900 mb-4">¿Cuánto quieres aportar? *</h2>

                            <div className="grid md:grid-cols-3 gap-4 mb-4">
                                {amountOptions.map((option) => (
                                    <button
                                        key={option.value}
                                        type="button"
                                        onClick={() => { setCantidad(option.value); setCustomAmount(''); }}
                                        className={`relative rounded-lg overflow-hidden border-2 transition-all ${cantidad === option.value && !customAmount
                                                ? 'border-[#2E7D32] ring-2 ring-[#2E7D32]/30'
                                                : 'border-gray-200 hover:border-gray-300'
                                            }`}
                                    >
                                        <img src={option.image} alt="" className="w-full h-32 object-cover" />
                                        <div className="absolute inset-0 bg-black/40 flex flex-col justify-end p-3">
                                            <p className="text-white text-xs text-left">{option.label}</p>
                                            <p className="text-yellow-400 text-xs text-right font-semibold">{option.subLabel}</p>
                                        </div>
                                        <div className={`py-2 text-center font-bold text-lg ${cantidad === option.value && !customAmount
                                                ? 'bg-[#2E7D32] text-white'
                                                : 'bg-gray-100 text-gray-700'
                                            }`}>
                                            {option.value}€
                                        </div>
                                    </button>
                                ))}
                            </div>

                            <button
                                type="button"
                                onClick={() => setCantidad(0)}
                                className={`w-full py-3 rounded-full font-semibold transition-all ${customAmount
                                        ? 'bg-[#2E7D32] text-white'
                                        : 'bg-yellow-500 hover:bg-yellow-400 text-[#1B5E20]'
                                    }`}
                            >
                                Otra cantidad
                            </button>

                            {(cantidad === 0 || customAmount) && (
                                <div className="mt-4">
                                    <input
                                        type="number"
                                        min="1"
                                        placeholder="Introduce la cantidad en €"
                                        value={customAmount}
                                        onChange={(e) => setCustomAmount(e.target.value)}
                                        className="w-full text-center text-lg border rounded px-3 py-2"
                                    />
                                </div>
                            )}
                        </div>

                        {/* Tipo Persona */}
                        <div className="flex gap-2">
                            <button
                                type="button"
                                onClick={() => setTipoPersona('persona')}
                                className={`px-6 py-2 rounded-full font-semibold transition-all ${tipoPersona === 'persona'
                                        ? 'bg-[#2E7D32] text-white'
                                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                Persona
                            </button>
                            <button
                                type="button"
                                onClick={() => setTipoPersona('empresa')}
                                className={`px-6 py-2 rounded-full font-semibold transition-all ${tipoPersona === 'empresa'
                                        ? 'bg-[#2E7D32] text-white'
                                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                Empresa
                            </button>
                        </div>

                        {/* Datos personales */}
                        <div className="bg-gray-50 rounded-lg p-6 space-y-4">
                            <h3 className="font-semibold text-gray-900 uppercase">Introduce tus datos</h3>

                            {tipoPersona === 'empresa' && (
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Empresa*:</label>
                                    <input
                                        value={formData.empresa}
                                        onChange={(e) => setFormData({ ...formData, empresa: e.target.value })}
                                        className="mt-1 w-full border rounded px-3 py-2"
                                        required={tipoPersona === 'empresa'}
                                    />
                                </div>
                            )}

                            <div className="grid md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Nombre*:</label>
                                    <input
                                        value={formData.nombre}
                                        onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                                        className="mt-1 w-full border rounded px-3 py-2"
                                        required
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Apellidos*:</label>
                                    <input
                                        value={formData.apellidos}
                                        onChange={(e) => setFormData({ ...formData, apellidos: e.target.value })}
                                        className="mt-1 w-full border rounded px-3 py-2"
                                        required
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700">Email*:</label>
                                <input
                                    type="email"
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="mt-1 w-full border rounded px-3 py-2"
                                    required
                                />
                            </div>

                            <p className="text-sm text-gray-600">Por favor indíquenos su número de teléfono y/o móvil.</p>

                            <div className="grid md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Teléfono:</label>
                                    <input
                                        value={formData.telefono}
                                        onChange={(e) => setFormData({ ...formData, telefono: e.target.value })}
                                        className="mt-1 w-full border rounded px-3 py-2"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Móvil*:</label>
                                    <input
                                        value={formData.movil}
                                        onChange={(e) => setFormData({ ...formData, movil: e.target.value })}
                                        className="mt-1 w-full border rounded px-3 py-2"
                                        required
                                    />
                                </div>
                            </div>

                            <div className="grid md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Fecha de nacimiento:</label>
                                    <input
                                        type="date"
                                        value={formData.fechaNacimiento}
                                        onChange={(e) => setFormData({ ...formData, fechaNacimiento: e.target.value })}
                                        className="mt-1 w-full border rounded px-3 py-2"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Forma de conocernos:</label>
                                    <select
                                        value={formData.formaConocernos}
                                        onChange={(e) => setFormData({ ...formData, formaConocernos: e.target.value })}
                                        className="mt-1 w-full border rounded px-3 py-2"
                                    >
                                        <option value="" disabled>Seleccionar...</option>
                                        <option value="periodico">Periódico</option>
                                        <option value="internet">Internet</option>
                                        <option value="amigos">Amigos/Familia</option>
                                        <option value="evento">Evento</option>
                                        <option value="otro">Otro</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        {/* Checkboxes */}
                        <div className="space-y-4">
                            <div className="flex items-start gap-2">
                                <input
                                    type="checkbox"
                                    id="extraData"
                                    checked={showExtraData}
                                    onChange={(e) => setShowExtraData(e.target.checked)}
                                    className="mt-1 w-4 h-4 text-[#2E7D32] border-gray-300 rounded focus:ring-[#2E7D32]"
                                />
                                <label htmlFor="extraData" className="text-sm text-gray-700 cursor-pointer">
                                    Quiero dar datos adicionales a cudeca para que les sea más fácil contactar conmigo.
                                </label>
                            </div>

                            <div className="flex items-start gap-2">
                                <input
                                    type="checkbox"
                                    id="fiscalData"
                                    checked={showFiscalData}
                                    onChange={(e) => setShowFiscalData(e.target.checked)}
                                    className="mt-1 w-4 h-4 text-[#2E7D32] border-gray-300 rounded focus:ring-[#2E7D32]"
                                />
                                <label htmlFor="fiscalData" className="text-sm text-gray-700 cursor-pointer">
                                    Quiero beneficiarme de las deducciones fiscales disponibles. La Fundación Cudeca está acogida al Régimen Fiscal especial de la Ley 49/2002, por tanto su donación tiene derecho a las máximas deducciones fiscales, que pueden llegar hasta un 80% desde Enero 2020 (
                                    <a href="#" className="text-[#2E7D32] underline">más información</a>
                                    ). Para ello, es imprescindible marcar la opción anterior y completar los campos adicionales.
                                </label>
                            </div>
                        </div>

                        {/* Fiscal Data */}
                        {showFiscalData && (
                            <div className="bg-green-50 border border-[#2E7D32]/30 rounded-lg p-6 space-y-4">
                                <div className="grid md:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">{tipoPersona === 'empresa' ? 'CIF:' : 'DNI/NIF:'}</label>
                                        <input
                                            value={formData.dni}
                                            onChange={(e) => setFormData({ ...formData, dni: e.target.value })}
                                            className="mt-1 w-full border rounded px-3 py-2 bg-white"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Dirección:</label>
                                        <input
                                            value={formData.direccion}
                                            onChange={(e) => setFormData({ ...formData, direccion: e.target.value })}
                                            className="mt-1 w-full border rounded px-3 py-2 bg-white"
                                        />
                                    </div>
                                </div>
                                <div className="grid md:grid-cols-3 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Código Postal:</label>
                                        <input
                                            value={formData.codigoPostal}
                                            onChange={(e) => setFormData({ ...formData, codigoPostal: e.target.value })}
                                            className="mt-1 w-full border rounded px-3 py-2 bg-white"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Población:</label>
                                        <input
                                            value={formData.poblacion}
                                            onChange={(e) => setFormData({ ...formData, poblacion: e.target.value })}
                                            className="mt-1 w-full border rounded px-3 py-2 bg-white"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Provincia:</label>
                                        <input
                                            value={formData.provincia}
                                            onChange={(e) => setFormData({ ...formData, provincia: e.target.value })}
                                            className="mt-1 w-full border rounded px-3 py-2 bg-white"
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">País:</label>
                                    <input
                                        value={formData.pais}
                                        onChange={(e) => setFormData({ ...formData, pais: e.target.value })}
                                        className="mt-1 w-full border rounded px-3 py-2 bg-white"
                                    />
                                </div>
                            </div>
                        )}

                        {/* Payment Method */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Método de pago*:</label>
                            <select
                                value={formData.metodoPago}
                                onChange={(e) => setFormData({ ...formData, metodoPago: e.target.value })}
                                className="mt-1 w-full border rounded px-3 py-2"
                            >
                                <option value="tarjeta">Tarjeta de crédito/débito</option>
                                <option value="domiciliacion">Domiciliación bancaria</option>
                            </select>
                        </div>

                        {/* Final Checkboxes */}
                        <div className="space-y-4">
                            <div className="flex items-start gap-2">
                                <input
                                    type="checkbox"
                                    id="privacidad"
                                    checked={formData.aceptaPrivacidad}
                                    onChange={(e) => setFormData({ ...formData, aceptaPrivacidad: e.target.checked })}
                                    className="mt-1 w-4 h-4 text-[#2E7D32] border-gray-300 rounded focus:ring-[#2E7D32]"
                                    required
                                />
                                <label htmlFor="privacidad" className="text-sm text-gray-700 cursor-pointer">
                                    Acepto la <a href="#" className="text-[#2E7D32] underline">Política de Privacidad</a> y el <a href="#" className="text-[#2E7D32] underline">Aviso Legal</a>.
                                </label>
                            </div>

                            <div className="flex items-start gap-2">
                                <input
                                    type="checkbox"
                                    id="recibirInfo"
                                    checked={formData.recibirInfo}
                                    onChange={(e) => setFormData({ ...formData, recibirInfo: e.target.checked })}
                                    className="mt-1 w-4 h-4 text-[#2E7D32] border-gray-300 rounded focus:ring-[#2E7D32]"
                                />
                                <label htmlFor="recibirInfo" className="text-sm text-gray-700 cursor-pointer">
                                    Quiero recibir información sobre la forma especial de cuidar de la Fundación Cudeca y las diferentes actividades que realiza.
                                </label>
                            </div>
                        </div>

                        {/* Submit */}
                        <div className="text-center pt-4">
                            <button
                                type="submit"
                                disabled={isSubmitting || !formData.aceptaPrivacidad}
                                className="bg-[#2E7D32] hover:bg-[#1B5E20] text-white font-bold px-12 py-6 rounded-full text-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center mx-auto"
                            >
                                {isSubmitting && <Loader2 className="w-5 h-5 animate-spin mr-2" />}
                                Hacerme socio
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </Layout>
    );
}
