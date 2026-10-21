import express from 'express';
import {
  getSemilleros,
  getSemilleroById,
  solicitarVinculacion,
  getIntegrantes,
  resolverVinculacion,
} from '../controllers/semilleroController.js';
import { authenticateToken, requireRole } from '../middleware/auth.js';

const router = express.Router();

router.get('/', getSemilleros);
router.get('/:id', getSemilleroById);
router.post('/solicitar-vinculacion', authenticateToken, solicitarVinculacion);
router.get('/:id/integrantes', getIntegrantes);
router.post('/resolver-vinculacion', authenticateToken, requireRole(['docente', 'administrador']), resolverVinculacion);

export default router;
