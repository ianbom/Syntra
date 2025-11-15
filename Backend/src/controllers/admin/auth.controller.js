import {successResponse, errorResponse} from "../../utils/response.js"
import { register } from "../../services/auth.service.js";

export const adminRegister = async (req, res) => {
    try {
        const newUser = await register(req.body);
        return successResponse(
            res,
            "User registered successfully",
            newUser,
            201
        );
    } catch (err) {
        return errorResponse(
            res,
            err.message || "Failed to register user",
            400
        );
    }
};
