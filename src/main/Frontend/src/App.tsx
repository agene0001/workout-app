// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './css/output.css'
import Navbar from './components/Navbar.tsx'
import Nutrition from './components/Nutrition.tsx'
import Chatbot from "./components/chatbot.tsx"
import Games from './components/Games.tsx'
import HeroSection from "./components/Hero.tsx";
import {Route, Routes} from "react-router-dom"

function App() {
    // const [count, setCount] = useState(0)

    return (
            <Routes>
                <Route path="/" element={<><div className='container fixed-top'><Chatbot/><Navbar name='Home'/> </div><HeroSection/></>}/>
                <Route path="/Nutrition" element={<><div className='container fixed-top'><Navbar name='Nutrition'/></div> <Nutrition/></>}/>
                <Route path="/Games" element={<><div className='container fixed-top'><Navbar name='Games'/></div> <Games/></>
                }/>
                </Routes>


    )
}


export default App



