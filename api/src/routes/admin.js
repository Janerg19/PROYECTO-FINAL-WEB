import express from 'express';
import {
  getCuentasPendientes,
  aprobarCuenta,
  rechazarCuenta,
  getFacultades,
  getProgramas,
} from '../controllers/adminController.js';
import { authenticateToken, requireRole } from '../middleware/auth.js';

const router = express.Router();

router.get('/cuentas-pendientes', authenticateToken, requireRole(['administrador']), getCuentasPendientes);
router.post('/cuentas/:usuario_id/aprobar', authenticateToken, requireRole(['administrador']), aprobarCuenta);
router.post('/cuentas/:usuario_id/rechazar', authenticateToken, requireRole(['administrador']), rechazarCuenta);
router.get('/facultades', getFacultades);
router.get('/programas', getProgramas);

export default router;
