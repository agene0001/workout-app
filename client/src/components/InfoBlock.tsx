import {useRef, useState, useEffect} from "react";
function InfoBlock(props:{heading:string,text:string,icon:string|null,animation:string}) {
    const [visible,setIsVisible] = useState(false);
    const ref = useRef(null);
    useEffect(() => {

        const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {
            if(ref.current) {
                setIsVisible(entry.isIntersecting);
            }

            observer.disconnect();
        })
        })
        if(ref.current) {
            observer.observe(ref.current)
        }
    }, []);
    return (
        <div ref={ref} className={`${props.animation} col p-3 m-5 bg-danger infoBlock`}>
            {props.icon!==null?<img src={props.icon} alt=""/>:''}
            <h1>{props.heading}</h1>
            <p>{props.text}</p>
        </div>
    );
}

export default InfoBlock