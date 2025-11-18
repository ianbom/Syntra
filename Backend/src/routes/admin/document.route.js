import { Router } from 'express';
import { upload } from "../../config/multer.js";
import { getEmbeddingRes, uploadDocument } from '../../controllers/admin/document.controller.js';

const router = Router();

router.post("/", upload.single("file"), uploadDocument);
router.post("/embed", getEmbeddingRes);
export default router;