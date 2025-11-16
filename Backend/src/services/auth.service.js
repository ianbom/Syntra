import prisma from "../config/prisma.js";
import bcrypt from "bcryptjs";
import jwt from 'jsonwebtoken';

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

export const login = async (credentials) => { 

        const {email, password} = credentials;
        const user = await prisma.users.findUnique({ 
            where: { email }
        })

        if (!user) {
            throw new Error('User not found');
        }

        const isPasswordValid = await bcrypt.compare(password, user.password);  
        if (!isPasswordValid) {
            throw new Error('Invalid password');
        }       

        const payload = { 
            id : user.id,
            name: user.name,
            email: user.email,
            role: user.role
        }

        const token = jwt.sign(payload, process.env.JWT_SECRET, {
            expiresIn: process.env.JWT_EXPIRES_IN || '1d'
        })

        delete user.password; 

        return { 
            user, token
        }
}



export const myProfile = (userId) => {

    const myProfile = prisma.users.findUnique({
        where: { id: userId }});

    if (!myProfile) {
        throw new Error('User not found');
    }
    delete myProfile.password;
    return myProfile;

}