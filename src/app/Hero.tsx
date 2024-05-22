'use client'
import {CSSProperties, useRef, useEffect, useState} from "react";
import InfoBlock from "./InfoBlock";
import Granim from "granim";
import anime from 'animejs'

let heroHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '6rem', padding: '1.5rem'};
let subHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '3rem'}


let paraStyle: CSSProperties = {textAlign: 'center', fontSize: '1.5rem'}

function HeroSection() {
    const myRef1 = useRef(null);
    const myRef2 = useRef(null);
    const myRef3 = useRef(null);
    const infoTitle: string = 'Exceptional Archive'
    const infoTitle1: string = 'Personalized Nutrition'
    const infoTitle2: string = 'Progress Tracker/ Forum Groups'
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
            // const entry = entries[0];
            // setMyElementIsVisible(entry.isIntersecting);
        })

        observer.observe(myRef1.current);
        observer.observe(myRef2.current);
        observer.observe(myRef3.current);
        var duration = 70000
        var ease = 'linear'
        var direction = 'alternate'
        var opac = .25
        anime({
            targets: '#pt1',
            fill: ['#000',`rgba(173,83,137,${opac})`,`rgba(6,23,0,${opac})`,`rgba(204,43,94,${opac})`,`rgba(165,254,203,${opac})`,'#000'],
            easing: ease,
            duration: duration,
            direction: direction,
            loop: true
        });      anime({
            targets: '#pt2',
            fill: ['#030304',`rgba(158, 74, 130,${opac})`,`rgba(16, 45, 7,${opac})`, `rgba(194, 45, 99,${opac})`,`rgba(136,240,214,${opac})`,'#030304'],
            easing: ease,
            duration: duration,
            direction: direction,
            loop: true
        });      anime({
            targets: '#pt3',
            fill: ['#050506',`rgba(142, 65, 122,${opac})`,`rgba(26, 67, 14,${opac})`,`rgba(181, 47, 105,${opac})`,`rgba(97,221,230,${opac})`,'#050506'],
            easing: ease,
            duration: duration,
            direction: direction,
            loop: true
        });      anime({
            targets: '#pt4',
            fill: ['#080809',`rgba(121, 52, 112,${opac})`, `rgba(39, 95, 23,${opac})`,`rgba(166, 50, 112,${opac}`,`rgba(32,189,255,${opac})`,'#080809'],
            easing: ease,
            duration: duration,
            direction: direction,
            loop: true
        });      anime({
            targets: '#pt5',
            fill: ['#0b0b0c',`rgba(101, 40, 102,${opac})`,`rgba(52, 125, 32,${opac})`,`rgba(153, 52, 118,${opac})`,`rgba(58,120,255,${opac})`,'#0b0b0c'],
            easing: ease,
            duration: duration,
            direction: direction,
            loop: true
        });   anime({
            targets: '#pt6',
            fill: [ '#0d0d0e',`rgba(75, 25, 90,${opac})`, `rgba(66, 158, 41,${opac})`,`rgba(132, 55, 128,${opac})`,`rgba(70,89,255,${opac})`,'#0d0d0e'],
            easing: ease,
            duration: duration,
            direction: direction,
            loop: true
        });   anime({
            targets: '#pt7,#pt8',
            fill: [`#0f0f10`,`rgba(60, 16, 83,${opac})`, `rgba(82, 194, 52,${opac})`,`rgba(117, 58, 136,${opac})`,`rgba(84,51,255,${opac})`,`#0f0f10`],
            easing: ease,
            duration: duration,
            direction: direction,
            loop: true
        });

    }, [])

    // It
    return (
        <>
            <div className='container1' ref={myRef1}>
                <svg id="visual" className='svgBg' viewBox="0 0 900 600" width="900" height="600"
                     xmlns="http://www.w3.org/2000/svg"
                     version="1.1" >

                    <path
                        d="M0 79L82 55L164 85L245 55L327 73L409 61L491 37L573 73L655 49L736 61L818 49L900 61L900 0L818 0L736 0L655 0L573 0L491 0L409 0L327 0L245 0L164 0L82 0L0 0Z"
                        fill="#000000" id="pt1"></path>
                    <path
                        d="M0 205L82 175L164 289L245 175L327 241L409 247L491 187L573 247L655 271L736 229L818 229L900 175L900 59L818 47L736 59L655 47L573 71L491 35L409 59L327 71L245 53L164 83L82 53L0 77Z"
                        fill="#030304" id="pt2"></path>
                    <path
                        d="M0 241L82 235L164 331L245 211L327 301L409 289L491 241L573 295L655 307L736 283L818 265L900 211L900 173L818 227L736 227L655 269L573 245L491 185L409 245L327 239L245 173L164 287L82 173L0 203Z"
                        fill="#050506" id="pt3"></path>
                    <path
                        d="M0 283L82 271L164 367L245 247L327 343L409 319L491 277L573 331L655 361L736 343L818 295L900 277L900 209L818 263L736 281L655 305L573 293L491 239L409 287L327 299L245 209L164 329L82 233L0 239Z"
                        fill="#080809" id="pt4"></path>
                    <path
                        d="M0 463L82 469L164 469L245 427L327 463L409 439L491 451L573 433L655 469L736 415L818 391L900 433L900 275L818 293L736 341L655 359L573 329L491 275L409 317L327 341L245 245L164 365L82 269L0 281Z"
                        fill="#0b0b0c" id="pt5"></path>
                    <path
                        d="M0 523L82 553L164 553L245 547L327 541L409 547L491 505L573 511L655 541L736 529L818 529L900 523L900 431L818 389L736 413L655 467L573 431L491 449L409 437L327 461L245 425L164 467L82 467L0 461Z"
                        fill="#0d0d0e" id="pt6"></path>
                    <path
                        d="M0 601L82 601L164 601L245 601L327 601L409 601L491 601L573 601L655 601L736 601L818 601L900 601L900 521L818 527L736 527L655 539L573 509L491 503L409 545L327 539L245 545L164 551L82 551L0 521Z"
                        fill="#0f0f10" id="pt7"></path>

                </svg>
                <div
                     className={`d-flex justify-content-end align-items-center container-fluid p-3`}
                     id='hero'>
                    <div className={`d-block ${heroStart ? 'heroStart' : ''}`}>
                        <h1 style={heroHeadingStyle} id='heroText'>Unleashing Your Potential Through Fitness and
                            Nutrition</h1>
                    </div>

                </div>
            </div>
            <div className='container2'>
                <svg id="visual" className='svgBg' viewBox="0 0 920 200" width="920" height="200" xmlns="http://www.w3.org/2000/svg"
                     version="1.1">
                    <rect x="0" y="0" width="920" height="200" id='pt8' fill="#0f0f10"></rect>
                    <path
                        d="M0 72L21.8 69.8C43.7 67.7 87.3 63.3 131.2 61.7C175 60 219 61 262.8 59.2C306.7 57.3 350.3 52.7 394.2 57.3C438 62 482 76 525.8 78.5C569.7 81 613.3 72 657.2 67.7C701 63.3 745 63.7 788.8 59.8C832.7 56 876.3 48 898.2 44L920 40L920 201L898.2 201C876.3 201 832.7 201 788.8 201C745 201 701 201 657.2 201C613.3 201 569.7 201 525.8 201C482 201 438 201 394.2 201C350.3 201 306.7 201 262.8 201C219 201 175 201 131.2 201C87.3 201 43.7 201 21.8 201L0 201Z"
                        fill="#c62368"></path>
                    <path
                        d="M0 103L21.8 103.5C43.7 104 87.3 105 131.2 98.3C175 91.7 219 77.3 262.8 72.5C306.7 67.7 350.3 72.3 394.2 75.7C438 79 482 81 525.8 83.8C569.7 86.7 613.3 90.3 657.2 94.3C701 98.3 745 102.7 788.8 102.5C832.7 102.3 876.3 97.7 898.2 95.3L920 93L920 201L898.2 201C876.3 201 832.7 201 788.8 201C745 201 701 201 657.2 201C613.3 201 569.7 201 525.8 201C482 201 438 201 394.2 201C350.3 201 306.7 201 262.8 201C219 201 175 201 131.2 201C87.3 201 43.7 201 21.8 201L0 201Z"
                        fill="#98225f"></path>
                    <path
                        d="M0 112L21.8 114C43.7 116 87.3 120 131.2 122.8C175 125.7 219 127.3 262.8 125.7C306.7 124 350.3 119 394.2 116.3C438 113.7 482 113.3 525.8 113.8C569.7 114.3 613.3 115.7 657.2 117.7C701 119.7 745 122.3 788.8 123C832.7 123.7 876.3 122.3 898.2 121.7L920 121L920 201L898.2 201C876.3 201 832.7 201 788.8 201C745 201 701 201 657.2 201C613.3 201 569.7 201 525.8 201C482 201 438 201 394.2 201C350.3 201 306.7 201 262.8 201C219 201 175 201 131.2 201C87.3 201 43.7 201 21.8 201L0 201Z"
                        fill="#6d2050"></path>
                    <path
                        d="M0 147L21.8 146.3C43.7 145.7 87.3 144.3 131.2 140C175 135.7 219 128.3 262.8 128.7C306.7 129 350.3 137 394.2 142C438 147 482 149 525.8 149C569.7 149 613.3 147 657.2 144.3C701 141.7 745 138.3 788.8 138.2C832.7 138 876.3 141 898.2 142.5L920 144L920 201L898.2 201C876.3 201 832.7 201 788.8 201C745 201 701 201 657.2 201C613.3 201 569.7 201 525.8 201C482 201 438 201 394.2 201C350.3 201 306.7 201 262.8 201C219 201 175 201 131.2 201C87.3 201 43.7 201 21.8 201L0 201Z"
                        fill="#451a3b"></path>
                    <path
                        d="M0 180L21.8 179.7C43.7 179.3 87.3 178.7 131.2 175.3C175 172 219 166 262.8 163.3C306.7 160.7 350.3 161.3 394.2 161.3C438 161.3 482 160.7 525.8 161.8C569.7 163 613.3 166 657.2 165.5C701 165 745 161 788.8 159C832.7 157 876.3 157 898.2 157L920 157L920 201L898.2 201C876.3 201 832.7 201 788.8 201C745 201 701 201 657.2 201C613.3 201 569.7 201 525.8 201C482 201 438 201 394.2 201C350.3 201 306.7 201 262.8 201C219 201 175 201 131.2 201C87.3 201 43.7 201 21.8 201L0 201Z"
                        fill="#231123"></path>
                </svg>
            </div>
            {/*<div className="spacer layer1"></div>*/}
            <div ref={myRef2} className="container-fluid stackedHaikei layer3 py-3" id="hero2">
                <section>
                    <h1 style={subHeadingStyle} className={`text-info ${heroSecond ? 'heroStart' : ''}`}>Achieve Peak
                        Fitness and Wellness with Our
                        Comprehensive Site</h1>
                    <p style={paraStyle} className={`text-primary ${heroSecond ? 'heroStart1' : ''}`}><br/> At our
                        platform, we're passionate about
                        building
                        a vibrant community
                        where individuals can thrive in their active lifestyles. Our goal is to provide a
                        holistic
                        approach to health and wellness by offering a diverse range of workout disciplines,
                        personalized
                        nutrition guidance, and a supportive environment for like-minded peers to connect and
                        learn.

                    </p>
                </section>
            </div>
            <div className="container-fluid text-center vh-100 align-content-center py-3" id="hero3">
                <div ref={myRef3} className='row py-3'>
                    <InfoBlock animation={`${blocks ? 'infoHero' : ''}`} heading={infoTitle} text={[`This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                           in iste
                           libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                           deserunt dicta
                           facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                           voluptas
                           voluptatum.`]} icon={null}/>
                    <InfoBlock animation={`${blocks ? 'infoHero1' : ''}`} heading={infoTitle1} text={[`This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                           in iste
                           libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                           deserunt dicta
                           facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                           voluptas
                           voluptatum.`]} icon={null}/>

                    <InfoBlock animation={`${blocks ? 'infoHero2' : ''}`} heading={infoTitle2} text={[`This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                           in iste
                           libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                           deserunt dicta
                           facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                           voluptas
                           voluptatum.`]} icon={null}/>

                </div>
            </div>

        </>
    );
}


export default HeroSection;

