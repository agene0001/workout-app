'use client'
import {useRef, useState, useEffect} from "react";
import anime from 'animejs';
import {AnimatedSectionProps, MilestoneProp, ValueCardProps} from "../types";

// Custom TeamMember component
// function TeamMember(props:TeamMemberProps) {
//     return (
//         <div className={`team-member ${props.animationClass}`}>
//             <div className="bg-[#f8f9fa] border-[0.75rem] border-[rgba(0,255,255,0.5)] shadow-[6px_6px_3px_rgba(0,255,125,1)] rounded-[2px] overflow-hidden h-full">
//                 <div className="h-[250px] overflow-hidden">
//                     <img
//                         src={props.imgSrc}
//                         alt={props.name}
//                         className="w-full h-full object-cover"
//                     />
//                 </div>
//                 <div className="p-4">
//                     <h3 className="text-primary mb-1">{props.name}</h3>
//                     <h5 className="text-danger mb-3">{props.role}</h5>
//                     <p>{props.bio}</p>
//                 </div>
//             </div>
//         </div>
//     );
// }

// Custom ValueCard component
function ValueCard(props:ValueCardProps) {
    return (
        <div className={`value-card ${props.animationClass}`}>
            <div className="p-8 bg-info border-[0.5rem] border-[rgba(0,255,255,0.5)] shadow-[6px_6px_3px_rgba(0,255,125,1)] rounded-[2px] h-full flex flex-col items-center text-center">
                <div className="mb-3 w-[60px] h-[60px] rounded-full bg-[rgba(204,43,94,0.2)] flex justify-center items-center">
                    {props.icon}
                </div>
                <h3 className="text-primary text-2xl mb-3">{props.title}</h3>
                <p className="mb-0">{props.description}</p>
            </div>
        </div>
    );
}

// Custom Section component
function AnimatedSection(props:AnimatedSectionProps) {
    return (
        <div
            ref={props.refProp}
            id={props.id}
            className={`${props.bgClass || ''} py-5`}
        >
            <div
                className={`container mx-auto px-4 ${props.isVisible ? 'fade-in' : ''}`}
                style={{
                    opacity: props.isVisible ? 1 : 0,
                    transform: props.isVisible ? 'translateY(0)' : 'translateY(30px)',
                    transition: 'opacity 0.8s ease, transform 0.8s ease'
                }}
            >
                {props.children}
            </div>
        </div>
    );
}

// Custom Milestone component for timeline
function Milestone(props:MilestoneProp) {
    return (
        <div className={`milestone ${props.isRight ? 'flex justify-end' : 'flex justify-start'} ${props.animationClass} mb-8 w-full`}>
            <div className={`w-4/5 p-6 ${props.isRight ? 'bg-[rgba(0,255,255,0.1)] border-[0.5rem] border-[rgba(0,255,255,0.3)] shadow-[4px_4px_2px_rgba(0,255,125,0.5)]' : 'bg-[rgba(204,43,94,0.1)] border-[0.5rem] border-[rgba(204,43,94,0.3)] shadow-[4px_4px_2px_rgba(204,43,94,0.5)]'} rounded-[2px] relative`}>
                <div className={`absolute -top-[10px] ${props.isRight ? 'right-[20px] bg-[rgba(0,255,255,0.5)]' : 'left-[20px] bg-[rgba(204,43,94,0.5)]'} py-1 px-4 rounded-[15px]`}>
                    <h6 className="mb-0 text-white">{props.year}</h6>
                </div>
                <h4 className={`${props.isRight ? 'text-danger' : 'text-info'} text-2xl font-orbital mt-4`}>{props.title}</h4>
                <p className="mb-0 text-primary">{props.description}</p>
            </div>
        </div>
    );
}

