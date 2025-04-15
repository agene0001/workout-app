'use client'

import {useRef, useState, useEffect, FC} from "react";
import {createPortal} from "react-dom";
import {InfoBlockProps, InstacartRes} from "../types";
import axios from "axios";

const InfoBlock: FC<InfoBlockProps> = ({
                                           heading,
                                           title,
                                           text,
                                           recipe = null,
                                           fadeInAnimation = '',
                                           bg = 'bg-danger', // bg-danger -> Tailwind equivalent
                                           expandable,
                                           // url = null
                                       }) => {
    const ref = useRef(null);
    const title1 = useRef(null);
    const content = useRef(null);
    const [expanded, setExpanded] = useState(false);
    const [mounted, setMounted] = useState(false);
    const [instacartData, setInstacartData] = useState<InstacartRes|null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [currentRecipeId, setCurrentRecipeId] = useState<string|null>(null);

    useEffect(() => {
        setMounted(true);
        return () => setMounted(false);
    }, []);

    // Reset instacart data when recipe changes
    useEffect(() => {
        if (recipe && (!currentRecipeId || currentRecipeId !== recipe.name)) {
            setInstacartData(null);
            setCurrentRecipeId(recipe.name);
        }
    }, [recipe]);

    // Fetch Instacart data when expanded and we have a recipe
    useEffect(() => {
        if (expanded && recipe && !instacartData && !isLoading) {
            fetchInstacartData();
        }
    }, [expanded, recipe, instacartData, isLoading]);

    const fetchInstacartData = async () => {
        if (!recipe) return;

        setIsLoading(true);
        try {
            const instructions = recipe.instructions.split(/(?=\d\s?:\s)/).map(step => step.trim());
            console.log("Processing recipe:", recipe.name);

            const res = await axios.post('/recipes/process-recipe', {
                'ingredients': recipe.ingredients,
                'instructions': instructions,
                'title': recipe.name,
                'image_url': recipe.imgSrc
            });

            console.log("Instacart response:", res.data);
            setInstacartData(res.data || "");
        } catch (error) {
            console.error("Error fetching Instacart data:", error);
        } finally {
            setIsLoading(false);
        }
    };

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
                className="fixed top-0 left-0 w-full h-full flex items-center justify-center"
                style={{
                    backgroundColor: 'rgba(0,0,0,0.7)', zIndex: 9999
                }}
                onClick={toggleExpand}
            >
                <div
                    className={`${bg.split(' ')[0]} p-5 rounded-xl`}
                    style={{
                        width: '80%', maxWidth: '600px', maxHeight: '80vh', overflowY: 'auto'
                    }}
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="flex justify-end mb-2">
                        <button
                            className="px-2 py-1 text-sm bg-black text-white rounded"
                            onClick={toggleExpand}
                        >
                            ×
                        </button>
                    </div>

                    {recipe?.imgSrc !== '' ? (
                        <div className='flex justify-center '>
                            <div
                                className='mb-3 rounded-3xl overflow-hidden'
                                style={{maxWidth: '45%',maxHeight: '200px'}}
                            >
                                <img
                                    className='w-full h-full'
                                    src={recipe?.imgSrc}
                                    alt=""
                                    style={{objectFit: 'contain'}}
                                />
                            </div>
                        </div>
                    ) : ''}

                    <h1 ref={title1} className='text-5xl font-orbital font-bold text-gray-800 py-4 text-center'>{title}</h1>

                    {text.map((item, index) => (
                        <p
                            key={index}
                            ref={content}
                            className='paraAnimate text-lg'
                        >
                            {item}
                        </p>
                    ))}

                    {/*{url ? <a href={url} className="hover:text-[#C62368] text-purple-900" target="_blank" rel="noopener noreferrer">Food Network Site</a> : ""}*/}

                    {isLoading ? (
                        <div className='text-amber-500'>Loading Instacart data...</div>
                    ) : instacartData ? (
                        <div>
                            <button className="h-[46px] bg-[#003D29] px-[18px] py-[16px] text-[#FAF1E5] flex items-center gap-2 rounded-full">
                                <a
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-[#FAF1E5] hover:text-[#C62368] font-medium flex items-center gap-2"
                                    href={instacartData.response.products_link_url}
                                >
                                    <img
                                        src="/Instacart_Carrot.png"
                                        alt="Instacart Logo"
                                        className="w-[22px] h-[22px]"
                                    />
                                    Get Recipe Ingredients
                                </a>
                            </button>

                        </div>
                    ) : null}
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
                className={`${fadeInAnimation} ${bg} p-3 m-4 rounded-xl infoBlock`}
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
                {recipe?.imgSrc !== '' ? (
                    <div className='flex justify-center '>
                        <div
                            className='mb-3 rounded-xl overflow-hidden'
                            style={{maxWidth: '100%',maxHeight: '200px'}}
                        >
                            <img
                                className='w-full h-full'
                                src={recipe?.imgSrc}
                                alt=""
                                style={{objectFit: 'contain'}}
                            />
                        </div>
                    </div>
                ) : ''}

                {heading}

                {text.map((item, index) => (
                    <div key={index} ref={content} className='text-gray-900 '>
                        {item}
                    </div>
                ))}
            </div>

            {/* Portal for expanded view */}
            {mounted && renderExpandedView()}
        </>
    );
}

export default InfoBlock;