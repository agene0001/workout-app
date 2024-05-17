// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './css/output.css'
import './App.css'
import Navbar from './components/Navbar.tsx'
import Nutrition from './components/Nutrition.tsx'
import Games from './components/Games.tsx'
import HeroSection from "./components/Hero.tsx";
import {Route, Routes} from "react-router-dom"

function App() {
    // const [count, setCount] = useState(0)

    return (
        <div className="container-fluid">
            <Routes>
                <Route path="/" element={<><Navbar name='Home'/> <HeroSection/></>}/>
                <Route path="/Nutrition" element={<div className='fixed-top'><Navbar name='Nutrition'/> <Nutrition/></div>}/>
                <Route path="/Games" element={<><Navbar name='Games'/> <Games/></>}/>
            </Routes>
        </div>


    )
}


export default App



