import { GoogleGenAI } from "@google/genai";
import dotenv from "dotenv";
dotenv.config();
const client = new GoogleGenAI({ apiKey: process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY });

const response = await client.models.list();
console.log("Keys:", Object.keys(response));
if (response.models) {
    console.log("Models inside response.models:", response.models.map(m => m.name));
} else {
    for (const key in response) {
        if (Array.isArray(response[key])) {
             console.log("Array found at key:", key, response[key].map(m => m.name));
        }
    }
}