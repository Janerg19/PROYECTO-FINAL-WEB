import express from 'express';
import {
  getPublicaciones,
  createPublicacion,
  comentar,
  reaccionar,
  compartir,
} from '../controllers/publicacionController.js';
import { authenticateToken, optionalAuth } from '../middleware/auth.js';

const router = express.Router();

router.get('/', optionalAuth, getPublicaciones);
router.post('/', authenticateToken, createPublicacion);
router.post('/comentar', authenticateToken, comentar);
router.post('/reaccionar', authenticateToken, reaccionar);
router.post('/compartir', authenticateToken, compartir);

export default router;
