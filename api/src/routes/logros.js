import express from 'express';
import {
  getLogrosPendientes,
  enviarLogro,
  getMisLogros,
  aprobarLogro,
  rechazarLogro,
} from '../controllers/logroController.js';
import { authenticateToken, requireRole } from '../middleware/auth.js';

const router = express.Router();

router.get('/pendientes', authenticateToken, requireRole(['administrador']), getLogrosPendientes);
router.post('/', authenticateToken, enviarLogro);
router.get('/mis-logros', authenticateToken, getMisLogros);
router.post('/:logro_id/aprobar', authenticateToken, requireRole(['administrador']), aprobarLogro);
router.post('/:logro_id/rechazar', authenticateToken, requireRole(['administrador']), rechazarLogro);

export default router;
