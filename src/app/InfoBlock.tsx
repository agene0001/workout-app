'use client'
import {useRef, useState, useEffect} from "react";
import anime from 'animejs'

function InfoBlock(props: { heading: string, text: string, icon: string | null, animation: string }) {
    const [visible, setIsVisible] = useState(false);
    const ref = useRef(null);
    const heading = useRef(null);
    const content = useRef(null);
    useEffect(() => {

        const observer = new IntersectionObserver((entries) => {

            entries.forEach(entry => {
                if (ref.current) {
                    setIsVisible(entry.isIntersecting);
                }

                observer.disconnect();
            })
        })
        if (ref.current) {
            observer.observe(ref.current)
        }



    }, []);
    useEffect(()=>{

            var textWrapper = content.current;
            // console.log(textWrapper.innerText);
            textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");
            textWrapper = heading.current;
            // console.log(textWrapper.innerText);
            textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

            heading.current.classList.add("textAnimate");
            content.current.classList.add("paraAnimate");
            var t1 = anime.timeline({loop: 1})
                .add({
                    targets: '.textAnimate .letter',
                    scale: [0.3, 1],
                    opacity: [0, 1],
                    translateZ: 0,
                    easing: "easeOutExpo",
                    duration: 600,
                    delay: (el, i) => 40 * (i + 1)
                });
            var t2= anime.timeline({loop: 1}).add({
                targets: '.paraAnimate .letter',
                scale: [0.3, 1],
                opacity: [0, 1],
                translateZ: 0,
                easing: "easeOutExpo",
                duration: 600,
                delay: (el, i) => 5 * (i + 1)
            })
    })

    return (
        <div ref={ref} className={`${props.animation} col p-3 m-5 bg-danger rounded-3 infoBlock`}>
            {props.icon !== null ? <img className='img-fluid' src={props.icon} alt=""/> : ''}
            <h1 ref={heading} className='textAnimate'>{props.heading}</h1>
            {props.text.map((item) => <p ref={content} className='paraAnimate'>{item}</p>)}
        </div>
    );
}

export default InfoBlock