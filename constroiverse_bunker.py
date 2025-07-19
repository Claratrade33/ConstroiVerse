<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ConstroiVerse | Bunker do Construtor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            margin: 0;
            background: #0f0f0f;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }

        header {
            background-color: #00c4b4;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: black;
        }

        nav {
            background-color: #121212;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            padding: 10px;
        }

        nav button {
            background: #1f1f1f;
            border: 2px solid #00c4b4;
            color: #00f0ff;
            padding: 10px 15px;
            margin: 5px;
            border-radius: 8px;
            cursor: pointer;
        }

        nav button:hover {
            background-color: #00c4b4;
            color: black;
        }

        section {
            padding: 20px;
            display: none;
        }

        section.active {
            display: block;
        }

        .card {
            background-color: #1a1a1a;
            border: 1px solid #00f0ff44;
            border-left: 6px solid #00c4b4;
            margin: 20px auto;
            padding: 20px;
            max-width: 600px;
            box-shadow: 0 0 10px #00f0ff33;
            border-radius: 10px;
        }
    </style>
</head>
<body>

<header>🔨 ConstroiVerse – Painel do Construtor</header>

<nav>
    <button onclick="navegar('dashboard')">Dashboard</button>
    <button onclick="navegar('projetos')">Central de Projetos</button>
    <button onclick="navegar('acompanhamento')">Acompanhamento</button>
    <button onclick="navegar('previsao')">Previsão & Custo</button>
    <button onclick="navegar('calculadora')">Calculadora</button>
    <button onclick="navegar('financiamento')">Simular Financiamento</button>
    <button onclick="navegar('corretores')">Rede de Corretores</button>
</nav>

<main>
    <section id="dashboard" class="active">
        <div class="card">
            <h2>📊 Dashboard</h2>
            <p>Resumo geral das obras, custos e progresso em tempo real.</p>
        </div>
    </section>

    <section id="projetos">
        <div class="card">
            <h2>📁 Central de Projetos</h2>
            <p>Todos os projetos organizados por fase, categoria e status.</p>
        </div>
    </section>

    <section id="acompanhamento">
        <div class="card">
            <h2>📍 Acompanhamento de Obra</h2>
            <p>Veja o que está pronto, o que está em andamento e o que falta com cronograma visual.</p>
        </div>
    </section>

    <section id="previsao">
        <div class="card">
            <h2>📅 Previsão e Custo</h2>
            <p>Tempo estimado, materiais necessários e valor total com base nos acabamentos escolhidos.</p>
        </div>
    </section>

    <section id="calculadora">
        <div class="card">
            <h2>🧮 Calculadora Inteligente</h2>
            <p>Insira as medidas e veja quanto material precisa, tempo, custo e margem de sobra.</p>
        </div>
    </section>

    <section id="financiamento">
        <div class="card">
            <h2>💰 Simulador de Financiamento</h2>
            <p>Veja quanto pegar no banco, qual será a taxa, os juros e quanto custará sua obra no final.</p>
        </div>
    </section>

    <section id="corretores">
        <div class="card">
            <h2>🌐 Rede de Corretores</h2>
            <p>Encontre arquitetos, mestres de obra, fornecedores e parceiros perto de você.</p>
        </div>
    </section>
</main>

<script>
    function navegar(pagina) {
        document.querySelectorAll('section').forEach(sec => sec.classList.remove('active'));
        document.getElementById(pagina).classList.add('active');
    }
</script>

</body>
</html>