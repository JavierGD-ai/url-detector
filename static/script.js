const consejos = [
    "Nunca hagas clic en enlaces sospechosos o no solicitados.",
    "Verifica que la URL comience con 'https://' antes de ingresar datos personales.",
    "Evita descargar archivos de sitios desconocidos o no confiables.",
    "Actualiza tu navegador y antivirus regularmente.",
    "Desconfía de ofertas demasiado buenas para ser verdad.",
    "Activa la verificación en dos pasos en tus cuentas importantes.",
    "No compartas tus contraseñas por correo o mensajes.",
    "Utiliza un administrador de contraseñas para tener claves fuertes.",
    "Revisa siempre el remitente de los correos electrónicos.",
    "Desconfía de los sitios que te piden información confidencial sin justificación."
];

function mostrarConsejoAleatorio() {
    const consejo = consejos[Math.floor(Math.random() * consejos.length)];
    alert("💡 Consejo de Seguridad:\n\n" + consejo);
}
