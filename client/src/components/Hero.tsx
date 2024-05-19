import {CSSProperties, useRef, useEffect, useState} from "react";
import InfoBlock from "./InfoBlock.tsx";

let heroHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '6rem'}
let subHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '3rem'}


let paraStyle: CSSProperties = {textAlign: 'center', fontSize: '1.5rem'}


function HeroSection() {
    const myRef1 = useRef(null);
    const myRef2 = useRef(null);
    const myRef3 = useRef(null);
    const infoTitle:string = 'Exceptional Archive'
    const infoTitle1:string = 'Personalized Nutrition'
    const infoTitle2:string = 'Progress Tracker/ Forum Groups'
    const [heroStart, setHeroStartIsVisible] = useState(false);
    const [heroSecond, setHeroSecondIsVisible] = useState(false);
    const [blocks, setBlocksIsVisible] = useState(false);
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
                    setBlocksIsVisible(entry.isIntersecting);
                }
            })
            // const entry = entries[0];
            // setMyElementIsVisible(entry.isIntersecting);
        })
        observer.observe(myRef1.current);
        observer.observe(myRef2.current);
        observer.observe(myRef3.current);

    }, [])

       // It
    return (
        <>

            <div ref={myRef1}
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

                    </p>
                </section>
            </div>
            <div className="container-fluid text-center vh-100 align-content-center py-3" id="hero3">
                <div ref={myRef3} className='row py-3'>
                    <InfoBlock animation={`${blocks?'infoHero':''}`} heading={infoTitle} text='This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                           in iste
                           libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                           deserunt dicta
                           facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                           voluptas
                           voluptatum.' icon={null}/>
                    <InfoBlock  animation={`${blocks?'infoHero1':''}`} heading={infoTitle1} text='This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                           in iste
                           libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                           deserunt dicta
                           facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                           voluptas
                           voluptatum.' icon={null}/>

                    <InfoBlock animation={`${blocks?'infoHero2':''}`} heading={infoTitle2} text='This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
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

