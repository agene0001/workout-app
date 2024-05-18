import {CSSProperties, useRef, useEffect, useState} from "react";
import InfoBlock from "./InfoBlock.tsx";

let heroHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '6rem'}
let subHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '3rem'}


let paraStyle: CSSProperties = {textAlign: 'center', fontSize: '1.5rem'}


function HeroSection() {
    const myRef = useRef();
    const myRef2 = useRef();
    const [heroStart, setHeroStartIsVisible] = useState(false);
    const [heroSecond, setHeroSecondIsVisible] = useState(false);
    useEffect(() => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry)=>{
                if(entry.target.className.includes('heroback')){
                    setHeroStartIsVisible(entry.isIntersecting);
                }
                else if(entry.target.className.includes('layer3')){
                    setHeroSecondIsVisible(entry.isIntersecting);
                }
                else{
                    setInfoBlock1(entry.isIntersecting);
                }
            })
            // const entry = entries[0];
            // setMyElementIsVisible(entry.isIntersecting);
        })
        observer.observe(myRef.current);
        observer.observe(myRef2.current);
    }, [])

       // It
    return (
        <>

            <div ref={myRef}
                 className={`heroback layer2 d-flex justify-content-end align-items-center container-fluid p-3`}
                 id='hero'>
                <div className={`d-block ${heroStart ? 'heroStart' : '' }`}>
                    <h1 style={heroHeadingStyle} id='heroText'>Unleashing Your Potential Through Fitness and
                        Nutrition</h1>
                </div>
            </div>


            <div  className="spacer layer1"></div>
            <div ref={myRef2} className="container-fluid stackedHaikei layer3 py-3" id="hero2">
                <section>
                    <h1 style={subHeadingStyle} className={`text-info ${heroSecond ? 'heroStart' : '' }`}>Achieve Peak Fitness and Wellness with Our
                        Comprehensive Site</h1>
                    <p style={paraStyle} className={`text-primary ${heroSecond ? 'heroStart1' : '' }`}><br/> At our platform, we're passionate about
                        building
                        a vibrant community
                        where individuals can thrive in their active lifestyles. Our goal is to provide a
                        holistic
                        approach to health and wellness by offering a diverse range of workout disciplines,
                        personalized
                        nutrition guidance, and a supportive environment for like-minded peers to connect and
                        learn.


                        Explore our site's diverse sections tailored to various martial arts and workout
                        disciplines,
                        designed to cater to enthusiasts of all levels. Whether you're passionate about MMA,
                        Brazilian
                        Jiu-Jitsu, Muay Thai, etc, our expert-led content and dedicated groups
                        are here to help you progress and achieve your fitness goals.


                    </p>
                </section>
            </div>
            <div className="container-fluid text-center vh-100 align-content-center py-3" id="hero3">
                <div className='row py-3'>
                    <InfoBlock heading='Exceptional Archive' text='This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                           in iste
                           libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                           deserunt dicta
                           facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                           voluptas
                           voluptatum.' icon={null}/>
                    <InfoBlock heading='Personalized Nutrition' text='This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                           in iste
                           libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                           deserunt dicta
                           facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                           voluptas
                           voluptatum.' icon={null}/>

                    <InfoBlock heading='Progress Tracker/ Forum Groups' text='This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                           in iste
                           libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                           deserunt dicta
                           facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                           voluptas
                           voluptatum.' icon={null}/>

                </div>
            </div>

        </>
    );
}


export default HeroSection;

