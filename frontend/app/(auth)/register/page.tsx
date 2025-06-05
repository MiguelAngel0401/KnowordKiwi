"use client";

import { useRef, useState } from "react";
import {
  Button,
  Field,
  Fieldset,
  Input,
  Label,
  Legend,
  Textarea,
  Transition,
} from "@headlessui/react";

export default function RegisterPage() {
  const [step, setStep] = useState(1);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    username: "",
    realName: "",
    avatar: "",
    bio: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const nextStep = () => setStep((prev) => prev + 1);
  const prevStep = () => setStep((prev) => prev - 1);

  const handleSubmit = () => {
    console.log("Datos del formulario:", formData);
  };

  return (
    <Fieldset className="max-w-lg mx-auto space-y-8 rounded-lg shadow-lg p-8 bg-gray-900">
      <Legend className="text-3xl font-bold mb-6 text-center">
        {step === 1 && "¡Bienvenido! Empecemos creando tu cuenta"}
        {step === 2 && "¿Cómo te gustaría que te conozcan?"}
        {step === 3 && "Haz que tu perfil cuente"}
      </Legend>

      {/* Paso 1 */}
      <Transition
        show={step === 1}
        enter="transition-opacity duration-400"
        enterFrom="opacity-0"
        enterTo="opacity-100"
        leave="transition-opacity duration-400"
        leaveFrom="opacity-100"
        leaveTo="opacity-0"
      >
        <div className="space-y-4">
          <h3 className="font-light text-center mb-8 text-gray-300">
            Solo necesitamos tu correo y una contraseña segura.
          </h3>
          <Field>
            <Label htmlFor="email" className="block text-sm font-medium">
              Correo electrónico
            </Label>
            <Input
              type="email"
              name="email"
              id="email"
              autoComplete="email"
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm transition duration-150 ease-in-out"
              value={formData.email}
              onChange={handleChange}
            />
          </Field>
          <Field>
            <Label htmlFor="password" className="block text-sm font-medium">
              Contraseña
            </Label>
            <Input
              type="password"
              name="password"
              id="password"
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm transition duration-150 ease-in-out"
              value={formData.password}
              onChange={handleChange}
            />
          </Field>
          <div className="flex justify-end pt-4">
            <button
              className="bg-primary text-white px-4 py-2 rounded hover:bg-primary-hover disabled:opacity-50"
              onClick={nextStep}
              disabled={!formData.email || !formData.password}
            >
              Continuar
            </button>
          </div>
        </div>
      </Transition>

      {/* Paso 2 */}
      <Transition show={step === 2}>
        <div className="space-y-4">
          <h3 className="font-light text-center mb-8 text-gray-300">
            Tu nombre de usuario será visible para otros. El nombre real es
            opcional, pero puede ayudar a conectar mejor.
          </h3>
          <Field>
            <Label htmlFor="username" className="block text-sm font-medium">
              Nombre de usuario
            </Label>
            <Input
              type="text"
              name="username"
              id="username"
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm transition duration-150 ease-in-out"
              value={formData.username}
              onChange={handleChange}
            />
          </Field>
          <Field>
            <Label htmlFor="realName" className="block text-sm font-medium">
              Nombre real (opcional)
            </Label>
            <Input
              type="text"
              name="realName"
              id="realName"
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm transition duration-150 ease-in-out"
              value={formData.realName}
              onChange={handleChange}
            />
          </Field>
          <div className="flex justify-between pt-4">
            <button
              className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
              onClick={prevStep}
            >
              Atrás
            </button>
            <button
              className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-hover disabled:opacity-50"
              onClick={nextStep}
              disabled={!formData.username}
            >
              Siguiente
            </button>
          </div>
        </div>
      </Transition>

      {/* Paso 3 */}
      <Transition show={step === 3}>
        <div className="space-y-4">
          <h3 className="font-light text-center mb-8 text-gray-300">
            Agrega una imagen y una pequeña descripción para mostrar tu
            personalidad desde el primer día.
          </h3>
          <Field>
            <Label htmlFor="avatar" className="block text-sm font-medium">
              Imagen de perfil (Opcional)
            </Label>

            <input
              type="file"
              name="avatar"
              id="avatar"
              accept="image/*"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) {
                  const reader = new FileReader();
                  reader.onloadend = () => {
                    setFormData((prev) => ({
                      ...prev,
                      avatar: reader.result as string,
                    }));
                  };
                  reader.readAsDataURL(file);
                }
              }}
              ref={fileInputRef}
            />

            <Button
              type="button"
              className="px-4 py-2 mt-4 bg-accent text-white rounded hover:bg-accent-hover transition duration-150 ease-in-out"
              onClick={() => {
                fileInputRef.current?.click();
              }}
            >
              {formData.avatar ? "Cambiar foto" : "Subir foto"}
            </Button>
            {formData.avatar && (
              <div className="w-full flex justify-center">
                <img
                  src={formData.avatar}
                  alt="Avatar preview"
                  className="mt-2 w-16 h-16 rounded-full object-cover inline-block "
                />
              </div>
            )}
          </Field>
          <Field>
            <Label htmlFor="bio" className="block text-sm font-medium">
              Descripción
            </Label>
            <Textarea
              name="bio"
              id="bio"
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm transition duration-150 ease-in-out"
              rows={3}
              value={formData.bio}
              onChange={handleChange}
            />
          </Field>
          <div className="flex justify-between pt-4">
            <button
              className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
              onClick={prevStep}
            >
              Atrás
            </button>
            <button
              className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-hover"
              onClick={handleSubmit}
            >
              Finalizar registro
            </button>
          </div>
        </div>
      </Transition>

      {/* Indicador de progreso */}
      <div className="mt-6 text-center text-sm text-gray-500">
        Paso {step} de 3
      </div>
    </Fieldset>
  );
}
