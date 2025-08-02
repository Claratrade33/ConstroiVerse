exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ sucesso: false, erro: 'Usuário não encontrado' });

    const senhaCorreta = await bcrypt.compare(password, user.password);
    if (!senhaCorreta) return res.status(401).json({ sucesso: false, erro: 'Senha incorreta' });

    const token = jwt.sign(
      { id: user._id, mainProfile: user.mainProfile, role: user.role, permissions: user.permissions },
      process.env.JWT_SECRET,
      { expiresIn: '12h' }
    );

    res.json({
      sucesso: true,
      token,
      redirect: `/painel/${user.mainProfile}`, // 🔁 redirecionamento por perfil
      perfil: user.mainProfile,
      role: user.role,
      permissions: user.permissions
    });
  } catch (err) {
    res.status(500).json({ sucesso: false, erro: err.message });
  }
};