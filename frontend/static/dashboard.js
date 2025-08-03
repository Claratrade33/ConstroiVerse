document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem('jwt');
  const perfil = localStorage.getItem('perfil');
  const usuarioId = localStorage.getItem('usuario_id');
  const clienteId = localStorage.getItem('cliente_id');
  const obraId = localStorage.getItem('obra_id');

  // Verifica login
  if (!token || !perfil || !usuarioId) {
    window.location.href = "/login.html";
    return;
  }

  // Redireciona para o painel correto
  const paginaAtual = window.location.pathname;
  if (paginaAtual === '/painel.html') {
    window.location.href = `/painel/painel_${perfil}.html`;
    return;
  }

  // Carrega funções por perfil
  if (perfil === 'cliente') {
    carregarOrcamentos(clienteId || usuarioId);
  }

  if (['pedreiro', 'engenheiro', 'eletricista', 'encanador'].includes(perfil)) {
    carregarTarefas(usuarioId);
  }

  if (perfil === 'engenheiro') {
    carregarObra(obraId || '1');
  }
});

// 🔹 Cliente: Histórico de orçamentos
async function carregarOrcamentos(clienteId) {
  const response = await fetch(`/orcamentos?cliente_id=${clienteId}`);
  const orcamentos = await response.json();

  const lista = document.getElementById('lista-orcamentos');
  if (!lista) return;

  lista.innerHTML = "";

  if (!orcamentos.length) {
    lista.innerHTML = "<li>Nenhum orçamento encontrado.</li>";
    return;
  }

  orcamentos.forEach(o => {
    const li = document.createElement("li");
    li.innerHTML = `
      📅 <b>${o.data}</b> — 💰 ${o.total_estimado || '---'}<br>
      <small>${o.descricao}</small>
    `;
    lista.appendChild(li);
  });
}

// 🔹 Profissionais: Tarefas por ID
async function carregarTarefas(profissionalId) {
  const response = await fetch(`/tarefas?profissional_id=${profissionalId}`);
  const tarefas = await response.json();

  const lista = document.getElementById('lista-tarefas');
  if (!lista) return;

  lista.innerHTML = "";

  if (!tarefas.length) {
    lista.innerHTML = "<li>Nenhuma tarefa atribuída.</li>";
    return;
  }

  tarefas.forEach(t => {
    const li = document.createElement("li");
    li.innerHTML = `
      <b>${t.titulo}</b><br>
      Status: ${t.status}<br>
      Entrega: ${t.data_entrega || '--'}
    `;
    lista.appendChild(li);
  });
}

// 🔹 Engenheiro: Status da obra
async function carregarObra(obraId) {
  const response = await fetch(`/obras/${obraId}`);
  const obra = await response.json();

  const div = document.getElementById('status-obra');
  if (!div) return;

  div.innerHTML = `
    <p><b>${obra.titulo}</b></p>
    <ul>
      <li>🟢 Fundação: ${obra.etapas.fundacao}</li>
      <li>🟡 Alvenaria: ${obra.etapas.alvenaria}</li>
      <li>🔌 Elétrica: ${obra.etapas.eletrica}</li>
      <li>🚿 Hidráulica: ${obra.etapas.hidraulica}</li>
      <li>🎨 Acabamento: ${obra.etapas.acabamento}</li>
    </ul>
    <p>📆 Entrega prevista: ${obra.previsao_entrega || '---'}</p>
  `;
}