// Main About Us Component
function AboutUs() {
    const missionRef = useRef(null);
    const journeyRef = useRef(null);
    const teamRef = useRef(null);
    const valuesRef = useRef(null);
    const contactRef = useRef(null);

    const [missionVisible, setMissionVisible] = useState(false);
    const [journeyVisible, setJourneyVisible] = useState(false);
    // const [teamVisible, setTeamVisible] = useState(false);
    const [valuesVisible, setValuesVisible] = useState(false);
    const [contactVisible, setContactVisible] = useState(false);

    // Team member data
    // const teamMembers = [
    //     {
    //         name: "Dr. Sarah Chen",
    //         role: "Nutrition Specialist",
    //         bio: "Dr. Chen has over 15 years of experience in sports nutrition and holds a Ph.D. in Nutritional Sciences. She specializes in developing personalized meal plans for athletes and fitness enthusiasts.",
    //         imgSrc: "/api/placeholder/300/300"
    //     },
    //     {
    //         name: "Elena Figex",
    //         role: "Fitness Director",
    //         bio: "A certified personal trainer with expertise in strength training and functional fitness, Elena has helped hundreds of clients achieve their fitness goals through personalized workout programs.",
    //         imgSrc: "/api/placeholder/300/300"
    //     },
    //     {
    //         name: "Alex Fenige",
    //         role: "Community Manager",
    //         bio: "Alex oversees our forum groups and community initiatives. With a background in health psychology, He is passionate about creating supportive environments for long-term wellness success.",
    //         imgSrc: "/api/placeholder/300/300"
    //     }
    // ];

    // Timeline milestones
    const milestones = [
        {
            year: "2020",
            title: "Our Founding",
            description: "Started with a simple vision to make personalized nutrition accessible to everyone.",
            isRight: false
        },
        {
            year: "2021",
            title: "Launch of Recipe Archive",
            description: "Introduced our comprehensive repository of nutritious recipes tailored to different dietary preferences.",
            isRight: true
        },
        {
            year: "2022",
            title: "AI Nutrition Recommender",
            description: "Developed our state-of-the-art AI system to provide personalized meal recommendations based on individual needs.",
            isRight: false
        },
        {
            year: "2023",
            title: "Community Forums",
            description: "Established forum groups to connect like-minded individuals on their fitness and nutrition journeys.",
            isRight: true
        },
        {
            year: "2024",
            title: "Progress Tracker Launch",
            description: "Introduced our comprehensive progress tracking system to help users monitor their fitness journey.",
            isRight: false
        }
    ];

    // Values data with SVG icons
    const values = [
        {
            icon: <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="rgba(204, 43, 94, 1)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
            </svg>,
            title: "Evidence-Based Approach",
            description: "We believe in science-backed nutrition and fitness recommendations, constantly updating our content based on the latest research."
        },
        {
            icon: <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="rgba(204, 43, 94, 1)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>,
            title: "Community Support",
            description: "We foster a positive, inclusive environment where members can share experiences, challenges, and successes."
        },
        {
            icon: <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="rgba(204, 43, 94, 1)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"></path>
                <line x1="16" y1="8" x2="2" y2="22"></line>
                <line x1="17.5" y1="15" x2="9" y2="15"></line>
            </svg>,
            title: "Personalization",
            description: "We understand that every individual has unique needs and goals, which is why our platform tailors recommendations to your specific requirements."
        }
    ];

    useEffect(() => {
        // Add styles to document head
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .fade-in-1 {
                animation: fadeIn 0.8s ease forwards;
                animation-delay: 0.2s;
                opacity: 0;
            }
            
            .fade-in-2 {
                animation: fadeIn 0.8s ease forwards;
                animation-delay: 0.4s;
                opacity: 0;
            }
            
            .fade-in-3 {
                animation: fadeIn 0.8s ease forwards;
                animation-delay: 0.6s;
                opacity: 0;
            }
        `;
        document.head.appendChild(style);

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.target === missionRef.current) {
                    setMissionVisible(entry.isIntersecting);
                } else if (entry.target === journeyRef.current) {
                    setJourneyVisible(entry.isIntersecting);
                }
                // else if (entry.target === teamRef.current) {
                //     setTeamVisible(entry.isIntersecting);
                // }
                else if (entry.target === valuesRef.current) {
                    setValuesVisible(entry.isIntersecting);
                } else if (entry.target === contactRef.current) {
                    setContactVisible(entry.isIntersecting);
                }
            });
        }, { threshold: 0.1 });

        anime({
            targets: '.hero-circle-1',
            translateX: ['10%', '-10%'],
            translateY: ['5%', '-15%'],
            scale: [1, 1.2],
            opacity: [0.4, 0.5],
            easing: 'easeInOutSine',
            duration: 10000,
            direction: 'alternate',
            loop: true
        });

        anime({
            targets: '.hero-circle-2',
            translateX: ['-5%', '15%'],
            translateY: ['-10%', '5%'],
            scale: [1.1, 0.9],
            opacity: [0.5, 0.3],
            easing: 'easeInOutQuad',
            duration: 13000,
            direction: 'alternate',
            loop: true
        });

        // Observe refs
        if (missionRef.current) observer.observe(missionRef.current);
        if (journeyRef.current) observer.observe(journeyRef.current);
        if (teamRef.current) observer.observe(teamRef.current);
        if (valuesRef.current) observer.observe(valuesRef.current);
        if (contactRef.current) observer.observe(contactRef.current);

        return () => {
            // Clean up
            if (missionRef.current) observer.unobserve(missionRef.current);
            if (journeyRef.current) observer.unobserve(journeyRef.current);
            // if (teamRef.current) observer.unobserve(teamRef.current);
            if (valuesRef.current) observer.unobserve(valuesRef.current);
            if (contactRef.current) observer.unobserve(contactRef.current);
            document.head.removeChild(style);
        };
    }, []);

    return (
        <>

            {/* Hero Section with enhanced background */}
            <div className="relative min-h-[500px] flex items-center justify-center overflow-hidden">
                {/* Animated gradient background */}
                <div className="absolute inset-0 bg-[#002233] z-0"></div>

                {/* Animated wave pattern overlay */}
                <div className="absolute inset-0 z-0 opacity-20">
                    <svg width="100%" height="100%" viewBox="0 0 1440 320" preserveAspectRatio="none">
                        <path
                            fill="rgba(0, 255, 255, 0.4)"
                            fillOpacity="1"
                            d="M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
                            className="animate-pulse"
                            style={{animationDuration: '10s'}}
                        ></path>
                    </svg>
                </div>

                {/* Second wave pattern with different animation */}
                <div className="absolute inset-0 z-0 opacity-20">
                    <svg width="100%" height="100%" viewBox="0 0 1440 320" preserveAspectRatio="none">
                        <path
                            fill="rgba(204, 43, 94, 0.4)"
                            fillOpacity="1"
                            d="M0,64L48,80C96,96,192,128,288,154.7C384,181,480,203,576,186.7C672,171,768,117,864,122.7C960,128,1056,192,1152,208C1248,224,1344,192,1392,176L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
                            className="animate-pulse"
                            style={{animationDuration: '15s'}}
                        ></path>
                    </svg>
                </div>

                {/* Animated gradient circles */}
                <div className="hero-circle-1 absolute w-[300px] h-[300px] rounded-full bg-[rgba(204,43,94,0.3)] filter blur-[40px] top-[20%] left-[10%] z-0"></div>
                <div className="hero-circle-2 absolute w-[400px] h-[400px] rounded-full bg-[rgba(0,255,255,0.3)] filter blur-[60px] bottom-[10%] right-[5%] z-0"></div>

                {/* Low poly grid background */}
                <div className="absolute inset-0 low-poly2 bg-center bg-cover bg-no-repeat opacity-20 z-0"></div>



                {/* Content */}
                <div className="container mx-auto text-center relative py-4 z-10">
                    <h1 className="text-6xl text-gradient-1 mb-4 font-orbital-style-normal hero-start">
                        About Our Mission
                    </h1>
                    <p className="text-xl text-primary mb-5 max-w-[800px] mx-auto shadow-[1px_1px_3px_rgba(0,0,0,0.2)] hero-start-delay">
                        We're passionate about empowering individuals to achieve their wellness goals through personalized nutrition and fitness solutions.
                    </p>
                    <a href="#mission" className="px-8 py-3 border-2 border-[var(--primary)] text-[var(--primary)] rounded-[2px] inline-block hover:bg-[rgba(0,255,255,0.1)] transition-colors duration-300">
                        Learn More
                    </a>
                </div>
            </div>

            {/* Mission Section */}
            <AnimatedSection
                id="mission"
                refProp={missionRef}
                isVisible={missionVisible}
                bgClass="bg-[rgba(0,255,255,0.2)]"
            >
                <div className="flex flex-col md:flex-row md:items-center">
                    <div className="w-full md:w-1/2 mb-4 md:mb-0">
                        <div className="border-l-[6px] border-[rgba(204,43,94,0.8)] pl-8">
                            <h2 className="text-5xl text-danger font-orbital-style-normal mb-4">Our Mission</h2>
                            <p className="text-lg text-primary mb-4">To empower individuals on their journey to optimal health through science-backed nutrition guidance and a supportive community environment.</p>
                        </div>
                        <p className="mb-4 mx-2 text-primary">At our core, we believe that everyone deserves access to personalized nutrition information that fits their unique lifestyle, preferences, and goals. Our platform combines cutting-edge technology with expert knowledge to deliver custom-tailored nutrition plans and workout recommendations.</p>
                        <p className="mx-2 text-primary">We're more than just a recipe database – we're a comprehensive wellness ecosystem designed to support you at every step of your journey toward better health.</p>
                    </div>
                    <div className="w-full md:w-1/2">
                        <div className="border-[1rem] border-[rgba(0,255,255,0.5)] shadow-[3px_3px_3px_rgba(0,255,125,.5)] rounded-[2px] overflow-hidden h-[400px]">
                            <img
                                src="/aboutus.png"
                                alt="Our Mission"
                                className="w-full h-full"                            />
                        </div>
                    </div>
                </div>
            </AnimatedSection>

            {/* Journey Timeline Section */}
            <AnimatedSection
                id="journey"
                refProp={journeyRef}
                isVisible={journeyVisible}
                bgClass="bg-light"
            >
                <h2 className="text-5xl text-primary font-bold font-orbital text-center mb-5">Our Journey</h2>
                <div className="journey-timeline">
                    {milestones.map((milestone, index) => (
                        <Milestone
                            key={index}
                            year={milestone.year}
                            title={milestone.title}
                            description={milestone.description}
                            isRight={milestone.isRight}
                            animationClass={journeyVisible ? `fade-in-${(index % 3) + 1}` : ''}
                        />
                    ))}
                </div>
            </AnimatedSection>

            {/* Team Section */}
            {/*<AnimatedSection*/}
            {/*    id="team"*/}
            {/*    refProp={teamRef}*/}
            {/*    isVisible={teamVisible}*/}
            {/*    bgClass="bg-light"*/}
            {/*>*/}
            {/*    <h2 className="text-4xl text-[var(--primary)] text-center mb-5">Meet Our Team</h2>*/}
            {/*    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">*/}
            {/*        {teamMembers.map((member, index) => (*/}
            {/*            <div key={index}>*/}
            {/*                <TeamMember*/}
            {/*                    name={member.name}*/}
            {/*                    role={member.role}*/}
            {/*                    bio={member.bio}*/}
            {/*                    imgSrc={member.imgSrc}*/}
            {/*                    animationClass={teamVisible ? `fade-in-${(index % 3) + 1}` : ''}*/}
            {/*                />*/}
            {/*            </div>*/}
            {/*        ))}*/}
            {/*    </div>*/}
            {/*</AnimatedSection>*/}

            {/* Values Section */}
            <AnimatedSection
                id="values"
                refProp={valuesRef}
                isVisible={valuesVisible}
                bgClass="bg-light"
            >
                <h2 className="text-5xl text-primary font-bold font-orbital-style-normal text-center mb-5">Our Core Values</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {values.map((value, index) => (
                        <div key={index}>
                            <ValueCard
                                icon={value.icon}
                                title={value.title}
                                description={value.description}
                                animationClass={valuesVisible ? `fade-in-${(index % 3) + 1}` : ''}
                            />
                        </div>
                    ))}
                </div>
            </AnimatedSection>

            {/* Contact Section */}
            <AnimatedSection
                id="contact"
                refProp={contactRef}
                isVisible={contactVisible}
                bgClass="bg-light"
            >
                <div className="flex justify-center mb-5">
                    <div className="w-full md:w-2/3 text-center">
                        <h2 className="text-4xl text-danger mb-4">Get In Touch</h2>
                        <p className="text-lg text-primary">Have questions or feedback? We'd love to hear from you!</p>
                    </div>
                </div>
                <div className="flex justify-center">
                    <div className="w-full md:w-2/3">
                        <div className="bg-[#002233] border-[1rem] border-[rgba(0,255,255,0.5)] shadow-[8px_8px_3px_rgba(0,255,125,1)] rounded-[2px] p-8">
                            <form>
                                <div className="flex flex-col md:flex-row gap-4 mb-4">
                                    <div className="w-full md:w-1/2">
                                        <input
                                            type="text"
                                            className="w-full h-[50px] border-[var(--danger)] bg-amber-50 border-4 px-3"
                                            placeholder="Your Name"
                                        />
                                    </div>
                                    <div className="w-full md:w-1/2">
                                        <input
                                            type="email"
                                            className="w-full h-[50px] border-[var(--danger)] bg-amber-50 border-4 px-3"
                                            placeholder="Your Email"
                                        />
                                    </div>
                                </div>
                                <div className="mb-4">
                                    <input
                                        type="text"
                                        className="w-full h-[50px] border-[var(--danger)] bg-amber-50 border-4 px-3"
                                        placeholder="Subject"
                                    />
                                </div>
                                <div className="mb-4">
                                    <textarea
                                        className="w-full border-[var(--danger)] bg-amber-50 border-4 p-3"
                                        rows={6}
                                        placeholder="Your Message"
                                    ></textarea>
                                </div>
                                <div className="text-center">
                                    <button
                                        type="submit"
                                        className="px-5 py-2 border-2 border-[var(--primary)] text-[var(--primary)] rounded-[2px] text-lg"
                                    >
                                        Send Message
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </AnimatedSection>

            {/* Final CTA Section */}
            <div className="py-5 text-center" style={{
                background: 'linear-gradient(135deg, rgba(204, 43, 94, 0.8) 0%, rgba(0, 255, 255, 0.8) 100%)'
            }}>
                <div className="container mx-auto py-4">
                    <h2 className="text-white mb-4">Ready to Transform Your Wellness Journey?</h2>
                    <a href="#" className="px-5 py-2 bg-white rounded-[2px] text-lg inline-block">
                        Join Our Community Today
                    </a>
                </div>
            </div>
        </>
    );
}

export default AboutUs;