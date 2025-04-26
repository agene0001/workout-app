import type { ComponentType } from 'svelte';

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

export interface InstacartRes {
    processed_ingredients: string[];
    response: { products_link_url: string };
}

export interface NavItemProps {
    text: string | svelte.JSX.Element;
}

export interface InfoBlockProps {
    heading: any;
    title: string;
    text: any[];
    recipe?: RecipeItem;
    icon?: string;
    fadeInAnimation?: string;
    bg?: string;
    nutrition?: string;
    ingredients?: string;
    expandable: boolean;
    url?: string;
}

export interface TeamMemberProps {
    name: string;
    role: string;
    bio: string;
    imgSrc: string;
    animationClass: string;
}

export interface ValueCardProps {
    icon: any;
    title: string;
    description: string;
    animationClass: string;
}

export interface AnimatedSectionProps {
    id: string;
    refProp: HTMLDivElement;
    isVisible: boolean;
    children: any;
    bgClass?: string;
}

export interface MilestoneProp {
    year: number | string;
    title: string;
    description: string;
    isRight: boolean;
    animationClass: string;
}