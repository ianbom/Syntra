import { adminRegister } from "../../controllers/admin/auth.controller.js";
import { Router } from 'express';

const router = Router();
router.post("/register", adminRegister);

export default router;