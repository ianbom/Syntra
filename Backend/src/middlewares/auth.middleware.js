import jwt from 'jsonwebtoken';

export const authenticateToken = (req, res, next) => {

    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ message: 'Access token is missing' });
    }
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ message: 'Invalid access token' });
        }
        req.user = user; 
        next(); 
    });

}

export const authorizeRole = (allowedRoles) => {
  return (req, res, next) => {
    if (!req.user || !req.user.role) {
      return res.status(403).json({ message: 'Forbidden: Peran pengguna tidak diketahui.' });
    }
    const { role } = req.user;
    if (!allowedRoles.includes(role)) {
      return res.status(403).json({ message: 'Forbidden: Anda tidak memiliki akses untuk sumber daya ini.' });
    }

    next();
  };
};
