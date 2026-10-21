import express from 'express';
import cors from 'cors';
import pool from './config/database.js';

// Routes
import authRoutes from './routes/auth.js';
import publicacionesRoutes from './routes/publicaciones.js';
import semillerosRoutes from './routes/semilleros.js';
import logrosRoutes from './routes/logros.js';
import adminRoutes from './routes/admin.js';
import rankingRoutes from './routes/ranking.js';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Health check
app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'healthy', database: 'connected' });
  } catch (error) {
    res.status(500).json({ status: 'unhealthy', database: 'disconnected' });
  }
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/publicaciones', publicacionesRoutes);
app.use('/api/semilleros', semillerosRoutes);
app.use('/api/logros', logrosRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api/ranking', rankingRoutes);

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Error interno del servidor' });
});

// Start server
app.listen(PORT, () => {
  console.log(`API RIUL corriendo en puerto ${PORT}`);
});
