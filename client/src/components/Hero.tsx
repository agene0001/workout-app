import {CSSProperties} from "react";

let heroHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '6rem'}
let subHeadingStyle: CSSProperties = {textAlign: 'center', fontSize: '3rem'}

let paraStyle: CSSProperties = {textAlign: 'center', fontSize: '1.5rem'}

function HeroSection() {
    return (
        <>
            <div className='heroback layer2 d-flex justify-content-end align-items-center vh-100 p-3' id='hero'>
                <div className='d-block vw-100'>
                    <h1 style={heroHeadingStyle} id='heroText'>Unleashing Your Potential Through Fitness and
                        Nutrition</h1>
                </div>
            </div>
            <div className="spacer layer1"></div>
            <div className="container-fluid stackedHaikei layer3" id="hero2">
                <section>
                    <h1 style={subHeadingStyle} className='text-info'>Achieve Peak Fitness and Wellness with Our
                        Comprehensive Site</h1>
                    <p style={paraStyle} className='text-primary'><br/> At our platform, we're passionate about building
                        a vibrant community
                        where individuals can thrive in their active lifestyles. Our goal is to provide a holistic
                        approach to health and wellness by offering a diverse range of workout disciplines, personalized
                        nutrition guidance, and a supportive environment for like-minded peers to connect and learn.

                        Explore our site's diverse sections tailored to various martial arts and workout disciplines,
                        designed to cater to enthusiasts of all levels. Whether you're passionate about MMA, Brazilian
                        Jiu-Jitsu, Muay Thai, etc, our expert-led content and dedicated groups
                        are here to help you progress and achieve your fitness goals.

                    </p>
                </section>
            </div>
            <div className="container-fluid text-center vh-100 align-content-center" id="hero3">
                <div className='row'>
                    <div className="col p-3 m-5 bg-danger" id='hero3B1'>
                        <h1>Info Block</h1>
                        <p>This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                            in iste
                            libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                            deserunt dicta
                            facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                            voluptas
                            voluptatum.</p>
                    </div>
                    <div className="col p-3 m-5 bg-danger" id='hero3B2'>
                        <h1>Info Block</h1>
                        <p>This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                            in iste
                            libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                            deserunt dicta
                            facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                            voluptas
                            voluptatum.</p>
                    </div>
                    <div className="col p-3 m-5 bg-danger" id='hero3B3'>
                        <h1>Info Block</h1>
                        <p>This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                            in iste
                            libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                            deserunt dicta
                            facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                            voluptas
                            voluptatum.</p>
                    </div>
                </div>
            </div>
            {/*/!*<section>*!/*/}
            {/*    <div className="container text-center" id="hero3">*/}
            {/*        <div className='row'>*/}
            {/*            <div className='col p-3 m-3'>*/}
            {/*                <h1 className='text-info'>Achieve Peak Fitness and Wellness with Our Comprehensive Site</h1>*/}
            {/*                <p className='text-primary'><br/> At our platform, we're passionate about building a vibrant*/}
            {/*                    community*/}
            {/*                    where individuals can thrive in their active lifestyles. Our goal is to provide a*/}
            {/*                    holistic*/}
            {/*                    approach to health and wellness by offering a diverse range of workout disciplines,*/}
            {/*                    personalized*/}
            {/*                    nutrition guidance, and a supportive environment for like-minded peers to connect and*/}
            {/*                    learn.*/}

            {/*                    Explore our site's diverse sections tailored to various martial arts and workout*/}
            {/*                    disciplines,*/}
            {/*                    designed to cater to enthusiasts of all levels. Whether you're passionate about MMA,*/}
            {/*                    Brazilian*/}
            {/*                    Jiu-Jitsu, Muay Thai, etc, our expert-led content and dedicated groups*/}
            {/*                    are here to help you progress and achieve your fitness goals.*/}

            {/*                </p>*/}
            {/*            </div>*/}

            {/*            <div className='col p-3 m-3'>*/}
            {/*                <h1 className='text-info'>Achieve Peak Fitness and Wellness with Our Comprehensive Site</h1>*/}
            {/*                <p className='text-primary'><br/> At our platform, we're passionate about building a vibrant*/}
            {/*                    community*/}
            {/*                    where individuals can thrive in their active lifestyles. Our goal is to provide a*/}
            {/*                    holistic*/}
            {/*                    approach to health and wellness by offering a diverse range of workout disciplines,*/}
            {/*                    personalized*/}
            {/*                    nutrition guidance, and a supportive environment for like-minded peers to connect and*/}
            {/*                    learn.*/}

            {/*                    Explore our site's diverse sections tailored to various martial arts and workout*/}
            {/*                    disciplines,*/}
            {/*                    designed to cater to enthusiasts of all levels. Whether you're passionate about MMA,*/}
            {/*                    Brazilian*/}
            {/*                    Jiu-Jitsu, Muay Thai, etc, our expert-led content and dedicated groups*/}
            {/*                    are here to help you progress and achieve your fitness goals.*/}

            {/*                </p>*/}
            {/*            </div>*/}
            {/*            <div className='col p-3 m-3'>*/}
            {/*                <h1 className='text-info'>Achieve Peak Fitness and Wellness with Our Comprehensive Site</h1>*/}
            {/*                <p className='text-primary'><br/> At our platform, we're passionate about building a vibrant*/}
            {/*                    community*/}
            {/*                    where individuals can thrive in their active lifestyles. Our goal is to provide a*/}
            {/*                    holistic*/}
            {/*                    approach to health and wellness by offering a diverse range of workout disciplines,*/}
            {/*                    personalized*/}
            {/*                    nutrition guidance, and a supportive environment for like-minded peers to connect and*/}
            {/*                    learn.*/}

            {/*                    Explore our site's diverse sections tailored to various martial arts and workout*/}
            {/*                    disciplines,*/}
            {/*                    designed to cater to enthusiasts of all levels. Whether you're passionate about MMA,*/}
            {/*                    Brazilian*/}
            {/*                    Jiu-Jitsu, Muay Thai, etc, our expert-led content and dedicated groups*/}
            {/*                    are here to help you progress and achieve your fitness goals.*/}

            {/*                </p>*/}
            {/*            </div>*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*/!*</section>*!/*/}

        </>
    );
}

export default HeroSection;