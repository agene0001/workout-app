'use client'
import {useRef, useEffect, useState} from "react";
import InfoBlock from "../components/InfoBlock.tsx";
import anime from 'animejs'

function HeroSection() {
    const myRef1 = useRef<HTMLDivElement|null>(null);
    const myRef2 = useRef<HTMLDivElement|null>(null);
    const myRef3 = useRef<HTMLDivElement|null>(null);
    const infoTitle1: string = 'Exceptional Archive'
    const infoTitle2: string = 'Personalized Nutrition'
    const infoTitle3: string = 'Progress Tracker/ Forum Groups (BETA)'
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
            <div className="container1 peaks w-full" ref={myRef1}>
                <div className="pt-25 flex justify-center items-center w-full" >
                    <div className={`w-full text-center ${heroStart ? 'hero-start' : ''}`}>
                        <h1 id="heroText" className=" text-6xl font-orbital font-bold mx-auto text-[#00dd87]">
                            Unleashing Your Potential Through <span className='text-gradient-2'>Fitness and Nutrition</span>
                        </h1>
                    </div>
                </div>
            </div>
            <div className='container2 spacer layer1'></div>
            <div ref={myRef2} className="bg-no-repeat bg-center bg-cover py-3 layer3 container1">
                <section>
                    <h1 className={`text-3xl md:text-4xl lg:text-5xl font-orbital font-bold text-[#00A76E] ${heroSecond ? 'hero-start' : ''}`}>Achieve Peak Fitness and Wellness with Our Comprehensive Site</h1>
                    <p className={`text-xl text-[#faebd7] ${heroSecond ? 'hero-start-delay' : ''}`}>At our platform, we're passionate about building a vibrant community where individuals can thrive in their active lifestyles. Our goal is to provide a holistic approach to health and wellness by offering a diverse range of workout disciplines, personalized nutrition guidance, and a supportive environment for like-minded peers to connect and learn.</p>
                </section>
            </div>
            <div className="container mx-auto text-center h-screen flex items-center py-3 relative">
                <div ref={myRef3} className='grid grid-cols-1 md:grid-cols-3 gap-6 py-3'>
                    <div>
                        <InfoBlock fadeInAnimation={`${blocks ? 'info-hero' : ''}`} title={infoTitle1} heading={<h1 className="text-4xl font-orbital font-bold">{infoTitle1}</h1>} expandable={false} text={[`"Our Exceptional Archive brings together a vast repository of food options. Here, you can explore a wide range of recipes tailored to meet your dietary preferences. Whether you're seeking tips on how to optimize your workout nutrition or interested in the latest sports betting insights, our archive provides the perfect blend of information to help you level up your fitness journey.`]} />
                    </div>
                    <div>
                        <InfoBlock fadeInAnimation={`${blocks ? 'info-hero1' : ''}`} title={infoTitle2} heading={<h1 className="text-4xl font-orbital font-bold">{infoTitle2}</h1>} expandable={false} text={[`At the heart of our platform is a Personalized Nutrition system powered by a state-of-the-art recommender. This intelligent system analyzes your unique dietary preferences, activity levels, and fitness goals to recommend the most suitable recipes for your needs. We continuously update our meal plans and recipes based on the latest research, ensuring you get the right balance of nutrition to fuel your workouts and promote overall health.`]} />
                    </div>
                    <div>
                        <InfoBlock fadeInAnimation={`${blocks ? 'info-hero' : ''}`} title={infoTitle3} heading={<h1 className="text-4xl font-orbital font-bold">{infoTitle3}</h1>} expandable={false} text={[`Our Progress Tracker is a powerful tool that lets you monitor your fitness journey with detailed insights into your workouts, nutrition, and milestones. Alongside the tracker, our Forum Groups provide a space for you to connect with others who share similar fitness goals, discuss strategies, and exchange tips. Whether you're aiming to lose weight, build muscle, or simply improve your overall fitness, these tools create a supportive environment for tracking your progress and engaging with a community of like-minded individuals.`]} />
                    </div>
                </div>
            </div>
        </>
    );
}

export default HeroSection;