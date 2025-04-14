import './css/tailwind-output.css'
import Navbar from './components/Navbar.tsx'
import Nutrition from './pages/Nutrition.tsx'
import AboutUs from './pages/AboutUs.tsx'
import Groups from './pages/Groups.tsx'
import HeroSection from "./pages/Hero.tsx";
import {Route, Routes} from "react-router-dom"

function App() {
    return (
        <Routes>
            <Route path="/" element={
                <>
                    <div className="w-full fixed top-0 flex justify-center z-50">
                        <div className="max-w-7xl w-full px-4">
                            <Navbar name='Home'/>
                        </div>
                    </div>
                    <HeroSection/>
                </>
            }/>
            <Route path="/Nutrition" element={
                <>
                    <div className="w-full fixed top-0 flex justify-center z-50">
                        <div className="max-w-7xl w-full px-4">
                            <Navbar name='Nutrition'/>
                        </div>
                    </div>
                    <Nutrition/>
                </>
            }/>
            <Route path="/Groups" element={
                <>
                    <div className="w-full fixed top-0 flex justify-center z-50">
                        <div className="max-w-7xl w-full px-4">
                            <Navbar name='Groups'/>
                        </div>
                    </div>
                    <Groups/>
                </>
            }/>
            <Route path="/About-Us" element={
                <>
                    <div className="w-full fixed top-0 flex justify-center z-50">
                        <div className="max-w-7xl w-full px-4">
                            <Navbar name='About-Us'/>
                        </div>
                    </div>
                    <AboutUs/>
                </>
            }/>
        </Routes>
    )
}

export default App