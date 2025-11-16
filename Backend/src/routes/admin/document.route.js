import { Router } from 'express';
import { upload } from "../../config/multer.js";
import { uploadDocument } from '../../controllers/admin/document.controller.js';

const router = Router();

router.post("/", upload.single("file"), uploadDocument);

export default router;