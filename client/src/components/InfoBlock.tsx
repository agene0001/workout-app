import {useRef, useState, useEffect} from "react";
function InfoBlock(props:{heading:string,text:string,icon:string|null}) {

    return (
        <div className={` col p-3 m-5 bg-danger infoBlock`}>
            {props.icon!==null?<img src={props.icon} alt=""/>:''}
            <h1>{props.heading}</h1>
            <p>{props.text}</p>
        </div>
    );
}

export default InfoBlock