'use client'
import {useRef, useEffect, useState} from "react";
import InfoBlock from "./InfoBlock";
// import Granim from "granim";
import anime from 'animejs'

// Responsive styles for headings
// const heroHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '4rem', padding: '1.5rem', marginTop: '7rem'};
// const subHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '2.5rem'};
// const paraStyle: CSSProperties = {textAlign: 'center', fontSize: '1.5rem'};

function HeroSection() {
    const myRef1 = useRef<HTMLDivElement|null>(null);
    const myRef2 = useRef<HTMLDivElement|null>(null);
    const myRef3 = useRef<HTMLDivElement|null>(null);
    const infoTitle1: string = 'Exceptional Archive'
    const infoTitle2: string = 'Personalized Nutrition'
    const infoTitle3: string = 'Progress Tracker/ Forum Groups'
    const [heroStart, setHeroStartIsVisible] = useState(false);
    const [heroSecond, setHeroSecondIsVisible] = useState(false);
    const [blocks, setBlocksIsVisible] = useState(false);

    useEffect(() => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.target.className.includes('container1')) {
                    setHeroStartIsVisible(entry.isIntersecting);
                } else if (entry.target.className.includes('layer3')) {
                    setHeroSecondIsVisible(entry.isIntersecting);
                } else {
                    setBlocksIsVisible(entry.isIntersecting);
                }
            })
        })
        const duration = 50000
        const ease = 'linear'
        const direction = 'alternate'
        const opac = .5
        anime({
            targets: '#pt1',
            fill: [`rgba(173,83,137,${opac})`, `rgba(6,23,0,${opac})`, `rgba(204,43,94,${opac})`, `rgba(165,254,203,${opac})`, '#000'],
            easing: ease,
            duration: duration,
            direction: direction,
            delay: 1000,
            loop: true
        });
        anime({
            targets: '#pt2',
            fill: [`rgba(158, 74, 130,${opac})`, `rgba(16, 45, 7,${opac})`, `rgba(194, 45, 99,${opac})`, `rgba(136,240,214,${opac})`, '#030304'],
            easing: ease,
            duration: duration,
            direction: direction,
            delay: 1000,
            loop: true
        });
        anime({
            targets: '#pt3',
            fill: [`rgba(142, 65, 122,${opac})`, `rgba(26, 67, 14,${opac})`, `rgba(181, 47, 105,${opac})`, `rgba(97,221,230,${opac})`, '#050506'],
            easing: ease,
            duration: duration,
            direction: direction,
            delay: 1000,
            loop: true
        });
        anime({
            targets: '#pt4',
            fill: [`rgba(121, 52, 112,${opac})`, `rgba(39, 95, 23,${opac})`, `rgba(166, 50, 112,${opac}`, `rgba(32,189,255,${opac})`, '#080809'],
            easing: ease,
            duration: duration,
            direction: direction,
            delay: 1000,
            loop: true
        });
        anime({
            targets: '#pt5',
            fill: [`rgba(101, 40, 102,${opac})`, `rgba(52, 125, 32,${opac})`, `rgba(153, 52, 118,${opac})`, `rgba(58,120,255,${opac})`, '#0b0b0c'],
            easing: ease,
            duration: duration,
            direction: direction,
            delay: 1000,
            loop: true
        });
        anime({
            targets: '#pt6',
            fill: [`rgba(75, 25, 90,${opac})`, `rgba(66, 158, 41,${opac})`, `rgba(132, 55, 128,${opac})`, `rgba(70,89,255,${opac})`, '#0d0d0e'],
            easing: ease,
            duration: duration,
            direction: direction,
            delay: 1000,
            loop: true
        });
        anime({
            targets: '#pt7,#pt8',
            fill: [`rgba(60, 16, 83,${opac})`, `rgba(82, 194, 52,${opac})`, `rgba(117, 58, 136,${opac})`, `rgba(84,51,255,${opac})`, `#0f0f10`],
            easing: ease,
            duration: duration,
            direction: direction,
            delay: 1000,
            loop: true
        });

        // Only observe if the ref is not null
        if (myRef1.current) observer.observe(myRef1.current);
        if (myRef2.current) observer.observe(myRef2.current);
        if (myRef3.current) observer.observe(myRef3.current);

        return () => {
            // Clean up the observer
            if (myRef1.current) observer.unobserve(myRef1.current);
            if (myRef2.current) observer.unobserve(myRef2.current);
            if (myRef3.current) observer.unobserve(myRef3.current);
        };

    }, [])

    return (
        <>
            <div className='container1 peaks container-fluid justify-content-center' style={{textAlign: 'center'}} ref={myRef1}>
                <div className={`p-3 justify-content-center align-content-center`} id='hero'>
                    <div className={`${heroStart ? 'heroStart' : ''}`}>
                        <h1 id='heroText'>Unleashing Your Potential Through Fitness and Nutrition</h1>
                    </div>
                </div>
            </div>
            <div className='container2 spacer layer1'></div>
            <div ref={myRef2} className="container-fluid stackedHaikei layer3 py-3" id="hero2">
                <section>
                    <h1 className={`display-4 text-danger ${heroSecond ? 'heroStart' : ''}`}>Achieve Peak Fitness and Wellness with Our Comprehensive Site</h1>
                    <p style={{fontSize:'1.3rem'}} className={`text-primary ${heroSecond ? 'heroStart1' : ''}`}>At our platform, we're passionate about building a vibrant community where individuals can thrive in their active lifestyles. Our goal is to provide a holistic approach to health and wellness by offering a diverse range of workout disciplines, personalized nutrition guidance, and a supportive environment for like-minded peers to connect and learn.</p>
                </section>
            </div>
            <div className="container-fluid text-center vh-100 align-content-center py-3" id="hero3">
                <div ref={myRef3} className='row py-3'>
                    <div className="col-12 col-md-4">
                        <InfoBlock fadeInAnimation={`${blocks ? 'infoHero' : ''}`} heading={infoTitle1} text={[`This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit in iste libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti deserunt dicta facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde voluptas voluptatum.`]} />
                    </div>
                    <div className="col-12 col-md-4">
                        <InfoBlock fadeInAnimation={`${blocks ? 'infoHero1' : ''}`} heading={infoTitle2} text={[`This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit in iste libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti deserunt dicta facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde voluptas voluptatum.`]} />
                    </div>
                    <div className="col-12 col-md-4">
                        <InfoBlock fadeInAnimation={`${blocks ? 'infoHero ' : ''}`} heading={infoTitle3} text={[`This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit in iste libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti deserunt dicta facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde voluptas voluptatum.`]} />
                    </div>
                </div>
            </div>
        </>
    );
}

export default HeroSection;