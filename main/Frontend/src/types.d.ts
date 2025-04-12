import {ReactNode} from "react";

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
