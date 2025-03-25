'use client'

import  {useRef, useState, useEffect, ReactNode, FC} from "react";
import { createPortal } from "react-dom";

interface InfoBlockProps {
    heading: ReactNode,
    title: string,

    text: ReactNode[],
    icon?: string,
    fadeInAnimation?: string,
    bg?: string,
    nutrition?: string,
    ingredients?: string,
    expandable: boolean,
    url?: string
}

const InfoBlock: FC<InfoBlockProps> = ({
                                                 heading,
    title,
                                                 text,
                                                 icon = null,
                                                 fadeInAnimation = '',
                                                 bg = 'bg-danger',
                                                 expandable,
    url = null
                                             }) => {
    const ref = useRef(null);
    const title1 = useRef(null);
    const content = useRef(null);
    const [expanded, setExpanded] = useState(false);
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
        return () => setMounted(false);
    }, []);

    const toggleExpand = () => {
        if (expandable) {
            setExpanded(!expanded);
            // When expanding, prevent body scrolling
            if (!expanded) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        }
    };

    // Create the expanded view
    const renderExpandedView = () => {
        if (!expanded) return null;

        const modalContent = (
            <div
                className="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center"
                style={{
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    zIndex: 9999
                }}
                onClick={toggleExpand}
            >
                <div
                    className={`${bg} p-5 rounded-3`}
                    style={{
                        width: '80%',
                        maxWidth: '600px',
                        maxHeight: '80vh',
                        overflowY: 'auto'
                    }}
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="d-flex justify-content-end mb-2">
                        <button
                            className="btn btn-sm btn-dark"
                            onClick={toggleExpand}
                        >
                            ×
                        </button>
                    </div>

                    {icon !== null ? <img className='img-fluid mb-3' src={icon} alt="" style={{ maxWidth: '100%', maxHeight: '200px', objectFit: 'contain' }} /> : ''}
                    <h1 ref={title1} className='textAnimate'>{title}</h1>
                    {text.map((item, index) => <p key={index} ref={content} className='paraAnimate' style={{ fontSize: '1.2rem' }}>{item}</p>)}
                    {url?<a href={url} target="_blank">Food Network Site</a>:""}
                </div>
            </div>
        );

        // Use createPortal to render at body level
        if (typeof document !== 'undefined') {
            return createPortal(modalContent, document.body);
        }

        return null;
    };

    // Regular view
    return (
        <>
            <div
                ref={ref}
                className={`${fadeInAnimation} ${bg} p-3 m-4 rounded-3 infoBlock`}
                style={{
                    width: '100%',
                    boxSizing: 'border-box',
                    cursor: 'pointer',
                    transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out'
                }}
                onClick={toggleExpand}
                onMouseOver={(e) => {
                    e.currentTarget.style.transform = 'scale(1.03)';
                    e.currentTarget.style.boxShadow = '0 10px 15px rgba(0,0,0,0.2)';
                }}
                onMouseOut={(e) => {
                    e.currentTarget.style.transform = 'scale(1)';
                    e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
                }}
            >
                {/* Existing content */}
                {icon !== null ? <img className='img-fluid' src={icon} alt="" style={{ maxWidth: '100%', maxHeight: '100px', objectFit: 'contain' }} /> : ''}
                {heading}
                {text.map((item, index) => <div key={index} ref={content} className='paraAnimate'>{item}</div>)}
            </div>

            {/* Portal for expanded view */}
            {mounted && renderExpandedView()}
        </>
    );
}
export default InfoBlock;