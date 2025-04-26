import {ReactNode, RefObject} from "react";

export interface RecipeItem {
    name: string;
    nutrition: string;
    ingredients: string;
    instructions: string;
    imgSrc: string;
    duration: string;
    rating: number;
    url: string;
}
export interface InstacartRes{
    processed_ingredients: string[],
    response: {products_link_url: string}
}
export  interface NavItemProps {
    text: string | Jsx.Element; // This allows text to be either a string or JSX.Element
}
export  interface InfoBlockProps {
    heading: ReactNode,
    title: string,

    text: ReactNode[],
    recipe?: RecipeItem
    icon?: string,
    fadeInAnimation?: string,
    bg?: string,
    nutrition?: string,
    ingredients?: string,
    expandable: boolean,
    url?: string
}

// About us properties
// Interface for TeamMember component props
interface TeamMemberProps {
    name: string;
    role: string;
    bio: string;
    imgSrc: string;
    animationClass: string;
}

// Interface for ValueCard component props
interface ValueCardProps {
    icon: ReactNode;
    title: string;
    description: string;
    animationClass: string;
}

// Interface for AnimatedSection component props
interface AnimatedSectionProps {
    id: string;
    refProp: RefObject<HTMLDivElement>;
    isVisible: boolean;
    children: ReactNode;
    bgClass?: string;
}
interface MilestoneProp{
    year: number|string,
    title:string,
    description:string,
    isRight: boolean,
    animationClass:string
}

