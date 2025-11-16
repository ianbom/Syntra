import { adminRegister, adminLogin, adminProfile } from "../../controllers/admin/auth.controller.js";
import { Router } from 'express';
import { authenticateToken } from "../../middlewares/auth.middleware.js";

const router = Router();
router.post("/register", adminRegister);
router.post("/login", adminLogin);

router.get("/myProfile", authenticateToken, adminProfile);

export default router;