// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './css/output.css'
import './App.css'
import Navbar from './components/Navbar.tsx'
import HeroSection from "./components/Hero.tsx";
function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
        <Navbar/><HeroSection/>
    </>
  )
}

export default App
