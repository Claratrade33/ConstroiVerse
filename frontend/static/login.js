async function logar() {
  const email = document.getElementById('email').value;
  const senha = document.getElementById('senha').value;

  const res = await fetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, senha })
  });

  const data = await res.json();

  if (!res.ok) {
    document.getElementById('erro').innerText = data.msg || 'Erro no login';
    return;
  }

  // Salva no localStorage
  localStorage.setItem('jwt', data.token);
  localStorage.setItem('perfil', data.perfil);
  localStorage.setItem('usuario_id', data.id); // Se enviar o ID
  if (data.perfil === 'cliente') localStorage.setItem('cliente_id', data.id);

  // Redireciona pro painel genérico (dashboard.js faz o redirecionamento real)
  window.location.href = "/painel.html";
}