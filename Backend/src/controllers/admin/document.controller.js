import { createDocument } from "../../services/document.service.js";
import { successResponse, errorResponse } from "../../utils/response.js";

export const uploadDocument = async (req, res) => {
  try {
    const result = await createDocument(req.body, req.file);

    return successResponse(
      res,
      "Document uploaded successfully",
      result,
      201
    );
  } catch (err) {
    return errorResponse(res, err.message, 400);
  }
};

