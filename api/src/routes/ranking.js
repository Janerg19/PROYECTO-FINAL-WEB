import express from 'express';
import {
  getRankingSemilleros,
  getRankingInvestigadores,
  getKPIs,
  getIndicadoresFacultad,
  getHojaVida,
} from '../controllers/rankingController.js';
import { optionalAuth } from '../middleware/auth.js';

const router = express.Router();

router.get('/semilleros', getRankingSemilleros);
router.get('/investigadores', getRankingInvestigadores);
router.get('/kpis', getKPIs);
router.get('/indicadores-facultad', getIndicadoresFacultad);
router.get('/hoja-vida/:usuario_id', getHojaVida);

export default router;
