// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAetUW9qraDo4FK76d7ZJBjjFf6PjZivWE",
  authDomain: "prodmind-ai.firebaseapp.com",
  projectId: "prodmind-ai",
  storageBucket: "prodmind-ai.firebasestorage.app",
  messagingSenderId: "10055147272",
  appId: "1:10055147272:web:e641a48176b721018296bd",
  measurementId: "G-8C8PLP8Q30"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db };
