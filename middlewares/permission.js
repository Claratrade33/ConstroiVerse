module.exports = function(requiredPermissions = []) {
  return (req, res, next) => {
    const user = req.user; // vindo do token JWT decodificado

    const hasPermission = requiredPermissions.every(p => user.permissions.includes(p));
    if (!hasPermission) {
      return res.status(403).json({ erro: 'Permissão negada' });
    }

    next();
  };
};