'use client'

import React, { useRef} from "react";
// import anime from 'animejs';
interface InfoBlockProps {
    heading: string,
    text: React.ReactNode[],
    icon?: string,
    // backgroundAnimate: boolean,
    fadeInAnimation: string | null,
    bg?: string,
    nutrition?: string,
    ingredients?: string// Making the prop optional
}
const InfoBlock:React.FC<InfoBlockProps> = ({
    heading,
    text,
    icon=null,
    // backgroundAnimate: boolean,
    fadeInAnimation,
    bg='bg-danger',
    // nutrition,
    // ingredients
}) => {
    // const [visible, setIsVisible] = useState(false);
    const ref = useRef(null);
    const title = useRef(null);
    const content = useRef(null);

    // useEffect(() => {
    //     // var textWrapper = content.current;
    //     // textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");
    //     // textWrapper = heading.current;
    //     // textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");
    //     //
    //     // heading.current.classList.add("textAnimate");
    //     // content.current.classList.add("paraAnimate");
    //
    //     // var t1 = anime.timeline({ loop: 1 })
    //     //     .add({
    //     //         targets: '.textAnimate .letter',
    //     //         scale: [0.3, 1],
    //     //         opacity: [0, 1],
    //     //         translateZ: 0,
    //     //         easing: "easeOutExpo",
    //     //         duration: 600,
    //     //         delay: (el, i) => 40 * (i + 1)
    //     //     });
    //     // var t2 = anime.timeline({ loop: 1 }).add({
    //     //     targets: '.paraAnimate .letter',
    //     //     scale: [0.3, 1],
    //     //     opacity: [0, 1],
    //     //     translateZ: 0,
    //     //     easing: "easeOutExpo",
    //     //     duration: 600,
    //     //     delay: (el, i) => 5 * (i + 1)
    //     // });
    // }, [props.animation]);

    return (
        <div
            ref={ref}
            // onClick={(ele) => {
            //     if (props.backgroundAnimate) {
            //         // ele.target.style.width = "100vw";
            //         // ele.target.style.height = "100vh";
            //     }
            // }}
            className={`${fadeInAnimation} ${bg} p-3 m-4 rounded-3 infoBlock`}
            style={{ width: '100%', boxSizing: 'border-box' }}
        >
            {icon !== null ? <img className='img-fluid' src={icon} alt="" style={{ maxWidth: '100%', maxHeight: '100px', objectFit: 'contain' }} /> : ''}
            <h1 ref={title} className='textAnimate' >{heading}</h1>
            {text.map((item, index) => <p key={index} ref={content} className='paraAnimate'>{item}</p>)}
        </div>
    );
}

export default InfoBlock;