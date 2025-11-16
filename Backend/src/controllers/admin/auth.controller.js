import {successResponse, errorResponse} from "../../utils/response.js"
import { register, login, myProfile } from "../../services/auth.service.js";

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

export const adminLogin = async (req, res) => {
    try {
        const result = await login(req.body);
        return successResponse(res, "Login successful", result, 200);
    } catch (error) {
        return errorResponse(res, error.message || "Login failed", 400);
    }   

}

export const adminProfile = async (req, res) => {

    try {
        
        const userId = req.user.id;
        const profile = await myProfile(userId);
        return successResponse(res, "Profile fetched successfully", profile, 200);

    } catch (error) {
        return errorResponse(res, error.message || "Failed to fetch profile", 400);
    }

} 