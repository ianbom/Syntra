import prisma from "../config/prisma.js";
import {successResponse} from "../utils/response.js"
import bcrypt from "bcryptjs";

export const register = async (userData) => { 

    const {name, email, password} = userData; 

    const existingEmail = await prisma.users.findUnique({
        where:{email: email}
    });

    if(existingEmail){
        throw new Error('Email already in use');
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const newUser = await prisma.users.create({
        data: {
            name: name,
            email: email,
            password: hashedPassword, 
            role: "user"
        }
    });

    delete newUser.password;  

    return newUser;
}