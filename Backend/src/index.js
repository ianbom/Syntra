import "dotenv/config";
import express from "express";
import authRoutes from "./routes/admin/auth.route.js";
import documentRoutes from "./routes/admin/document.route.js";
const app = express();
app.use(express.json());

app.get("/", (req, res) => {
  res.json({ message: "Hello World!" });
});

app.use('/api/admin/auth', authRoutes);
app.use('/api/admin/document', documentRoutes);


app.listen(5000, () => console.log("Server running on port 5000"));
